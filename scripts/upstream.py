#!/usr/bin/env python3
"""Resolve a fixture's `upstream` entries (PROTOCOL.md section 12, ADR 0001). Standard library only.

resolve(entry, machine_checkout=None) -> (state, reason). States:
  satisfied        engine/pr: the checkout contains the PR head (or its merge commit)
  pending          PR or issue still open, not in the checkout, or gh could not say (reason says which)
  merged           PR merged upstream: re-point citations to the merge commit
  closed-unmerged  PR closed without merging: needs a human decision
  issue-closed     issue closed (GitHub) or resolved Done/Fixed (Jira): retire or re-check
  rejected         Jira issue resolved Won't Fix/Won't Do: needs a human decision
Git ancestry decides first (no network); gh is asked only when git cannot decide. A missing, unauthenticated or
offline gh yields `pending` with the reason; this module never raises for a network or tooling failure.
"""
import base64
import json
import os
import re
import subprocess
import urllib.request

REF = re.compile(r"^([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#([0-9]+)$")
JIRA_REF = re.compile(r"^jira:([A-Z][A-Z0-9]*-[0-9]+)$")  # FieldWorks tracks issues in Jira project LT
REJECTED = ("won't fix", "won't do", "wontfix", "rejected")


def is_jira(ref):
    return ref.startswith("jira:")


def parse_ref(ref):
    """(owner/repo, number), or ("jira", "LT-123") for a Jira key."""
    j = JIRA_REF.match(ref)
    if j:
        return "jira", j.group(1)
    m = REF.match(ref)
    if not m:
        raise ValueError(f"bad upstream ref {ref!r} (want owner/repo#number or jira:KEY-123)")
    return m.group(1), int(m.group(2))


def contains(checkout, sha, run=subprocess.run):
    """True/False if `checkout` HEAD contains `sha`; None when git cannot say (no checkout, unknown commit)."""
    if not checkout or not sha:
        return None
    try:
        r = run(["git", "-C", str(checkout), "merge-base", "--is-ancestor", sha, "HEAD"],
                capture_output=True, text=True)
    except OSError:
        return None
    return {0: True, 1: False}.get(r.returncode)  # 128 = commit not present: undecided


def gh_json(args, run=subprocess.run):
    """Return (data, None) or (None, reason)."""
    try:
        r = run(["gh", *args], capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        return None, "gh is not installed"
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"gh failed to run ({type(e).__name__})"
    if r.returncode != 0:
        return None, f"gh unavailable or unauthenticated or offline: {(r.stderr or '').strip()[:120]}"
    try:
        return json.loads(r.stdout), None
    except ValueError:
        return None, "gh returned unparseable output"


def http_get_json(url, headers):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def jira_headers(env):
    """Auth headers from the env names the atlassian-skills skill documents, or None. Secrets are only read."""
    if not env.get("JIRA_URL"):
        return None
    if env.get("JIRA_PAT_TOKEN"):
        return {"Authorization": "Bearer " + env["JIRA_PAT_TOKEN"], "Accept": "application/json"}
    if env.get("JIRA_USERNAME") and env.get("JIRA_API_TOKEN"):
        cred = base64.b64encode(f"{env['JIRA_USERNAME']}:{env['JIRA_API_TOKEN']}".encode()).decode()
        return {"Authorization": "Basic " + cred, "Accept": "application/json"}
    return None


def resolve_jira(key, env, http):
    headers = jira_headers(env)
    if headers is None:
        return "pending", "jira unchecked (no JIRA_URL and credentials in the environment); treated as pending"
    url = f"{env['JIRA_URL'].rstrip('/')}/rest/api/2/issue/{key}?fields=status,resolution"
    try:
        fields = http(url, headers)["fields"]
    except Exception as e:  # network, auth, 404: never fail a run
        return "pending", f"jira unchecked ({type(e).__name__}); treated as pending"
    resolution = (fields.get("resolution") or {}).get("name")
    if not resolution:
        return "pending", f"open ({(fields.get('status') or {}).get('name', 'no status')})"
    if resolution.lower() in REJECTED:
        return "rejected", f"resolved {resolution}"
    return "issue-closed", f"resolved {resolution}"


def resolve(entry, machine_checkout=None, run=subprocess.run, env=None, http=http_get_json):
    repo, number = parse_ref(entry["ref"])
    if repo == "jira":
        return resolve_jira(number, os.environ if env is None else env, http)
    is_pr = entry["kind"] == "pr"
    engine = entry.get("affects") == "engine"
    if is_pr and engine and contains(machine_checkout, entry.get("head"), run):
        return "satisfied", f"build contains head {entry['head'][:7]}"
    if is_pr:
        data, why = gh_json(["pr", "view", str(number), "-R", repo, "--json", "state,mergeCommit"], run)
    else:
        data, why = gh_json(["issue", "view", str(number), "-R", repo, "--json", "state,stateReason"], run)
    if data is None:
        return "pending", f"{why}; treated as pending"
    state = data.get("state")
    if state == "OPEN":
        return "pending", "open"
    if is_pr and state == "MERGED":
        merge = (data.get("mergeCommit") or {}).get("oid")
        if engine and contains(machine_checkout, merge, run):
            return "satisfied", f"merged as {merge[:7]} and the build contains it"
        return "merged", f"merged as {merge[:7] if merge else 'unknown commit'}"
    if is_pr and state == "CLOSED":
        return "closed-unmerged", "closed without merging"
    if not is_pr and state == "CLOSED":
        return "issue-closed", f"closed ({data.get('stateReason') or 'no reason given'})"
    return "pending", f"unrecognised upstream state {state!r}"


def allows_never_shape(entries, run=subprocess.run, env=None, http=http_get_json):
    """FieldWorks-producible gate: a shape HCLoader never writes is allowed iff the fixture has an open
    `affects: loader` entry for sillsdev/FieldWorks (a GitHub PR/issue or a Jira LT key). Returns (allowed, note); note is non-empty when offline."""
    for e in entries or []:
        if e.get("affects") != "loader" or parse_ref(e["ref"])[0] not in ("sillsdev/FieldWorks", "jira"):
            continue
        state, reason = resolve(e, run=run, env=env, http=http)
        if state == "pending":
            return True, (f"{e['ref']} not confirmed open ({reason})" if reason != "open" else "")
    return False, ""
