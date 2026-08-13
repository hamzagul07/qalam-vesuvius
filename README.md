# Qalam — Vesuvius Challenge campaign

**Vesuvius August campaign — battle plan**

Mission: ship one real, open-source contribution to the Vesuvius Challenge
before the monthly deadline (Aug 31, 11:59pm Pacific). Deadline is ~17 days away.

Honest framing: nobody can hand you a pre-made winner. Progress prizes go to
work that the community actually uses. This kit removes every excuse between
you and the loop: touch data -> feel pain -> ship fix -> submit.

---

## 0. Accounts to create (do all four immediately)

1. **Data access** — go to scrollprize.org -> Data -> accept the data agreement
   form. You receive credentials for the data server. Without this you cannot
   touch scroll data.
2. **Discord** — the invite is on scrollprize.org. Introduce yourself in one
   line. Read the segmentation/ink channels daily: this is the live map of
   where the pain (= prize opportunity) is.
3. **GitHub** — your public workshop. Everything you build goes here, public,
   from day one.
4. **Kaggle** — free GPU (~30h/week) and home of the practice dataset
   `vesuvius-challenge-ink-detection`.

## 1. Where everything runs (your exact question, answered)

- **Cursor (your setup)** = the workshop. Open THIS folder in Cursor.
  `CLAUDE.md` briefs your agent on the whole domain automatically.
- **Your laptop CPU** = enough for tooling work (converters, viewers, scripts,
  VC3D-adjacent utilities). This is the lane chosen for August — deliberately.
- **Kaggle / Colab GPU** = where the baseline trains. Your laptop does NOT
  train ink models; the free cloud GPUs do.
- **VC3D** (the community's main segmentation tool) = runs via Docker, Linux,
  or WSL if you are on Windows.
- **Browser (Neuroglancer links on each scroll's Data Browser page)** =
  instant scroll exploration with zero download. Start looking at data here
  within the first hour.
- **vesuvius Python library** = programmatic data access in a few lines;
  streams small pieces instead of downloading terabytes.

## 2. Order of operations (gates, not dates)

- **Gate A — Contact.** Accounts made. Opened a scroll in Neuroglancer.
  Pulled a small subvolume with the `vesuvius` library. You have SEEN the data.
- **Gate B — Rite of passage.** Run `baseline/train_ink_baseline.py` on Kaggle
  with the fragment dataset. Output: your first ink image. Post it. This is
  practice, NOT your submission.
- **Gate C — Feel the pain.** Do the official segmentation tutorial with VC3D
  on a small region, manually. Note every step that is slow, confusing, or
  repetitive. Cross-reference the wishlist + open problems page
  (scrollprize.org/2026_open_problems). Pick ONE target from `TARGETS.md`.
- **Gate D — Build.** Small scope. Working > ambitious. Clean README with
  before/after images, install instructions, a demo GIF.
- **Gate E — Ship early, then improve in public.** Release the first working
  version DAYS before the deadline, post it in Discord, respond to feedback,
  iterate. Then fill the official submission form before Aug 31.

## 3. What the judges reward (this is the meta-game)

The organizers state their criteria openly. Winning submissions:
- are released/open-sourced EARLY in the month (tools released early actually
  get used before judging);
- ACTUALLY GET USED (community questions, bug reports, feature requests are
  the signal — this is why Discord presence matters);
- are WELL DOCUMENTED (walkthroughs, images, tutorials).

Strategy implication: a modest tool shipped on Aug 22 with great docs beats a
brilliant tool shipped silently on Aug 31.

## 4. Prize reality check

- Monthly pool: awards at ~$20k / $10k / $5k / $2.5k / $1k / $500 levels,
  multiple winners per month, plus $20,000 guaranteed for best of month.
- Your realistic August outcome: a real submission + your name entering the
  room. Possible outcome: a small prize ($500–$2.5k tier has gone to focused
  single tools before). September/October: genuine winning shots.

## 5. Operating rules

1. One target. The kit lists many; you build ONE.
2. Everything public from hour one.
3. Stuck > 45 min after real effort -> ask in Discord with a screenshot and
   what you tried. Fast people stay fast by asking well.
4. No meta-productivity systems. Automate the SCROLL work, never "being
   productive."
5. Log every experiment in EXPERIMENTS.md (your agent is instructed to do
   this).
