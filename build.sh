#!/usr/bin/env bash
set -o errexit

# ── 中文字体：避免 Chromium 生成 Type3 字体 ──
FONT_DIR="static/fonts"
mkdir -p "$FONT_DIR"

if [ "$(uname)" = "Linux" ]; then
  # Linux（Railway）：安装系统字体包
  apt-get install -y fonts-noto-cjk 2>/dev/null || true
  # 将系统字体软链到 static/fonts
  for WEIGHT in Regular Bold; do
    SRC=$(find /usr/share/fonts -name "NotoSansCJK*${WEIGHT}*" -o -name "NotoSansSC*${WEIGHT}*" 2>/dev/null | head -1)
    [ -n "$SRC" ] && cp "$SRC" "$FONT_DIR/NotoSansSC-${WEIGHT}.ttf" && echo "复制字体: $SRC"
  done
fi

pip install -r requirements.txt
playwright install --with-deps chromium
