# Paseo Gilded Fortune 主题插件

本文件沉淀本插件的技术约束与配色决策，避免以后重复查源码 / 重复踩坑。

## 项目背景

为 Paseo 贡献的「金运亨通」明暗双主题。色板不是移植任何第三方 Obsidian 主题，而是以作者自建的
五行「补金」运势页为母版推导而来，因此**无上游版权依赖**，
仓库只需自己的 MIT LICENSE，不需要 NOTICE。

- Paseo 源码：`https://github.com/getpaseo/paseo`（AGPLv3，monorepo）
- 插件 id：`gilded-fortune`；主题贡献 id 为 `dark` / `light`，Paseo 自动拼成
  `gilded-fortune/theme/dark`、`gilded-fortune/theme/light`
- 本地开发环境：Paseo 0.13.2，SDK `@getpaseo/plugin` ^0.13.2

## 8 字段契约

插件只能贡献 8 个色值，其余色板由 Paseo 推导（源码 `packages/app/src/plugins/themes/index.ts`）：

| 插件字段 | 映射 | 主要用途 |
|---|---|---|
| `background` | `surface0` | 页面背景 |
| `raised` | `surface1` | 助手气泡、卡片 |
| `control` | `surface2` | 标题栏、输入框、侧栏（浅色端） |
| **`border`** | **`surface3`** | **用户气泡背景** + 卡片/控件背景 + 边框线 |
| `foreground` | `foreground` | 正文 |
| `mutedForeground` | `foregroundMuted` | 次要文字 |
| `accent` | `accent` | 强调色（按钮、选中态、标签） |
| `ring` | `surface4` + `foregroundExtraMuted` + `terminalBrightBlack` | 焦点环、滚动条、时间戳、选中行底色 |

约束要点：

- **用户气泡背景绑死在 `border`**（0.5.1 起 `message.tsx` 用 `surface3` 作气泡底色，文字是 `foreground`），
  所以 `border` 必须与 `background` 拉开距离；本主题取 `#292517`，正文压上去 13.4:1
- 强调底色上的文字取 **`background`**（源码 `accentForeground: colors.background`），
  因此 `accent` 与 `background` 的对比度必须 ≥ 4.5:1
- `ring` 一个 token 三种用途，是三端最难选的值，见下节

## 0.12.0 起的 `ring` / `surface4` 回归

- 根因 commit `01f9bc8`「Modernize compact headers and sidebar affordances (#6431)」（2026-10-10）：
  仅改 `buildLightSemanticColors`，把浅色主题的 `surfaceSidebarSelected` 从 `surface3` 改成 `surface4`，
  而插件主题的 `surface4` 绑的是 `ring`。0.13.2 打包产物里仍能看到
  `surfaceSidebarSelected: t.surface4`（深色端是 `surface2`，不受影响）。
- 后果：浅色主题若把 `ring` 设成深色（如 Solarized Light 的 `#586e75`），侧栏选中行就是
  「深底压深字」，实测 1.21:1，几乎不可读（上游 issue #7471）。
- 同一 token 还兼任 `foregroundExtraMuted`（弱化文字）与 composer placeholder，方向与「选中行底色」相反。
  **8 色契约内无解**：深了选中行糊，浅了弱化文字看不见。

本插件的取舍：亮端 `ring` 取中间调 `#8f7429`，两个用途各约 3.8:1——都不达 AA，但都不是「不可读」。
选它而不是 `#8a6d1f`（4.12 / 3.61）是因为它和 `accent` 同色相（44°）、同饱和度（55%），只是深两档，
色系上自洽。等上游拆开 `surface4` 与 `foregroundExtraMuted` 的绑定后，可以再分别优化。

暗端不受此问题影响（`surfaceSidebarSelected` 走 `surface2` = `control`）。

## 配色决策记录

| 决策 | 值 | 理由 |
|---|---|---|
| 暗端背景 | `#17150f` | 直接取源页面，近黑褐，不纯黑 |
| 暗端正文 | `#f5efe0` | 源页面正文色，15.9:1 |
| 暗端强调金 | `#c8a63f` | 源页面是 `#d4af37`（饱和 65%），压到 55%，色相/明度不变 |
| 暗端焦点环 | `#d9c06b` | 跟随强调金提亮，滚动条/时间戳可读 |
| 亮端底 | `#f2ebda` | 与暗端同色系推导的羊皮纸 |
| 亮端强调金 | `#7a5f1a` | 源色在浅底上不可用；`#8a6d1f` 仅 4.12:1，压到 5.08:1 |
| 亮端 ring | `#8f7429` | 见上节折中说明 |

已验算的 WCAG 对比度（脚本：`design/gen_palette_svg.py` 同源算法）：

| | 正文/底 | 次文/底 | 强调/底 | 正文/气泡 |
|---|---|---|---|---|
| 暗端 | 15.91:1 | 9.98:1 | 8.68:1（原味）/ 7.81:1（压一档） | 13.35:1 |
| 亮端 | 14.89:1 | 6.02:1 | 5.08:1 | 12.15:1 |

## 设计稿

`design/palette.svg` 由 `design/gen_palette_svg.py` 生成（纯 Python 标准库，无依赖）。
改色后重新执行脚本即可，不要手改 SVG：

```bash
python3 design/gen_palette_svg.py
```

## 常用命令

```bash
export PATH="/Applications/Paseo.app/Contents/Resources/bin:$PATH"

npm run typecheck                 # 必须通过
paseo plugin add .                # 首次安装
paseo plugin reload gilded-fortune
paseo plugin ls
paseo plugin logs gilded-fortune
paseo plugin remove gilded-fortune   # 只删配置，不删源码目录
```

⚠️ 插件 id 由 **daemon 配置键**决定（`loadDirectoryPlugin` 里 `id: pluginId`），
`paseo-plugin.json` 的 `id` 只在安装时用于生成配置键。改了 manifest 的 `id` 必须
`paseo plugin remove <旧键>` 后重装，`reload` 不会换前缀。

## paseo.cafe 收录

- 收录入口：向 `getpaseo/plugins` 提 PR，新增 `plugins/<owner>/<id>.json`（文件名 = 插件 id）
- ⚠️ **新条目强制声明公开 npm 包**：`scripts/plugin-security/targets.ts` 对
  `!previous && !baseIds.has(id) && !entry.package` 直接抛错；git-only 只对规则生效前的历史条目有效
- `package.json` 的 `version` 不能是 `0.0.0`；仓库 version、npm 已发布 version、registry 声明三者必须一致
- 发布包内必须带 `paseo-plugin.json` + `index.client.ts`（纯数据主题无需 build）
- 本机 `~/.npmrc` 指向 npmmirror（只读镜像），发布必须显式 `--registry=https://registry.npmjs.org`

## 开发日志

每次修改后更新 `devlog/`（格式：`YYYYMMDD-<简述>.md`），记录用户需求、问题定位、最终方案。
