#!/usr/bin/env bash
# Push the baseline kernel to Kaggle and start a GPU run.
#   ./tools/push.sh
# Auth comes from ~/.kaggle/access_token — nothing to pass, nothing to export.
set -euo pipefail
cd "$(dirname "$0")/.."

KAGGLE="${KAGGLE_BIN:-.venv/bin/kaggle}"

# baseline/ is the single source of truth; kaggle/ is just the push payload.
cp baseline/train_ink_baseline.py kaggle/train_ink_baseline.py

echo "pushing kaggle/ ..."
out="$("$KAGGLE" kernels push -p kaggle 2>&1)"
echo "$out"

# Remember the version so pull.sh can label the EXPERIMENTS.md row.
ver="$(printf '%s' "$out" | grep -oE 'version [0-9]+' | grep -oE '[0-9]+' | tail -1 || true)"
if [ -n "$ver" ]; then
  mkdir -p out/kaggle_run
  printf '%s' "$ver" > out/kaggle_run/.last_version
  echo "recorded version $ver"
fi

echo
echo "now: ./tools/status.sh   (wait for 'complete', then ./tools/pull.sh)"
