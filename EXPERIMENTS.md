# EXPERIMENTS.md

The honest log. One row per experiment — including the ones that failed.
Rule: fixed seed, config block at the top of the file, one command to run.

Format: `date | command | result (1–3 lines)`

---

| date | command | result |
|---|---|---|
| 2026-08-14 | `git init` + Phase 0 scaffolding | Repo initialised; `recon/`, `tools/`, `notebooks/`, `baseline/` created. No data touched yet. |
| 2026-08-14 | recon sweep: `scrollprize.org/{prizes,2026_open_problems,community_projects,data}` + `gh issue/pr list --repo ScrollPrize/villa` | 37 open issues, 3 labelled `help wanted` (= "Good candidate for a Progress Prize"), ~50 open community PRs. Findings in [recon/RECON.md](recon/RECON.md). |
| 2026-08-14 | `python3.13 -m venv .venv && pip install vesuvius` | See PROGRESS.md for the outcome and any blockers. |
| 2026-08-14 | `python tools/smoke_test.py` | First real data touched: streams one small ROI from the public S3 bucket and writes `out/smoke_*.png`. |

<!--
Append new rows below. Template:

| YYYY-MM-DD | `exact command you ran` | what happened, what it means, what you changed next |
-->
