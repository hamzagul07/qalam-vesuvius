# CLAUDE.md — Agent Briefing: Vesuvius Challenge Campaign

You are the coding agent for a solo, fast-moving contributor entering the
Vesuvius Challenge (scrollprize.org) with the goal of shipping one open-source
progress-prize submission before Aug 31 (monthly deadline, 11:59pm Pacific).

## Domain context (read once, remember always)

- The Herculaneum scrolls are carbonized papyrus, scanned by X-ray micro-CT
  into huge 3D volumes. Reading them = three sub-problems:
  1. **Segmentation**: trace the crumpled papyrus sheet surface through the
     3D volume (semi-automated today; full automation is THE open problem).
  2. **Flattening/rendering**: unroll the traced surface into flat images.
  3. **Ink detection**: ML models find carbon ink on carbon papyrus from
     subtle texture; trained on fragments with visible ink, applied inside
     sealed scrolls.
- Key data formats: newer volumes are **OME-Zarr** (chunked, multi-resolution
  — stream chunks, never bulk-download); older releases are TIF stacks;
  segment meshes use **tifxyz**; rendered segments come with layer TIFs;
  ink labels are binary masks aligned to renders.
- The scan resolution is micrometers; volumes are terabyte-scale. ALWAYS work
  on small subvolumes / single segments / low-res pyramid levels first.

## Key resources (ground truth over memory — fetch/read these, do not guess)

- scrollprize.org/data — data agreement + access instructions
- scrollprize.org/2026_open_problems — current technical frontier, incl. VC3D
  internals (surface prediction volumes -> meshes, normal grids, neural
  tracer, the "lasagna" optimization approach)
- scrollprize.org/prizes — prize rules, submission form, wishlist link
- scrollprize.org/community_projects — existing tools (do NOT duplicate them;
  extend or interoperate)
- github.com/ScrollPrize/villa — the official monorepo (VC3D lives here)
- `pip install vesuvius` — official Python data-access library
- Community tools worth knowing: vesuvius-phalanx (CLI downloads), Khartes
  (manual meshing), segment browser (web viewing), vesuvius-render
  (CPU rendering), vesuvius-gui.

## Working rules for you, the agent

1. **Small first.** Every pipeline is proven on a tiny crop/subvolume before
   scaling. If a script would download >2 GB, stop and propose an
  alternative (ROI streaming, lower pyramid level).
2. **Reproducible.** Every experiment: fixed seed, config block at top of
   file, one-command run, results appended to EXPERIMENTS.md with date,
   command, and outcome (1–3 lines).
3. **Ship-shaped.** Anything intended for submission gets: README with
   install + usage + before/after images, MIT/Apache license, example data
   or clear pointers, and a short demo script. Documentation is a judging
   criterion, treat it as code.
4. **Don't reinvent.** Before building, check community_projects and the
   villa monorepo. The winning pattern is filling gaps BETWEEN existing
   tools (converters, viewers, speedups, missing UX) — not duplicating them.
5. **Compute honesty.** Training runs go to Kaggle/Colab notebooks (free
   GPU); local machine is for CPU tooling. Structure code so the same file
   runs in both places (no hardcoded paths outside the config block).
6. **No meta-work.** Refuse to build productivity dashboards, personal
   trackers, or "systems for working." All effort goes into scroll tooling,
   data, or models.
7. **Verify against docs.** Data layouts and tool interfaces change; when
   code touches server paths or formats, check the current docs/tutorials
   rather than assuming.

## Definition of done (August)

- [ ] Public GitHub repo, documented as in rule 3
- [ ] Posted in Discord early enough to gather feedback and iterate
- [ ] Official monthly progress-prize submission form completed before
      Aug 31, 11:59pm Pacific
- [ ] EXPERIMENTS.md tells the honest story of how it was built
