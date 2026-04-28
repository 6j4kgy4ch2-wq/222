#!/usr/bin/env bash
set -euo pipefail

OUTPUT_NAME=${1:-financial-eye-code.zip}
ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
OUTPUT_PATH="$ROOT_DIR/$OUTPUT_NAME"

rm -f "$OUTPUT_PATH"

cd "$ROOT_DIR"
zip -r "$OUTPUT_PATH" . \
  -x ".git/*" \
  -x "*.zip" \
  -x "backend/uploads/*" \
  -x "__pycache__/*" \
  -x "*.pyc"

echo "打包完成: $OUTPUT_PATH"
