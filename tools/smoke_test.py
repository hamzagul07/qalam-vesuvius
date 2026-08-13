"""
GATE A SMOKE TEST — prove we can stream real scroll data and see it.

Streams ONE small, low-resolution region out of the public Vesuvius S3 bucket
and writes preview PNGs. Nothing is bulk-downloaded: at the default settings
this pulls single-digit megabytes, not gigabytes.

Why PHerc0009B level 4: the multi-resolution pyramid for this fragment is

    level 0: (9598, 7837, 7837) uint8   ~ 589 GB   <- never touch casually
    level 4: ( 600,  490,  490) uint8   ~ 144 MB   <- whole volume is small
    level 5: ( 300,  245,  245) uint8   ~  18 MB

so a 256^3 ROI at level 4 is ~16 MB of voxels, and the three preview slices
we save are a few hundred KB each.

USAGE
    python tools/smoke_test.py                 # default ROI, level 4
    python tools/smoke_test.py --level 5       # even smaller
    python tools/smoke_test.py --size 128      # smaller cube

FIRST RUN ONLY — accept the data license (no account, no credentials):
    vesuvius.accept_terms --yes

Data access needs NO credentials. s3://vesuvius-challenge-open-data/ is an AWS
Open Data bucket read anonymously via Volume(..., anon=True); there is no data
agreement form and no keys to configure. Browse it at
https://scrollprize.org/data_browser

This follows the official quick-start:
https://github.com/ScrollPrize/open-data -> examples/get-to-know-a-dataset.ipynb
(same Volume(type="zarr", path=..., anon=True) call, same PHerc0009B volume;
this script differs only in reading a low-resolution pyramid level instead of
level 0, and in writing PNGs instead of plotting inline).
"""

import argparse
import os
import random

import numpy as np

# ----------------------------------------------------------------------------
# CONFIG — the only block you should need to touch
# ----------------------------------------------------------------------------
CFG = {
    # Fragment PHerc. 0009B, 8.640um masked scan. Trailing slash matters:
    # the pyramid level is appended to this to form the array path.
    "volume_url": (
        "s3://vesuvius-challenge-open-data/PHerc0009B/volumes/"
        "20250521125136-8.640um-1.2m-116keV-masked.zarr/"
    ),
    "level": 4,          # pyramid level; HIGHER number = LOWER resolution
    "roi_size": 256,     # cube edge in voxels at the chosen level
    "roi_center_frac": (0.5, 0.5, 0.5),  # ROI centre as a fraction of (z, y, x)
    "out_dir": "out",
    "seed": 42,
    "max_mb": 64,        # refuse to stream more than this; guards against typos
}

random.seed(CFG["seed"])
np.random.seed(CFG["seed"])


def _to_png(arr):
    """Contrast-stretch a 2D array to uint8 using robust percentiles."""
    arr = arr.astype(np.float32)
    lo, hi = np.percentile(arr, [1, 99])
    if hi <= lo:                       # flat slice (all air, or all mask)
        return np.zeros(arr.shape, dtype=np.uint8)
    return (np.clip((arr - lo) / (hi - lo), 0, 1) * 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--level", type=int, default=CFG["level"])
    ap.add_argument("--size", type=int, default=CFG["roi_size"])
    ap.add_argument("--out-dir", default=CFG["out_dir"])
    args = ap.parse_args()

    from PIL import Image
    from vesuvius import Volume

    os.makedirs(args.out_dir, exist_ok=True)
    path = f"{CFG['volume_url']}{args.level}"

    print(f"opening  {path}")
    vol = Volume(type="zarr", path=path, anon=True)
    shape = vol.shape()
    print(f"level {args.level}: shape={shape} dtype={vol.dtype}")

    # ---- pick a centred ROI, clamped to the array bounds --------------------
    size = min(args.size, *shape)
    starts = []
    for extent, frac in zip(shape, CFG["roi_center_frac"]):
        s = int(extent * frac) - size // 2
        starts.append(max(0, min(s, extent - size)))
    z0, y0, x0 = starts

    est_mb = (size ** 3 * np.dtype(vol.dtype).itemsize) / 1e6
    if est_mb > CFG["max_mb"]:
        raise SystemExit(
            f"refusing to stream {est_mb:.0f} MB (max_mb={CFG['max_mb']}). "
            f"Use a higher --level or a smaller --size."
        )
    print(f"streaming ROI z={z0}:{z0+size} y={y0}:{y0+size} x={x0}:{x0+size} "
          f"(~{est_mb:.1f} MB)")

    roi = vol[z0:z0 + size, y0:y0 + size, x0:x0 + size]
    roi = np.asarray(roi)
    print(f"got {roi.shape} {roi.dtype}  "
          f"min={roi.min()} max={roi.max()} mean={roi.mean():.1f}")

    # ---- save three orthogonal previews through the ROI centre -------------
    mid = size // 2
    planes = {
        "xy": roi[mid, :, :],
        "xz": roi[:, mid, :],
        "yz": roi[:, :, mid],
    }
    written = []
    for name, plane in planes.items():
        out_path = os.path.join(args.out_dir, f"smoke_L{args.level}_{name}.png")
        Image.fromarray(_to_png(plane)).save(out_path)
        written.append(out_path)

    # ---- and one contact sheet so a human can eyeball it in a single file ---
    sheet = np.concatenate([_to_png(p) for p in planes.values()], axis=1)
    sheet_path = os.path.join(args.out_dir, f"smoke_L{args.level}_triptych.png")
    Image.fromarray(sheet).save(sheet_path)
    written.append(sheet_path)

    print("\nwrote:")
    for w in written:
        print(f"  {w}")
    print("\nOPEN THE TRIPTYCH. Those concentric arcs are the rolled papyrus "
          "sheets of a carbonised Herculaneum scroll fragment. Gate A cleared.")


if __name__ == "__main__":
    main()
