#!/usr/bin/env bash
# Check whether the Kaggle run has finished.
#   ./tools/status.sh
set -euo pipefail
cd "$(dirname "$0")/.."

KAGGLE="${KAGGLE_BIN:-.venv/bin/kaggle}"
ID="$(.venv/bin/python -c "import json;print(json.load(open('kaggle/kernel-metadata.json'))['id'])")"

"$KAGGLE" kernels status "$ID"
