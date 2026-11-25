#!/usr/bin/env python3
"""Resolve a fixture's `upstream` entries (PROTOCOL.md section 12, ADR 0001). Standard library only.

resolve(entry, machine_checkout=None) -> (state, reason). States:
  satisfied        engine/pr: the checkout contains the PR head (or its merge commit)
  pending          PR or issue still open, not in the checkout, or gh could not say (reason says which)
  merged           PR merged upstream: re-point citations to the merge commit
  closed-unmerged  PR closed without merging: needs a human decision
  issue-closed     issue closed: retire or re-check
Git ancestry decides first (no network); gh is asked only when git cannot decide. A missing, unauthenticated or
offline gh yields `pending` with the reason; this module never raises for a network or tooling failure.
"""
import json
import re
import subprocess

REF = re.compile(r"^([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#([0-9]+)$")


def parse_ref(ref):
    m = REF.match(ref)
    if not m:
        raise ValueError(f"bad upstream ref {ref!r} (want owner/repo#number)")
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


def resolve(entry, machine_checkout=None, run=subprocess.run):
    repo, number = parse_ref(entry["ref"])
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


def allows_never_shape(entries, run=subprocess.run):
    """FieldWorks-producible gate: a shape HCLoader never writes is allowed iff the fixture has an open
    `affects: loader` entry for sillsdev/FieldWorks. Returns (allowed, note); note is non-empty when offline."""
    for e in entries or []:
        if e.get("affects") != "loader" or parse_ref(e["ref"])[0] != "sillsdev/FieldWorks":
            continue
        state, reason = resolve(e, run=run)
        if state == "pending":
            return True, (f"{e['ref']} not confirmed open ({reason})" if reason != "open" else "")
    return False, ""
