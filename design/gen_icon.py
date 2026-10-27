#!/usr/bin/env python3
"""生成插件图标：暗金底 + 双层金框 + 思源宋体 Heavy「金」字，512x512 PNG。

字形不按基线、而按墨迹包围盒居中；思源宋体 CN Heavy 自带足够字重，不再叠描边，
以保留横细竖粗和起收笔锋。

依赖：pillow。字体需先安装（Source Han Serif CN Heavy）：
    python3 design/gen_icon.py                 # 默认读 ~/Library/Fonts/SourceHanSerifCN-Heavy.otf
    python3 design/gen_icon.py /path/to.otf
输出：assets/icon.png（同时供 paseo-plugin.json 的 icon 字段使用）
"""

import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024          # 先大后缩，保证边缘平滑
OUT = 512
BG = "#17150f"       # 暗色端页面底
GOLD = "#c8a63f"     # 暗色端强调金
GLYPH = "#d9c06b"    # 暗色端焦点环金，比框略亮
INK = 620            # 字形墨迹目标宽度（画布 1024）
FONT_SIZE = 760      # 先大字号渲染，再缩放到目标宽度

DEFAULT_FONT = pathlib.Path.home() / "Library/Fonts/SourceHanSerifCN-Heavy.otf"


def main() -> None:
    font_path = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_FONT
    if not font_path.exists():
        sys.exit(f"找不到字体：{font_path}\n先安装思源宋体 CN Heavy，或把字体路径作为参数传入。")
    font = ImageFont.truetype(str(font_path), FONT_SIZE)

    # 字形画在透明层上，再裁到墨迹包围盒
    layer = Image.new("RGBA", (SIZE * 2, SIZE * 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((SIZE, SIZE), "金", font=font, fill=GLYPH, anchor="mm")
    glyph = layer.crop(layer.getbbox())
    glyph = glyph.resize((INK, round(glyph.height * INK / glyph.width)), Image.LANCZOS)

    img = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    # 双层边框：外粗内细，内框压暗，避免抢字形
    draw.rounded_rectangle([44, 44, SIZE - 44, SIZE - 44], radius=120, outline=GOLD, width=30)
    inner = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(inner).rounded_rectangle(
        [110, 110, SIZE - 110, SIZE - 110], radius=88, outline=GOLD, width=12
    )
    inner.putalpha(inner.split()[3].point(lambda a: int(a * 0.6)))
    img = Image.alpha_composite(img, inner)

    img.alpha_composite(glyph, ((SIZE - glyph.width) // 2, (SIZE - glyph.height) // 2))

    flat = Image.new("RGB", (SIZE, SIZE), BG)
    flat.paste(img, (0, 0), img)
    flat = flat.resize((OUT, OUT), Image.LANCZOS)

    out = pathlib.Path(__file__).parent.parent / "assets/icon.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    flat.save(out)
    print(out)


if __name__ == "__main__":
    main()
