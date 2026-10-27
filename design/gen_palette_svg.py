#!/usr/bin/env python3
"""生成 README 用的配色卡 SVG：只呈现最终采用的暗/亮两套色板。

改色后重新执行本脚本，不要手改 SVG：
    python3 design/gen_palette_svg.py
"""

W, H = 1240, 680
PAD = 40
PANEL_W = 560
PANEL_H = 530

FONT = "'PingFang SC','Hiragino Sans GB','Noto Sans SC',-apple-system,sans-serif"
MONO = "'SF Mono',Menlo,monospace"

# 最终采用的色板（暗端为压一档的金，非源页原色）
DARK = dict(
    bg="#17150f", raised="#1e1b13", control="#221f15", border="#292517",
    fg="#f5efe0", muted="#c9bfa5", accent="#c8a63f", ring="#d9c06b",
    name="Gilded Fortune", sub="暗色 · 近黑褐底 + 鎏金",
    ratios="正文 15.9:1　次文 10.0:1　强调 7.8:1",
)
LIGHT = dict(
    bg="#f2ebda", raised="#f8f3e6", control="#ece4d0", border="#e0d5bc",
    fg="#1b1813", muted="#5f5745", accent="#7a5f1a", ring="#8f7429",
    name="Gilded Fortune Light", sub="亮色 · 同源推导的羊皮纸",
    ratios="正文 14.9:1　次文 6.0:1　强调 5.1:1",
)

# 8 个字段的展示顺序与中文名
ROLES = [
    ("bg", "背景"),
    ("raised", "凸起层"),
    ("control", "控件"),
    ("border", "气泡"),
    ("fg", "正文"),
    ("muted", "次文"),
    ("accent", "强调"),
    ("ring", "焦点环"),
]


def lum(hexv):
    hexv = hexv.lstrip("#")
    r, g, b = [int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def chip_text_color(hexv):
    """在色块上放深字还是浅字，按亮度挑对比更高的一边。"""
    return "#14110b" if lum(hexv) > 0.35 else "#f7f1e2"


def panel(x, y, c):
    p = [f'<rect x="{x}" y="{y}" width="{PANEL_W}" height="{PANEL_H}" rx="18" fill="{c["bg"]}" stroke="#000" stroke-opacity="0.35"/>']

    # 标题区
    p.append(f'<text x="{x+32}" y="{y+52}" font-family="{FONT}" font-size="23" font-weight="700" fill="{c["accent"]}">{c["name"]}</text>')
    p.append(f'<text x="{x+32}" y="{y+76}" font-family="{FONT}" font-size="12.5" fill="{c["muted"]}">{c["sub"]}</text>')

    # 迷你对话示意
    mx, my, mw = x + 32, y + 100, PANEL_W - 64
    p.append(f'<rect x="{mx}" y="{my}" width="{mw}" height="188" rx="12" fill="{c["control"]}"/>')
    p.append(f'<text x="{mx+18}" y="{my+24}" font-family="{MONO}" font-size="10.5" fill="{c["muted"]}">Paseo</text>')
    # 助手气泡
    p.append(f'<rect x="{mx+16}" y="{my+38}" width="{mw-130}" height="62" rx="9" fill="{c["raised"]}"/>')
    p.append(f'<text x="{mx+30}" y="{my+62}" font-family="{FONT}" font-size="13" fill="{c["fg"]}">配色定稿，出两套</text>')
    p.append(f'<text x="{mx+30}" y="{my+84}" font-family="{FONT}" font-size="12" fill="{c["muted"]}">底色不动，只换强调色</text>')
    # 用户气泡（背景 = border 字段）
    p.append(f'<rect x="{mx+mw-226}" y="{my+112}" width="210" height="36" rx="9" fill="{c["border"]}"/>')
    p.append(f'<text x="{mx+mw-212}" y="{my+135}" font-family="{FONT}" font-size="12.5" fill="{c["fg"]}">好，叫金运亨通</text>')
    # 输入区 + 强调按钮
    p.append(f'<rect x="{mx+16}" y="{my+156}" width="{mw-32}" height="20" rx="6" fill="{c["bg"]}" fill-opacity="0.45"/>')
    p.append(f'<circle cx="{mx+mw-26}" cy="{my+166}" r="11" fill="{c["accent"]}"/>')

    # 8 个色块：两行四列
    top = y + 310
    cw, ch, gap = 118, 46, 10
    for i, (key, cn) in enumerate(ROLES):
        col, row = i % 4, i // 4
        cx = x + 32 + col * (cw + gap)
        cy = top + row * (ch + 34)
        hexv = c[key]
        p.append(f'<text x="{cx}" y="{cy-8}" font-family="{FONT}" font-size="11" fill="{c["muted"]}">{cn}</text>')
        p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="7" fill="{hexv}" stroke="{c["fg"]}" stroke-opacity="0.12"/>')
        p.append(f'<text x="{cx+cw/2}" y="{cy+28}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{chip_text_color(hexv)}">{hexv.upper()}</text>')

    # 对比度摘要
    p.append(f'<text x="{x+32}" y="{y+PANEL_H-24}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{c["ratios"]}</text>')
    return "".join(p)


parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Gilded Fortune 配色卡">']
parts.append(f'<rect width="{W}" height="{H}" fill="#0b0a07"/>')
parts.append(f'<text x="{PAD}" y="34" font-family="{FONT}" font-size="11" letter-spacing="4" fill="#8a6d1f">GILDED FORTUNE · 金运亨通</text>')
parts.append(f'<text x="{W-PAD}" y="34" text-anchor="end" font-family="{FONT}" font-size="11" fill="#6f6656">Paseo 主题插件 · 8 色契约</text>')
parts.append(panel(PAD, 76, DARK))
parts.append(panel(PAD + PANEL_W + 40, 76, LIGHT))
parts.append(f'<text x="{PAD}" y="{H-24}" font-family="{FONT}" font-size="11" fill="#6f6656">色块内文字为十六进制值；右侧为同源推导的亮色端，强调金压深以满足浅底对比要求。</text>')
parts.append(f'<text x="{W-PAD}" y="{H-24}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="#4a4335">design/palette.svg</text>')
parts.append("</svg>")

import pathlib
out = pathlib.Path(__file__).with_name("palette.svg")
out.write_text("\n".join(parts), encoding="utf-8")
print(out, len(out.read_text(encoding="utf-8")), "chars")
