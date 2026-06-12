---
name: tweet-card-generator
description: Given a topic, auto-searches for info, generates a tweet + matching data-card PNG (HTML→screenshot, clean cream-background style, multi-layout + multi-chart).
version: 2.0.0
author: Hermes Agent
tags: [twitter, x, social-media, image-generation, data-visualization, screenshot]
platforms: [linux]
triggers:
  - generate a tweet card
  - make a twitter post with image
  - create a data card for X
  - 生成推特推文和配图
  - 做个信息图发推
  - tweet card for
prerequisites:
  commands: [chromium-browser]
---

# Tweet Card Generator v2

One command: give a topic → tweet (≤280 chars) + a high-density data card PNG.

**v2 核心升级：** 4 种布局 × 8 种图表，根据数据自动选最优搭配，不死板。

## Workflow

### Step 1: Research → Step 2: Draft tweet → Step 3: Card HTML → Step 4: Screenshot → Step 5: Post → Step 6: Present

(Same as v1 — unchanged.)

---

## Layout System (v2)

根据话题类型选布局，不要只用一种：

### Layout A: Split（左指标 + 右图表）
- 适用：3-4 个核心数字 + 对比/趋势图
- 经典 Bloomberg 风格
- 之前 Culper NVDA、Gold 卡用的就是这种

### Layout B: Stacked（纵向堆叠）
- 适用：叙事型话题，3-5 个要点，每个配小图
- 上方大数字标题 → 中间 3 列要点 + 迷你图表 → 底部结论
- 信息密度最高，适合"分析报告"型卡片

### Layout C: Big Number（大字报）
- 适用：单一震撼数字 or 对比型
- 超大数字居中 + 2-3 个小图表围绕
- 适合 "68% 市场认为..." 这类话题

### Layout D: Timeline（时间轴）
- 适用：事件演进、历史脉络
- 左侧时间线 + 右侧事件描述 + 关键数字
- 适合"做空报告时间线"这类

### 选择规则
| 数据特征 | 推荐布局 |
|----------|:--:|
| 3-4 个关键指标 + 对比 | Layout A |
| 5+ 分散信息点 | Layout B |
| 1-2 个震撼数字 | Layout C |
| 时间线/事件链 | Layout D |

---

## Chart Library (v2)

All charts are inline SVG — zero external dependencies. They render perfectly in headless Chromium.
Copy the relevant snippet into the `.ch-b` div in `card-dense.html`.

### HTML Templates

| 模板文件 | 用途 | 何时用 |
|----------|------|--------|
| `templates/card-dense.html` | **默认**，高密度多区块网格 | 大部分话题 |
| `templates/card-template.html` | 4 种经典布局（Split/Stacked/Big/Timeline） | 需要特定布局时 |

### Dense Template Building Blocks

| Class | 作用 | 示例 |
|-------|------|------|
| `.r3` | 三等分列 | 3 个指标并排 |
| `.r21` | 2:1 分列 | 2/3 表格 + 1/3 图表 |
| `.r12` | 1:2 分列 | 1/3 指标 + 2/3 大图 |
| `.m` | 指标块 | label + 28px 数字 + subtext |
| `.box` | 信息盒 | 带标题的键值对列表 |
| `.tbl` | 紧凑表格 | 多行对比数据 |
| `.ch-b` | 图表容器 | SVG 自动撑满 |
| `.hr` | 分割线 | 区块间距 |

**组合套路：**
## Chart Library (v2.1)

12 种可复用 SVG 图表，全部零依赖。加载：`skill_view(name="tweet-card-generator", file_path="templates/chart-examples.html")`

| # | 图表 | 典型用途 |
|---|------|----------|
| 1 | Horizontal Bars | 排名、份额对比 |
| 2 | Vertical Bars | 时间序列、季度数据 |
| 3 | Sparkline | 趋势、价格走势 |
| 4 | Donut Ring | 百分比、占比 |
| 5 | Mini Comparison | A vs B、同比对比 |
| 6 | Grouped Bars | 多组对比 |
| 7 | Waterfall | 增减量分解 |
| 8 | Progress Bars | 进度、完成率 |
| 9 | Pie Chart | 构成分布、饼图 |
| 10 | Flow Diagram | 资金链路、流程图 |
| 11 | Stacked Bar | 堆叠构成 |
| 12 | Area Chart | 面积趋势图 |

### 图表选择规则
- 不要所有卡都用柱状图！根据数据选
- 排名/份额 → Horizontal Bars 或 Pie
- 时间序列 → Vertical Bars 或 Area
- 趋势 → Sparkline
- 占比 → Donut 或 Pie
- 流程/链路 → Flow Diagram
- 构成变化 → Stacked Bar 或 Waterfall
- 一张卡 1-3 个小型图表混搭，比 1 个大图丰富

---

## Design Principles (v2)

**强制约束：**
- 背景：#FAF8F5（米白）
- 字体：`-apple-system, 'WenQuanYi Micro Hei', 'PingFang SC', sans-serif`
- 水印：`@IBO0OK` 居中 180px rgba(0,0,0,0.06)
- 无渐变、无阴影、圆角 ≤ 6px
- 色板：主色 3-4 个足够，不要彩虹盘

**密度原则（v2.1 核心）：**
- 🚫 拒绝大留白。1200×675 每一像素都得干活
- 📊 每张卡至少 4 个独立数据点（指标/图表/对比/引用）
- 📏 内边距从 40px 压缩到 24-28px
- 🔢 字号阶梯：Hero 48-56px → 主指标 28-36px → 正文 11-12px → 标注 9-10px
- 🗂 多区块并行：左指标 + 中对比表 + 右迷你图 > 单调两栏
- 📋 能用表格就别用文字罗列
- 📈 一张卡可含 2-3 个小型图表，不限于 1 个大图

**活用的部分：**
- 根据数据选布局，不要永远 Split
- 图表类型和数据匹配
- 强调色从话题语义取（做空=红、增长=绿、科技=蓝、贵金属=金）
- 优先使用 Layout B（Stacked）——信息密度天然最高

---

## Pitfalls

1. **Snap Chromium**: 截图写 `$HOME/.hermes/tweet-cards/` 不用 `/tmp`
2. **中文字体**: 必须包含 `WenQuanYi Micro Hei`
3. **图表**: 只用内联 SVG，不用 Canvas
4. **viewBox 留余量**: SVG viewBox 底部至少留 15-20px 给图例和标注。带图例的图表 viewBox 高度 = 内容高度 + 25px
5. **饼图图例**: 饼图右侧图例距离饼心至少 100px，避免重叠
6. **堆叠柱图例**: 图例放在 viewBox 底部 y=238-244 区域，viewBox 高度 ≥ 255
7. **不要只用一种布局**: 每张卡根据数据独立设计
8. **xurl 国内需走 SOCKS5 代理**：`HTTPS_PROXY=socks5://127.0.0.1:10808`
9. **dasharray 精度**: 饼图/环形图的 `stroke-dasharray` 值 = 百分比 × 周长。周长 = 2πr。先算出周长再算 dasharray
