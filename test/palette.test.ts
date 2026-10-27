import test from "node:test";
import assert from "node:assert/strict";
import contribute from "../index.client.ts";

// 主题贡献的形状（只取本插件用到的字段）
type Contribution = {
  id: string;
  name: string;
  appearance: "light" | "dark";
  colors: Record<string, string>;
};

/** 用一个假 client 收集 addTheme 的调用结果 */
function collect(): Contribution[] {
  const themes: Contribution[] = [];
  const client = { addTheme: (theme: Contribution) => themes.push(theme) };
  contribute(client as unknown as Parameters<typeof contribute>[0]);
  return themes;
}

// ---- WCAG 对比度工具（测试内自足，不引依赖） ----
function luminance(hex: string): number {
  const v = hex.replace("#", "");
  const [r, g, b] = [0, 2, 4].map((i) => {
    const c = parseInt(v.slice(i, i + 2), 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrast(a: string, b: string): number {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

const HEX = /^#[0-9a-fA-F]{6}$/;
const FIELDS = [
  "background",
  "foreground",
  "raised",
  "control",
  "border",
  "accent",
  "mutedForeground",
  "ring",
];

const themes = collect();

test("注册且只注册两个主题", () => {
  assert.equal(themes.length, 2);
  assert.deepEqual(
    themes.map((t) => t.id).sort(),
    ["dark", "light"],
  );
});

test("明暗端各自声明正确的 appearance", () => {
  const byId = Object.fromEntries(themes.map((t) => [t.id, t]));
  assert.equal(byId.dark.appearance, "dark");
  assert.equal(byId.light.appearance, "light");
});

test("主题名非空且不超过 60 字符（Paseo 的字段上限）", () => {
  for (const t of themes) {
    assert.ok(t.name.trim().length > 0, `${t.id} 的名字为空`);
    assert.ok(t.name.trim().length <= 60, `${t.id} 的名字超过 60 字符`);
  }
});

test("每个主题恰好提供 8 个字段且都是合法十六进制色值", () => {
  for (const t of themes) {
    assert.deepEqual(Object.keys(t.colors).sort(), [...FIELDS].sort(), `${t.id} 字段不齐`);
    for (const field of FIELDS) {
      assert.match(t.colors[field], HEX, `${t.id}.${field} 不是合法色值`);
    }
  }
});

test("正文与气泡文字保持可读（AA 以上）", () => {
  for (const t of themes) {
    const c = t.colors;
    // 正文对页面背景：本主题的目标是 7:1 以上
    assert.ok(contrast(c.foreground, c.background) >= 7, `${t.id} 正文对背景不足 7:1`);
    // 用户气泡背景绑在 border 字段上，气泡文字是 foreground
    assert.ok(contrast(c.foreground, c.border) >= 4.5, `${t.id} 气泡文字对比不足 4.5:1`);
    // 次要文字
    assert.ok(contrast(c.mutedForeground, c.background) >= 4.5, `${t.id} 次要文字对比不足 4.5:1`);
  }
});

test("强调色与背景保持 4.5:1（强调底色上的文字取 background）", () => {
  for (const t of themes) {
    const ratio = contrast(t.colors.accent, t.colors.background);
    assert.ok(ratio >= 4.5, `${t.id} 强调色对比仅 ${ratio.toFixed(2)}:1`);
  }
});

test("暗端金色与亮端强调金不同，避免浅底直接套用同一值", () => {
  const byId = Object.fromEntries(themes.map((t) => [t.id, t]));
  assert.notEqual(byId.dark.colors.accent, byId.light.colors.accent);
  // 浅底必须用更深的金，否则对比不足
  assert.ok(luminance(byId.light.colors.accent) < luminance(byId.dark.colors.accent));
});
