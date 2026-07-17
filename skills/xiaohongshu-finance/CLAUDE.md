# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An AI skill (not a traditional software project) for generating Xiaohongshu (小红书) financial content. It produces platform-compliant investment copywriting with built-in banned-word avoidance, cover image generation, and hashtag strategy. Installable into Claude Code, OpenClaw, or Codex by copying this directory into the respective skills folder.

## Architecture

```
SKILL.md                    ← Core skill definition: activation rules, safety constraints, workflow, title formulas, expression DNA
references/                 ← Domain knowledge loaded at generation time
  banned-words.md           ← 200+ banned words + compliant replacements (check before every output)
  copywriting-templates.md  ← 6 content templates (科普入门/深度分析/观点输出/实操指南/热点解读/对比分析)
  hashtag-strategy.md       ← Tag library + combination strategy (大流量 + 垂直 + 长尾 + 热点)
  image-prompts.md          ← Midjourney/DALL-E prompt templates
  a-stock-data.md           ← A股数据接入: mootdx/百度/腾讯 (self-contained)
  global-stock-data.md      ← 港股美股数据接入: 新浪/Yahoo/腾讯 (self-contained)
templates/                  ← HTML/SVG templates for cover image rendering (8 types, unified blue-gray theme)
  card.html                 ← Default: numbered points card
  minimal.html              ← Title + subtitle only
  data.html                 ← 2×2 data grid with trend indicators
  table.html                ← Tabular data with conditional coloring
  comparison.html           ← Side-by-side VS comparison
  kpi.html                  ← KPI dashboard with progress bars
  ranking.html              ← Ranked list with bar charts
  chart.html                ← SVG chart container (line/bar/pie/donut/area/mixed/candle)
examples/                   ← Example JSON configs for each chart type (含 candle.json)
driver.py                   ← Python script: renders HTML/SVG templates → Playwright screenshots → PNG
```

## Key Workflows

### Content Generation (SKILL.md workflow)

The 5-step agentic protocol in SKILL.md is the core process:
1. **需求确认** — Confirm topic, style, word count, audience (defaults exist)
2. **信息验证** — Search-verify any uncertain data before writing (economic data, market prices, policies)
3. **内容生成** — Produce title options (3-5), body copy, hashtags (8-15), cover image prompt
4. **合规检查** — Run banned-word scan, verify no promise of returns, confirm risk disclaimer present
5. **输出交付** — Structured output with 📌标题/📝正文/🏷️标签/🎨封面图/⚠️风险提示

### Cover Image Generation (driver.py)

```bash
# Basic card with points
python driver.py --title "标题" --points "要点1" "要点2" "要点3"

# Charts (SVG, 6 chart types)
python driver.py --template chart --chart-type line --config examples/line.json

# Generate complete post (image + text together)
python driver.py generate examples/post_chart.json --output-dir output/
python driver.py generate examples/post_card.json --output-dir output/

# Flex template: full control over HTML content
python driver.py --template flex --config flex.json --title "主标题" --subtitle "副标题" --footer "风险提示"
# flex.json: {"content": "<div>自由的HTML内容，可包含图表、表格、对比区块等</div>"}
```

## Flex Template Guide (for AI generating rich content)

The `--template flex` option gives full control over the card layout. Use it when you need:

### Multi-section layout
```html
<div class="section-title">章节标题</div>
<p style="font-size:20px;line-height:1.8;color:rgba(234,224,207,0.75);margin-bottom:16px;">
段落文字
</p>
```

### Data comparison block
```html
<div style="display:flex;gap:16px;margin:20px 0;">
  <div style="flex:1;padding:16px;background:rgba(75,86,148,0.08);border-radius:12px;">
    <div style="font-size:14px;color:#7288AE;">标签</div>
    <div style="font-size:32px;font-weight:700;color:#EAE0CF;margin-top:4px;">数值</div>
  </div>
</div>
```

### Inline table
```html
<table style="width:100%;border-collapse:collapse;margin:16px 0;">
  <thead><tr><th style="padding:10px;text-align:center;color:#7288AE;border-bottom:1px solid rgba(114,136,174,0.2);font-size:16px;">列标题</th></tr></thead>
  <tbody><tr><td style="padding:10px;text-align:center;color:rgba(234,224,207,0.75);font-size:16px;border-bottom:1px solid rgba(114,136,174,0.08);">数据</td></tr></tbody>
</table>
```

### Embedded SVG chart
Generate a chart config first, then embed its SVG as a data URL or reference.

### Design principles for flex content
- Use `rgba(234,224,207,0.75)` for body text on dark theme
- Use `#7288AE` for labels and section markers
- Use `#EAE0CF` for highlighted values and headings
- Keep paragraph `font-size` between 18-22px
- Section spacing: `margin: 24px 0 12px` for titles, `margin-bottom: 16px` for paragraphs

`driver.py` requires `playwright` (`pip install playwright && playwright install chromium`). Windows UTF-8 handling is built in.

## Critical Rules (from SKILL.md Safety Principles)

These are hard constraints, not suggestions:

1. **Banned words are zero-tolerance** — every output must pass the banned-word check from `references/banned-words.md`. Hit = replace, no exceptions.
2. **Never promise returns** — no "保证赚钱", "稳赚不赔", "年化XX%".
3. **Never recommend specific trades** — analyze methods/logic, never say "买入/卖出". Must include: "以上仅为个人分析，不构成投资建议".
4. **Data must be sourced** — cite origins for economic/market data. If uncertain, search first.
5. **Risk disclaimer required** — every piece of financial content must end with a risk warning.
6. **No anxiety-inducing content** — no panic headlines, maintain professional tone.
7. **No引流/导流** — no WeChat IDs, private messages, or external links.

## Template Variables

HTML templates use `{{VARIABLE}}` placeholders: `{{TITLE}}`, `{{SUBTITLE}}`, `{{POINTS_HTML}}`, `{{DATA_HTML}}`, `{{TABLE_HTML}}`, `{{COMPARE_HTML}}`, `{{KPI_HTML}}`, `{{RANKING_HTML}}`, `{{CHART_HTML}}`, `{{FOOTER}}`, `{{STYLE_CLASS}}`, `{{ICON}}`.

Unified blue-gray theme (`#111844` / `#4B5694` / `#7288AE` / `#EAE0CF`). `{{STYLE_CLASS}}` hardcoded to `dark`.

## Chart Config Format

Charts use JSON config with `chart_type` and `chart_data`. For line/bar/area/mixed, data uses `labels` + `datasets`. For pie/donut, data uses `items` with `label`/`value`/`color`. See `examples/` for reference configs.

## Content Output Format

Every generated post follows this structure (from SKILL.md Step 5):

```
📌 标题备选： (3-5 options)
📝 正文：     (structured copy)
🏷️ 标签：     (8-15 hashtags: 2-3 大流量 + 3-5 垂直 + 2-3 长尾 + 1-2 热点)
🎨 封面图/图表： (driver.py 生成)
⚠️ 风险提示： (status of disclaimer inclusion)
```
