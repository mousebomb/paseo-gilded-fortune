import type { PluginClientContext } from "@getpaseo/plugin/client";

// 金运亨通（Gilded Fortune）：近黑褐底 + 压一档的鎏金强调色。
// 色板源自自建的五行「补金」运势页，暗端取其原色但把金色饱和度从 65% 压到 55%，
// 以便长时间编写/阅读；亮端由同一套色板推导，强调金必须压深到 #7a5f1a 才满足正文对比要求。
export default function contribute(client: PluginClientContext) {
  client.addTheme({
    id: "dark",
    name: "Gilded Fortune",
    appearance: "dark",
    colors: {
      background: "#17150f", // 页面背景（近黑褐）
      foreground: "#f5efe0", // 正文（奶油白），对对比 15.9:1
      raised: "#1e1b13", // 次级凸起层：助手气泡、卡片
      control: "#221f15", // 控件背景：标题栏、输入框
      border: "#292517", // surface3：用户气泡背景 + 卡片描边，正文压上去 13.4:1
      accent: "#c8a63f", // 强调色：压一档的鎏金（原味 #d4af37 为 65% 饱和度）
      mutedForeground: "#c9bfa5", // 次要文字，9.98:1
      ring: "#d9c06b", // surface4：焦点环、滚动条、时间戳
    },
  });

  client.addTheme({
    id: "light",
    name: "Gilded Fortune Light",
    appearance: "light",
    colors: {
      background: "#f2ebda", // 羊皮纸底
      foreground: "#1b1813", // 正文，14.9:1
      raised: "#f8f3e6", // 更亮一层的卡片
      control: "#ece4d0", // 控件/侧栏（比底略深）
      border: "#e0d5bc", // 用户气泡背景，正文压上去 12.2:1
      accent: "#7a5f1a", // 强调金：深金，5.08:1（#8a6d1f 仅 4.12，不达标）
      mutedForeground: "#5f5745", // 次要文字，6.02:1
      ring: "#8f7429", // 与 accent 同色相、深两档，充当选中行底色与弱化文字
    },
  });

  return () => {};
}
