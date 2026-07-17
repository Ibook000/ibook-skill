# 小红书财经封面图参考

> 封面图决定点击率。优先使用 `driver.py` 生成专业封面图（8 种模板 + 6 种图表）。
> 以下 AI 绘图提示词仅作为备选参考，用于需要 AI 插画风格时。

---

## 主要方案：driver.py

推荐使用 `driver.py` 生成封面图，无需 AI 绘图：

```bash
# 要点列表卡片
python driver.py --title "标题" --points "要点1" "要点2" "要点3" --font classic

# 数据图表
python driver.py --template chart --chart-type bar --config examples/bar.json

# 批量生成
python driver.py --title "标题" --count 3 --font default
```

支持 8 种模板（card/minimal/data/table/comparison/kpi/ranking/chart）和 6 种图表（line/bar/pie/donut/area/mixed），字体预设 5 种，输出按日期组织到 `output/YYYY-MM-DD/`。

---

## 备选方案：AI 绘图（仅插画风格需要）

以下提示词模板适用于 Midjourney / Stable Diffusion / DALL-E，用于需要扁平插画、商务插画等非数据图表的场景。

---

## 风格一：数据可视化

### 基础模板

```
A professional financial data visualization poster, showing {图表类型} chart with {数据主题} data, clean modern design, dark blue and white color scheme, minimalist style, high contrast, suitable for social media thumbnail, 3:4 aspect ratio, no text
```

### 图表类型变体

**柱状图风格**
```
A sleek financial bar chart infographic poster, comparing {对比项}, professional dark blue background with gold accent bars, clean data visualization, modern flat design, social media ready, 3:4 aspect ratio, no text
```

**折线图风格**
```
An elegant line chart showing market trend over time, upward trending golden line on dark navy background, subtle grid lines, professional financial dashboard aesthetic, clean minimalist design, 3:4 aspect ratio, no text
```

**饼图风格**
```
A professional asset allocation pie chart infographic, showing portfolio distribution, harmonious color palette of navy blue gold and white, clean modern financial design, suitable for social media, 3:4 aspect ratio, no text
```

**仪表盘风格**
```
A financial dashboard poster with multiple KPI indicators, showing growth metrics and percentages, professional dark theme with green and gold accents, modern data visualization, 3:4 aspect ratio, no text
```

---

## 风格二：极简文字卡片

### 基础模板

```
A minimalist financial text card design, clean white background with bold dark text area in center, subtle gold accent line, professional typography layout, modern and elegant, suitable for social media thumbnail, 3:4 aspect ratio, no text
```

### 颜色变体

**白底金字**
```
A premium minimalist poster design, clean white background, large centered text placeholder area, gold accent border and subtle gold decorative elements, luxury financial aesthetic, 3:4 aspect ratio, no text
```

**深底白字**
```
A professional dark-themed financial card, deep navy blue background with white text placeholder area, subtle geometric patterns, gold accent details, modern executive style, 3:4 aspect ratio, no text
```

**渐变底**
```
A modern gradient background card design, transitioning from deep blue to teal, with a clean white text overlay area, subtle financial icons in background, professional and modern, 3:4 aspect ratio, no text
```

---

## 风格三：扁平插画

### 基础模板

```
A warm flat illustration of {场景描述}, soft pastel colors, modern vector art style, friendly and approachable, financial literacy theme, clean composition, suitable for social media, 3:4 aspect ratio, no text
```

### 场景变体

**存钱场景**
```
A cute flat illustration of a piggy bank with coins being inserted, warm pastel pink and gold colors, modern vector style, savings and investment theme, clean minimal background, 3:4 aspect ratio, no text
```

**增长场景**
```
A cheerful flat illustration of a small plant growing into a tree with golden coins as leaves, warm green and gold palette, modern vector art, investment growth concept, clean background, 3:4 aspect ratio, no text
```

**规划场景**
```
A friendly flat illustration of a person reviewing financial plans on a clipboard, warm pastel colors, modern vector style, financial planning theme, organized and calm atmosphere, 3:4 aspect ratio, no text
```

