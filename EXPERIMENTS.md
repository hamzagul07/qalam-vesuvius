# EXPERIMENTS.md

The honest log. One row per experiment — including the ones that failed.
Rule: fixed seed, config block at the top of the file, one command to run.

Format: `date | command | result (1–3 lines)`

---

| date | command | result |
|---|---|---|
| 2026-08-14 | `git init` + Phase 0 scaffolding | Repo initialised; `recon/`, `tools/`, `notebooks/`, `baseline/` created. No data touched yet. |
| 2026-08-14 | recon sweep: `scrollprize.org/{prizes,2026_open_problems,community_projects,data}` + `gh issue/pr list --repo ScrollPrize/villa` | 37 open issues, 3 labelled `help wanted` (= "Good candidate for a Progress Prize"), ~50 open community PRs. Findings kept in local working notes. |
| 2026-08-14 | `python3.13 -m venv .venv && pip install vesuvius` | See PROGRESS.md for the outcome and any blockers. |
| 2026-08-14 | `python tools/smoke_test.py` | First real data touched: streams one small ROI from the public S3 bucket and writes `out/smoke_*.png`. |
| 2026-08-13 | baseline run by hand in Kaggle notebook `notebook340f204c0e` (T4, fragment 1, 8 epochs) | **Gate B cleared.** 8181x6330, 2322 train / 144 val patches. val_dice by epoch: 0, 0, 0, 0, 0, 0.1111, **0.3333**, 0.2222; val_loss fell 0.396 → 0.136 throughout. Wrote `prediction.png`. Two findings: (1) `data_dir` had to be edited — this kernel mounts the competition under `/kaggle/input/competitions/...`, not the classic path; now auto-detected. (2) every val_dice is an exact multiple of 1/9 (144 patches / batch 16 = 9 batches), so the metric is swinging on whole batches and is a weak signal at this validation size. |

<!--
Append new rows below. Template:

| YYYY-MM-DD | `exact command you ran` | what happened, what it means, what you changed next |
-->
