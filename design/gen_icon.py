#!/usr/bin/env python3
"""生成插件图标：暗金底 + 金色「金」字，512x512 PNG。

改色/改字后重跑：
    python3 design/gen_icon.py
"""

import pathlib
import subprocess

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SIZE = 512
BG = "#17150f"
GLYPH = "#c8a63f"
RING = "#3a2f18"

SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
  <rect width="{SIZE}" height="{SIZE}" fill="{BG}"/>
  <rect x="40" y="40" width="{SIZE-80}" height="{SIZE-80}" rx="96" fill="none"
        stroke="{RING}" stroke-width="6"/>
  <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central"
        font-family="Songti SC, STSong, Noto Serif SC, serif"
        font-size="272" font-weight="700" fill="{GLYPH}" dy="8">金</text>
</svg>
"""

here = pathlib.Path(__file__).parent
svg_path = here / "icon.svg"
png_path = here / "icon.png"
svg_path.write_text(SVG, encoding="utf-8")

subprocess.run(
    [
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--default-background-color=00000000",
        f"--window-size={SIZE},{SIZE}",
        f"--screenshot={png_path}",
        f"file://{svg_path}",
    ],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
print(png_path)