**目标场景**
```
An inspiring flat illustration of a target board with an arrow hitting bullseye, surrounded by floating coins, warm gold and blue palette, modern vector art, financial goal achievement, 3:4 aspect ratio, no text
```

---

## 风格四：金融商务

### 基础模板

```
A professional financial photography style image, {场景描述}, premium quality, corporate blue and gold color scheme, depth of field, cinematic lighting, high-end business aesthetic, 3:4 aspect ratio, no text
```

### 场景变体

**城市金融**
```
A stunning aerial view of modern city skyline at golden hour, financial district with glass skyscrapers, warm golden light, cinematic composition, prosperity and growth metaphor, premium quality, 3:4 aspect ratio, no text
```

**数据分析**
```
A close-up of a professional analyzing financial data on multiple screens, blue and gold ambient lighting, bokeh background, modern trading desk aesthetic, high-end professional atmosphere, 3:4 aspect ratio, no text
```

**黄金/贵金属**
```
A luxurious close-up of polished gold bars stacked elegantly, warm golden lighting, shallow depth of field, premium quality photography, wealth and value concept, 3:4 aspect ratio, no text
```

**书籍/学习**
```
An elegant still life of financial books, a cup of coffee, and a notebook on a wooden desk, warm morning light, cozy yet professional atmosphere, financial education concept, 3:4 aspect ratio, no text
```

---

## 场景专用提示词

### 宏观经济

```
A professional infographic poster showing global economic indicators, world map with data points and connection lines, blue and gold color scheme, clean modern design, macroeconomic analysis theme, 3:4 aspect ratio, no text
```

### 基金投资

```
A modern investment fund concept illustration, showing diversified portfolio as interconnected circles, professional blue gradient background, clean data visualization style, fund investment theme, 3:4 aspect ratio, no text
```

### 股票分析

```
A professional stock market analysis poster, showing candlestick chart pattern, dark background with green and red candles, technical analysis aesthetic, clean modern design, 3:4 aspect ratio, no text
```

### 房产投资

```
A modern real estate investment concept, miniature houses with upward arrows and coins, clean white background, warm pastel colors, property investment growth theme, flat design style, 3:4 aspect ratio, no text
```

### 黄金投资

```
A luxurious gold investment concept image, polished gold coins and bars arranged elegantly, warm amber lighting, dark background, premium quality, precious metals theme, 3:4 aspect ratio, no text
```

### 加密货币

```
A modern cryptocurrency concept illustration, abstract blockchain network with glowing nodes, futuristic blue and purple color scheme, clean digital aesthetic, crypto investment theme, 3:4 aspect ratio, no text
```

### 保险规划

```
A warm and protective concept illustration, an umbrella sheltering a family and their home, soft blue and green colors, safety and protection theme, modern flat design, 3:4 aspect ratio, no text
```

### 财务自由

```
An inspiring financial freedom concept, a person standing on a mountain peak overlooking a sunrise, warm golden light, achievement and liberation theme, cinematic composition, 3:4 aspect ratio, no text
```

---

## 提示词优化技巧

### 增加专业感

在任意提示词后追加：
```
professional quality, sharp details, clean composition, modern aesthetic
```

### 增加温暖感

在任意提示词后追加：
```
warm lighting, soft shadows, inviting atmosphere, friendly mood
```

### 增加科技感

在任意提示词后追加：
```
futuristic elements, digital aesthetic, holographic accents, tech-forward design
```

### 统一账号风格

建议选定1-2种固定风格，在所有提示词中保持一致的：
- 配色方案（如：navy blue + gold）
- 构图风格（如：centered composition）
- 光影效果（如：soft warm lighting）

---

## 使用说明

1. 将 `{场景描述}` 替换为具体内容
2. 根据文案主题选择对应风格
3. 建议使用 3:4 竖版比例（小红书推荐）
4. 生成后可添加文字标题（使用 Canva 等工具）
5. 保持同一账号的封面风格统一
