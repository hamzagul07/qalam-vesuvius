# PROGRESS.md

One line per step. Newest at the bottom. Blockers logged honestly.

## 2026-08-14 — Phase 0: foundation + reconnaissance

- `git init` in `qalam-vesuvius`; repo is local-only so far (no remote yet).
- Created `.gitignore` (python, `data/`, `out/`, `.env`, model weights, `.DS_Store`).
- Created MIT `LICENSE`. **BLOCKER (needs you):** copyright line still reads
  `<YOUR NAME>` — I will not guess your legal name. One-line fix before the repo goes public.
- Created `EXPERIMENTS.md` (date | command | result) and this file.
- Created `recon/`, `tools/`, `notebooks/`; moved `train_ink_baseline.py` into `baseline/`
  to match the path the briefing and README refer to (`baseline/train_ink_baseline.py`).
- Recon sweep completed with web access — no URLs needed from you. Sources read:
  `scrollprize.org/prizes`, `/2026_open_problems`, `/community_projects`, `/data`,
  `/winners`, the `ScrollPrize/villa` README + **CONTRIBUTING.md**, all 37 open issues,
  ~50 open PRs and the last 40 merged PRs.
- **Key correction to the kit's assumptions:** scroll data is now **public and anonymous**
  (AWS Open Data, `s3://vesuvius-challenge-open-data/`, browsable at
  `scrollprize.org/data_browser`). There is no data-agreement form to fill in and no
  credentials are issued. The only gate is `vesuvius.accept_terms --yes`.
  README.md step 0.1 ("You receive credentials for the data server") is out of date —
  independently confirmed by the user mid-session.
- **Key strategic finding:** the `help wanted` label on villa is officially defined as
  *"Good candidate for a Progress Prize"*. Only 3 issues carry it; one (#192) is also
  `good first issue`. Full analysis in [recon/RECON.md](recon/RECON.md).
- Wrote `recon/RECON.md`: per-candidate existing tools, demand evidence, S/M/L sizing,
  risks, and a top-3 ranked shortlist with a v1 spec for each.
- `uv venv --python 3.12 .venv` + `uv pip install vesuvius pillow matplotlib` → **vesuvius 0.2.4**.
  (System python is 3.9.6, too old; `uv` is what villa's own CONTRIBUTING recommends.)
- `vesuvius.accept_terms --yes` → agreement saved. No account required.
- Wrote `tools/smoke_test.py`, following the official quick-start
  (`ScrollPrize/open-data` → `examples/get-to-know-a-dataset.ipynb`): same
  `Volume(type="zarr", path=..., anon=True)` call, same PHerc0009B volume, but reading a
  low-resolution pyramid level instead of level 0.
- No `.env` / credential scaffolding: access is anonymous, so there is nothing to configure.
  (`.env` stays in `.gitignore` purely as a safety net.)
- **GATE A CLEARED.** `python tools/smoke_test.py` streamed a 256³ ROI (~16.8 MB) from
  PHerc. 0009B at pyramid level 4 and wrote `out/smoke_L4_triptych.png`. Verified visually:
  papyrus fibre texture and the fragment cross-section are clearly resolved. Real data,
  real pixels, no bulk download.
- Wrote `notebooks/baseline_kaggle.ipynb` — a faithful cell-split of
  `baseline/train_ink_baseline.py` with the training logic unchanged.

- Kaggle bridge: CLI 2.2.4 authed as `hamzagulhassan` via `~/.kaggle/access_token` (KGAT style,
  mode 600). `kaggle/` holds the pushable kernel; `tools/{push,status,pull}.sh` drive it.
  Competition rules for `vesuvius-challenge-ink-detection` were already accepted.
- **PUBLISHED:** https://github.com/hamzagul07/qalam-vesuvius (public, `main`, 3 commits).
  LICENSE now carries the real copyright holder. Pre-flight secret scan clean: no `.env*`,
  `access_token`, `kaggle.json` or `KGAT_` string in any commit, and the published tree was
  re-fetched from the API and re-audited after the push.

### Open blockers

1. ~~LICENSE placeholder~~ — resolved, set to Hamza Gul Hassan.
2. No GitHub remote yet — repo is not public. Needs your call on the repo name.
3. Baseline notebook is **untested**: it needs a Kaggle GPU session with the
   `vesuvius-challenge-ink-detection` dataset attached, which I cannot run from here.
