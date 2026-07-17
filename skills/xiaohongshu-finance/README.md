# 小红书财经 · 专业投资内容生成器

> 自动生成符合小红书平台规范的专业投资理财文案，内置违禁词规避系统。

---

## 这个 Skill 是什么

这是一个面向小红书财经博主的 AI 内容生成技能。它不是一个代码项目，而是一套完整的内容生产工作流——当你需要写小红书投资理财类内容时，激活这个 Skill，它会自动帮你：

- ✅ 生成符合小红书风格的爆款标题（3-5个备选）
- ✅ 撰写结构化的专业投资文案
- ✅ 自动规避小红书违禁词（内置完整替代词库）
- ✅ 生成专业封面图（driver.py，8种模板 + 6种图表）
- ✅ 搭配合理的标签组合
- ✅ 对不确定的数据自动搜索验证
- ✅ 每篇内容附带风险提示

## 适合谁用

- 想做小红书财经博主但不知道怎么写内容的人
- 已经在做但经常踩违禁词/被限流的人
- 需要批量生产高质量投资理财内容的人
- 想要专业投资风格但又不想太枯燥的人

## 安装方式

### Claude Code

将 `skills/xiaohongshu-finance/` 目录复制到你的项目 `.claude/skills/` 目录下：

```bash
# 在你的项目根目录
mkdir -p .claude/skills
cp -r /path/to/ibook-skill/skills/xiaohongshu-finance .claude/skills/
```

### OpenClaw

将 `skills/xiaohongshu-finance/` 目录复制到 OpenClaw 技能目录：

```bash
cp -r /path/to/ibook-skill/skills/xiaohongshu-finance ~/.openclaw/skills/
```

### Codex

将 `skills/xiaohongshu-finance/` 目录复制到 Codex 技能目录：

```bash
cp -r /path/to/ibook-skill/skills/xiaohongshu-finance ~/.codex/skills/
```

## 激活方式

在对话中使用以下短句激活：

- `帮我写一篇小红书`
- `生成小红书文案`
- `小红书投资内容`
- `写个财经小红书`
- `小红书理财文案`

## 使用示例

### 示例1：生成基金定投入门文案

```
用户：帮我写一篇关于基金定投的小红书文案

AI：（自动激活 xiaohongshu-finance skill）
📌 标题备选：
1. 基金定投入门｜月薪5000也能开始的理财方式
2. 定投3年，我的收益跑赢了90%的散户
3. 别再说不会理财了！这个方法小学生都能学会

📝 正文：
（完整文案，包含数据、分点、风险提示）

🏷️ 标签：
#基金定投 #理财入门 #小白理财 #定投笔记 ...

🎨 封面图：
（driver.py 生成的图片文件路径）
```

### 示例2：解读最新经济数据

```
用户：帮我写一篇解读最新CPI数据的小红书

AI：（先搜索最新CPI数据，然后生成内容）
📌 标题备选：
1. X月CPI数据出炉，释放了什么信号？
2. 通胀还是通缩？看完这组数据你就懂了
...
```

## 目录结构

```
xiaohongshu-finance/
├── SKILL.md                        # 主技能文件（核心指令）
├── README.md                       # 本文件
├── CLAUDE.md                       # Claude Code 开发指引
├── driver.py                       # 封面图/图表生成器（Playwright 截图）
├── requirements.txt                # Python 依赖
├── references/
│   ├── banned-words.md             # 违禁词库与合规替代词
│   ├── copywriting-templates.md    # 文案模板与结构
│   └── hashtag-strategy.md         # 标签策略与推荐标签
├── templates/                      # HTML/SVG 封面图模板（8种）
│   ├── card.html                   # 要点列表卡片
│   ├── minimal.html                # 极简标题卡片
│   ├── data.html                   # 数据仪表盘
│   ├── table.html                  # 数据表格
│   ├── comparison.html             # 双栏对比
│   ├── kpi.html                    # KPI 指标看板
│   ├── ranking.html                # 排行榜
│   └── chart.html                  # SVG 图表容器
└── examples/                       # 图表示例 JSON 配置
    ├── line.json / bar.json / pie.json
    ├── donut.json / area.json / mixed.json
```

## 内置能力

### 违禁词规避系统

内置 200+ 违禁词及合规替代词，覆盖：
- 绝对化用语
- 虚假宣传类
- 金融投资专项（承诺收益、荐股荐基、引导性词汇）
- 平台敏感词（含谐音变体检测）
- 涉政/敏感类

### 6种文案模板

| 模板 | 适用场景 |
|------|----------|
| 科普入门型 | 基金定投入门、什么是ETF |
| 深度分析型 | 经济数据分析、市场解读 |
| 观点输出型 | 投资理念分享、趋势判断 |
| 实操指南型 | 开户教程、定投设置 |
| 热点解读型 | 政策解读、市场异动 |
| 对比分析型 | 基金对比、理财比较 |

### 封面图生成

通过 `driver.py` 一键生成专业封面图（需安装 Playwright）：

```bash
pip install playwright && playwright install chromium
```

**7 种文字卡片模板：** card / minimal / data / table / comparison / kpi / ranking

**6 种数据图表：** line / bar / pie / donut / area / mixed

```bash
# 文字卡片
python driver.py --template card --title "标题" --points "要点1" "要点2"

# 数据图表
python driver.py --template chart --chart-type line --config examples/line.json
```

图表支持 `description` 字段在图表下方添加专业分析文字。详见 `examples/` 目录。

### 标签策略

内置标签库 + 组合原则，确保每篇内容的标签搭配合理。

## 注意事项

- ⚠️ AI 生成的内容仅供参考，发布前请人工审核
- ⚠️ 违禁词库可能滞后于平台最新规则，建议用「零克查词」二次检查
- ⚠️ 经济数据和市场分析需要核实后才能发布
- ⚠️ 每篇内容必须包含风险提示语
- ⚠️ 不保证内容一定获得高流量，流量受多因素影响

## 更新日志

- **v1.1** (2025-06)：新增 driver.py 封面图生成器，支持 7 种文字卡片模板 + 6 种 SVG 数据图表，统一蓝灰色调主题
- **v1.0** (2025-06)：初始版本，包含完整违禁词库、6种文案模板、封面图提示词、标签策略
