# TARGETS.md — August Target Menu (researched Aug 14, 2026)

Pick ONE. Tier 1 is chosen for maximum odds given: 17 days, solo, fast
software engineer with Cursor+agent, CPU-first, new to the community.

The judging meta (from the organizers): released early > actually used >
well documented. Tools that the segmentation team and community pick up win.
Proven winning pattern from past monthly prizes: downloaders, viewers,
format converters, CPU-friendly alternatives, inference speedups, label QA —
i.e. INFRASTRUCTURE, not moonshots.

---

## TIER 1 — Tooling & data infrastructure (best odds, CPU-only, ship fast)

1. **Wishlist / VC3D "good first issues"** (check the live wishlist first —
   it exists precisely as a menu of prize-worthy ideas, and some VC3D issues
   are labeled for newcomers). Highest signal: the organizers literally
   asked for these. Pick the one closest to plain software engineering.

2. **Data ergonomics tool.** Precedent: a CLI download tool (phalanx) and
   chunk-access utilities won prizes. Gaps to probe in Discord: smarter
   ROI streaming, caching layers, dataset integrity checks beyond the
   existing audit tool, format conversion (Zarr <-> OME-Zarr <-> TIF)
   with windowing/8-bit options.

3. **Visualization / QA overlay tool.** Precedent: segment browser, scroll
   cell viewer, Khartes overlays all won. Gap pattern: "let a human quickly
   SEE whether X is good" (segmentation quality, ink-label alignment,
   mesh/volume agreement). Web-based (runs anywhere, easy for judges to
   try) or a VC3D panel contribution.

4. **Docs-as-code contribution.** Precedent: introductory notebooks and
   tutorial updates have won money. A polished, tested "zero to first ink
   prediction" or "zero to first VC3D segment" walkthrough notebook that
   ACTUALLY RUNS end-to-end — beginners flood in, docs rot fast, the team
   values this. Lowest glory, very real odds, builds reputation fast.

## TIER 2 — ML-adjacent (only if Tier 1 exploration reveals you're strong here)

5. **Inference speed/efficiency.** Precedent: ink-detection inference
   speedups won a prize. Profile an existing open ink model; make it
   faster/cheaper (batching, mixed precision, tiling, ONNX) with identical
   outputs. Measurable = judgeable.

6. **Label quality tooling.** The community's current focus includes better
   ink labels and better segmentation inputs. A tool that finds label
   errors/misalignments or maps labels between segment versions
   (precedent: segment-to-segment label mapping won) is high-leverage.

## TIER 3 — DO NOT ATTEMPT IN AUGUST (note them for later)

- Full automated segmentation / unrolling improvements to the neural tracer
  or "lasagna" optimizer (the real frontier — study it for Sept/Oct).
- Anything touching the Grand Prize / First Letters directly.
- New ink-detection architectures trained from scratch (GPU-hungry,
  veterans are far ahead; revisit after the baseline teaches you the data).

---

## Selection procedure (do this, in order)

1. Read the live wishlist + open-problems page. Shortlist 3 items.
2. Search Discord history for each: has someone built it? is someone
   building it now? what do people complain about weekly?
3. Kill 2. Announce the survivor in Discord ("I'm building X, planning to
   ship a first version by ~Aug 22 — feedback welcome"). Announcing does
   three things: claims the territory, gets early guidance, and starts the
   "actually gets used" clock.
4. Build minimal working version -> ship -> iterate in public -> submit.
