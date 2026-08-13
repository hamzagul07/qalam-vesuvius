#!/usr/bin/env bash
# Pull the finished run's outputs into out/kaggle_run/ and log it.
#   ./tools/pull.sh
# Appends one row to EXPERIMENTS.md: date | kernel version | val_dice.
set -euo pipefail
cd "$(dirname "$0")/.."

KAGGLE="${KAGGLE_BIN:-.venv/bin/kaggle}"
PY=".venv/bin/python"
ID="$($PY -c "import json;print(json.load(open('kaggle/kernel-metadata.json'))['id'])")"
DEST="out/kaggle_run"

mkdir -p "$DEST"
echo "pulling $ID -> $DEST"
"$KAGGLE" kernels output "$ID" -p "$DEST"

# Parse the log and append a row to EXPERIMENTS.md.
"$PY" - "$DEST" <<'PY'
import datetime, pathlib, re, sys

dest = pathlib.Path(sys.argv[1])
root = pathlib.Path.cwd()

# Kaggle writes the run log next to the outputs; take the newest .log
logs = sorted(dest.glob("*.log"), key=lambda p: p.stat().st_mtime)
text = ""
if logs:
    text = logs[-1].read_text(errors="replace")
    # the log is JSON records ({"stream_name":..,"data":..}) on newer kernels
    text = "\n".join(re.findall(r'"data"\s*:\s*"((?:[^"\\]|\\.)*)"', text)) or text
    text = text.encode().decode("unicode_escape", errors="replace")

dices = [float(m) for m in re.findall(r"val_dice=([0-9.]+)", text)]
best = f"{max(dices):.4f} (best of {len(dices)} epochs)" if dices else "not found in log"

ver = "unknown"
vf = dest / ".last_version"
if vf.exists():
    ver = vf.read_text().strip() or "unknown"

row = f"| {datetime.date.today().isoformat()} | `./tools/pull.sh` (kernel v{ver}) | val_dice={best} |\n"

exp = root / "EXPERIMENTS.md"
lines = exp.read_text().splitlines(keepends=True)
# Insert after the last real table row, staying above the trailing HTML
# comment (which holds a "| YYYY-MM-DD |" template row we must not append to).
end = next((i for i, l in enumerate(lines) if l.lstrip().startswith("<!--")), len(lines))
rows = [i for i, l in enumerate(lines[:end]) if l.startswith("| ")]
lines.insert(rows[-1] + 1 if rows else end, row)
exp.write_text("".join(lines))

print(f"\nlogged to EXPERIMENTS.md: kernel v{ver}, val_dice={best}")
if not logs:
    print("NOTE: no .log in the output — has the run finished? ./tools/status.sh")
PY

echo
echo "outputs in $DEST — open $DEST/out/prediction.png"
