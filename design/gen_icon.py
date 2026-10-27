#!/usr/bin/env python3
"""生成插件图标：暗金底 + 双层金框 + 文津宋体「金」字，512x512 PNG。

字形用文津宋体（WenJinMincho，SIL OFL），字形按墨迹包围盒精确居中（不是按基线），
再用描边加粗，保留宋体的横细竖粗与起收笔锋。

依赖：pillow。字体需先安装或指定路径：
    python3 design/gen_icon.py                 # 默认读 ~/Library/Fonts/WenJinMinchoP0-Regular.ttf
    python3 design/gen_icon.py /path/to.ttf
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
STROKE = 10

DEFAULT_FONT = pathlib.Path.home() / "Library/Fonts/WenJinMinchoP0-Regular.ttf"


def load_font(path: pathlib.Path) -> ImageFont.FreeTypeFont:
    if not path.exists():
        sys.exit(f"找不到字体：{path}\n先安装文津宋体，或把字体路径作为参数传入。")
    return ImageFont.truetype(str(path), FONT_SIZE)


def glyph_layer(font: ImageFont.FreeTypeFont) -> Image.Image:
    """把字形画在透明层上，裁到墨迹包围盒。"""
    canvas = Image.new("RGBA", (SIZE * 2, SIZE * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (SIZE, SIZE),
        "金",
        font=font,
        fill=GLYPH,
        anchor="mm",
        stroke_width=STROKE,
        stroke_fill=GLYPH,
    )
    bbox = canvas.getbbox()
    if bbox is None:
        sys.exit("字形渲染为空，检查字体是否含该字符")
    return canvas.crop(bbox)


def main() -> None:
    font_path = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_FONT
    font = load_font(font_path)

    img = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    # 双层边框，比例照金印样式：外粗内细
    draw.rounded_rectangle(
        [44, 44, SIZE - 44, SIZE - 44], radius=120, outline=GOLD, width=30
    )
    inner = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(inner).rounded_rectangle(
        [110, 110, SIZE - 110, SIZE - 110], radius=88, outline=GOLD, width=12
    )
    # 内框压暗一点，避免和外框抢视觉
    alpha = inner.split()[3].point(lambda a: int(a * 0.6))
    inner.putalpha(alpha)
    img = Image.alpha_composite(img, inner)

    # 字形：缩放到目标墨迹宽度，按包围盒居中
    glyph = glyph_layer(font)
    ratio = INK / glyph.width
    glyph = glyph.resize((INK, round(glyph.height * ratio)), Image.LANCZOS)
    pos = ((SIZE - glyph.width) // 2, (SIZE - glyph.height) // 2)
    img.alpha_composite(glyph, pos)

    out = Image.new("RGB", (SIZE, SIZE), BG)
    out.paste(img, (0, 0), img)
    out = out.resize((OUT, OUT), Image.LANCZOS)

    here = pathlib.Path(__file__).parent
    out.save(here / "icon.png")

    # 自检：墨迹包围盒中心与画布中心的偏差
    box = out.convert("L").point(lambda v: 255 if v > 40 else 0).getbbox()
    cx = (box[0] + box[2]) / 2 - OUT / 2
    cy = (box[1] + box[3]) / 2 - OUT / 2
    print(f"{here / 'icon.png'}  内容包围盒中心偏差 dx={cx:.1f} dy={cy:.1f}")


if __name__ == "__main__":
    main()
