#!/bin/bash
# 把 HTML 用 headless Chrome 截成 PNG。
# 用法：render.sh <html 檔> <輸出 png> <寬> <高> [#hash]
# 圖片、字體一律用「相對路徑」放在 html 同資料夾——絕對路徑含中文時 Chrome 會讀不到。
set -e
HTML="$1"; OUT="$2"; W="$3"; H="$4"; HASH="$5"
DIR="$(cd "$(dirname "$HTML")" && pwd)"
OUTDIR="$(cd "$(dirname "$OUT")" && pwd)"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size="$W,$H" --virtual-time-budget=3000 \
  --screenshot="$OUTDIR/$(basename "$OUT")" "file://$DIR/$(basename "$HTML")$HASH" 2>/dev/null
echo "→ $OUTDIR/$(basename "$OUT")"
