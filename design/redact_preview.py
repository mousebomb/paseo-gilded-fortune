#!/usr/bin/env python3
"""给 Paseo 实拍截图打码，产出 listing 用预览图。

用法：
    python3 design/redact_preview.py <原始截图.png> <输出.png>

原始截图用窗口级抓取（只含 Paseo 窗口，不含其他应用）。当前唯一需要遮挡的是
侧栏底部的主机名；若换了机器或截图内容不同，改下面 BOX 即可。
原始截图不入库。
"""

import pathlib
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 主机名所在区域（按 1366x1070 的窗口截图坐标）
BOX = dict(x=30, y=618, w=232, h=34)
SIZE = (1366, 1070)

HTML = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  html,body{{margin:0;padding:0;background:#000;}}
  .wrap{{position:relative;width:{w}px;height:{h}px;}}
  img{{display:block;width:{w}px;height:{h}px;}}
  .redact{{
    position:absolute;left:{x}px;top:{y}px;width:{bw}px;height:{bh}px;
    backdrop-filter:blur(7px);
    -webkit-backdrop-filter:blur(7px);
    border-radius:6px;
  }}
</style></head>
<body><div class="wrap">
  <img src="file://{src}">
  <div class="redact"></div>
</div></body></html>
"""


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    page = src.with_suffix(".redact.html")
    w, h = SIZE
    page.write_text(
        HTML.format(w=w, h=h, src=src, x=BOX["x"], y=BOX["y"], bw=BOX["w"], bh=BOX["h"]),
        encoding="utf-8",
    )
    subprocess.run(
        [
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--allow-file-access-from-files",
            f"--window-size={w},{h}",
            f"--screenshot={out}",
            f"file://{page}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    page.unlink(missing_ok=True)
    print(out)


if __name__ == "__main__":
    main()
