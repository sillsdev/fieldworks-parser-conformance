# cal-work-cap

Two word lists, two caps. Read this before running either.

| file | run with | expected |
|---|---|---|
| `words.txt` (6 words) | any cap, default is fine | every word finishes below 125,000 work steps; `words.yaml` has the oracle's analyses |
| `cap-words.work-cap-200000.txt` (2 words) | **`--work-cap 200000`, always** | status `CAP` at about 212,500 work steps and about 150M cost each; no analyses expected (`cap-words.work-cap-200000.yaml`) |

```
pangloss batch grammar.xml cap-words.work-cap-200000.txt out.tsv --cost-column --work-columns --work-cap 200000
```

At the default cap the two cap words do finish (measured: `xxmiloy` 1.78M steps, 1.57G cost, 26.6 MB; `xxxmilmy` 14.3M
steps, 9.81G cost, 165 MB) but they cost 10 to 60 times more than at the reduced cap, which is too much for a profiler.
`MEMCAP` is not expected for either. The grammar can still run away on other words of the same shape (`x^20 milm y^6`
peaked at 25.9 GB), so do not add words here without running them under `ulimit -v` and `timeout`. See `../README.md`.
