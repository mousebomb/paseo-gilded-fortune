# Paseo Gilded Fortune 主题插件

[English](README.md) | 中文

为 [Paseo](https://github.com/getpaseo/paseo) 提供的 **金运亨通（Gilded Fortune）** 明暗双主题：近黑褐色底、压一档的鎏金强调色、奶油白正文，配一套同源推导的羊皮纸亮色版。

![Gilded Fortune 配色对照](./design/palette.svg)

## 安装

需要 Paseo 0.8 或更高版本。以下三种方式**任选其一**：

### npm

```bash
paseo plugin add npm:@mousebomb/paseo-gilded-fortune
```

### Git

```bash
paseo plugin add github:mousebomb/paseo-gilded-fortune
```

### 源码安装（开发用）

```bash
git clone https://github.com/mousebomb/paseo-gilded-fortune.git
cd paseo-gilded-fortune
npm install
npm run typecheck
paseo plugin add .
```

安装后启用插件并选择主题：

1. **Settings → Plugins** → 打开 **Enable plugins**
2. **Settings → Appearance → Theme** → 选择 **Gilded Fortune** 或 **Gilded Fortune Light**

修改代码后热重载：

```bash
paseo plugin reload gilded-fortune
```

如果 `paseo` 命令不在 PATH：

```bash
/Applications/Paseo.app/Contents/Resources/bin/paseo plugin add .
```

## 设计要点

- 插件只贡献 Paseo 开放给主题的 8 个色值，界面其余颜色由 Paseo 自行推导，升级不会被覆盖
- 暗端金色用 `#c8a63f`（饱和度 55%），不是原页面的 `#d4af37`（65%）：同样的色相与明度，久看更稳
- 亮端强调金必须压到 `#7a5f1a`，否则与羊皮纸底对比不足 4.5:1
- `border` 字段同时承担用户气泡背景，所以取的是比卡片再深一档的 `#292517`，正文压上去 13.4:1
- 亮端 `ring` 取 `#8f7429`：它同时被 Paseo 用作选中行底色与弱化文字，取中间调让两个用途都不至于不可读（详见 `AGENTS.md`）

完整色值与对比度见 [`design/palette.svg`](./design/palette.svg)，生成脚本为 `design/gen_palette_svg.py`。

## License

MIT。主题配色由作者自建的五行「补金」运势页推导，无第三方色板版权依赖。
