#!/usr/bin/env python3
"""
小红书财经封面图生成器
手写 HTML+CSS 深色卡片 → Playwright 截图 → PNG

用法:
  python driver.py --title "标题" --content "正文内容"
  python driver.py --config post.json
  python driver.py --title "标题" --points "要点1" "要点2" "要点3"
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

# 模板目录
TEMPLATE_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"

# 字体配置（集中管理，模板和 SVG 共用）
# 需要系统安装「阿里巴巴普惠体 3.0」或通过 @font-face 加载本地字体文件
# 下载地址: https://fonts.alibabafonts.com/#/home
FONT_FAMILY = "Alibaba PuHuiTi 3.0, PingFang SC, Microsoft YaHei, sans-serif"
FONT_FACE_CSS = """
  @font-face {
    font-family: 'Alibaba PuHuiTi 3.0';
    src: local('Alibaba PuHuiTi 3.0');
    font-weight: 100 900;
    font-display: swap;
  }
"""


def load_template(name: str = "card.html") -> str:
    """加载 HTML 模板"""
    template_path = TEMPLATE_DIR / name
    if not template_path.exists():
        print(f"❌ 模板不存在: {template_path}")
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")


def render_card(
    title: str,
    subtitle: str = "",
    points: list[str] | None = None,
    footer: str = "",
    style: str = "dark",
    icon: str = "💰",
) -> str:
    """渲染卡片 HTML"""
    html = load_template()

    # 默认值
    if not points:
        points = []
    if not footer:
        footer = "以上仅为个人分析，不构成投资建议"
    if not subtitle:
        subtitle = ""

    # 构建要点 HTML
    points_html = ""
    if points:
        points_html = '<div class="points">\n'
        for i, p in enumerate(points, 1):
            points_html += f'  <div class="point"><span class="point-num">{i}</span><span class="point-text">{p}</span></div>\n'
        points_html += "</div>"

    # 替换模板变量
    html = html.replace("{{ICON}}", icon)
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{POINTS_HTML}}", points_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


def render_minimal(title: str, subtitle: str = "", style: str = "dark") -> str:
    """渲染极简文字卡片"""
    html = load_template("minimal.html")
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)
    return html


def render_data_card(
    title: str,
    data_items: list[dict] | None = None,
    footer: str = "",
    style: str = "dark",
) -> str:
    """渲染数据可视化卡片"""
    html = load_template("data.html")

    if not data_items:
        data_items = []
    if not footer:
        footer = "数据来源：公开市场数据"

    data_html = ""
    if data_items:
        data_html = '<div class="data-grid">\n'
        for item in data_items:
            label = item.get("label", "")
            value = item.get("value", "")
            trend = item.get("trend", "")  # up, down, flat
            trend_icon = {"up": "📈", "down": "📉", "flat": "➡️"}.get(trend, "")
            data_html += f'''  <div class="data-item">
    <div class="data-value">{value} {trend_icon}</div>
    <div class="data-label">{label}</div>
  </div>\n'''
        data_html += "</div>"

    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{DATA_HTML}}", data_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


async def screenshot_html(html: str, output_path: str, width: int = 1080, height: int = 1440):
    """用 Playwright 截图"""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height})

        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=output_path, full_page=True)

        await browser.close()

    return output_path


def ensure_output_dir():
    """确保输出目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def generate_filename(prefix: str = "xhs") -> str:
    """生成文件名"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.png"


def render_table_card(
    title: str,
    headers: list[str] | None = None,
    rows: list[list[str]] | None = None,
    subtitle: str = "",
    footer: str = "",
    style: str = "dark",
) -> str:
    """渲染专业数据表格"""
    html = load_template("table.html")

    if not headers:
        headers = []
    if not rows:
        rows = []
    if not footer:
        footer = "数据来源：公开市场数据"

    table_html = '<table class="data-table">\n'

    # 表头
    if headers:
        table_html += '  <thead><tr class="table-header">\n'
        for h in headers:
            table_html += f'    <th>{h}</th>\n'
        table_html += '  </tr></thead>\n'

    # 数据行
    if rows:
        table_html += '  <tbody>\n'
        for row in rows:
            table_html += '    <tr class="table-row">\n'
            for i, cell in enumerate(row):
                # 检测涨跌标记
                cell_class = "table-cell"
                if cell.startswith("+") or cell.startswith("↑"):
                    cell_class = "table-cell cell-highlight"
                elif cell.startswith("-") or cell.startswith("↓"):
                    cell_class = "table-cell cell-warning"
                table_html += f'      <td class="{cell_class}">{cell}</td>\n'
            table_html += '    </tr>\n'
        table_html += '  </tbody>\n'

    table_html += '</table>'

    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{TABLE_HTML}}", table_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


def render_comparison_card(
    title: str,
    left_name: str = "",
    right_name: str = "",
    items: list[dict] | None = None,
    subtitle: str = "",
    footer: str = "",
    style: str = "dark",
) -> str:
    """渲染对比分析卡片"""
    html = load_template("comparison.html")

    if not items:
        items = []
    if not footer:
        footer = "以上仅为个人分析，不构成投资建议"

    compare_html = '<div class="compare-grid">\n'

    # 左列
    compare_html += '  <div class="compare-col left">\n'
    compare_html += f'    <div class="col-title">{left_name}</div>\n'
    for item in items:
        label = item.get("label", "")
        left_val = item.get("left", "")
        left_class = "item-value"
        if item.get("left_good"):
            left_class += " good"
        elif item.get("left_bad"):
            left_class += " bad"
        compare_html += f'    <div class="compare-item"><div class="item-label">{label}</div><div class="{left_class}">{left_val}</div></div>\n'
    compare_html += '  </div>\n'

    # 右列
    compare_html += '  <div class="compare-col right">\n'
    compare_html += f'    <div class="col-title">{right_name}</div>\n'
    for item in items:
        label = item.get("label", "")
        right_val = item.get("right", "")
        right_class = "item-value"
        if item.get("right_good"):
            right_class += " good"
        elif item.get("right_bad"):
            right_class += " bad"
        compare_html += f'    <div class="compare-item"><div class="item-label">{label}</div><div class="{right_class}">{right_val}</div></div>\n'
    compare_html += '  </div>\n'

    compare_html += '</div>'

    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{COMPARE_HTML}}", compare_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


def render_kpi_card(
    title: str,
    kpis: list[dict] | None = None,
    subtitle: str = "",
    footer: str = "",
    style: str = "dark",
) -> str:
    """渲染 KPI 仪表盘卡片"""
    html = load_template("kpi.html")

    if not kpis:
        kpis = []
    if not footer:
        footer = "数据来源：公开市场数据"

    kpi_html = '<div class="kpi-grid">\n'
    for kpi in kpis:
        icon = kpi.get("icon", "📊")
        label = kpi.get("label", "")
        value = kpi.get("value", "")
        change = kpi.get("change", "")
        progress = kpi.get("progress", 0)

        change_class = "kpi-change"
        if change.startswith("+") or change.startswith("↑"):
            change_class += " up"
        elif change.startswith("-") or change.startswith("↓"):
            change_class += " down"

        kpi_html += f'''  <div class="kpi-card">
    <div class="kpi-header">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
    </div>
    <div class="kpi-value">{value}</div>
    <div class="{change_class}">{change}</div>
    <div class="progress-container">
      <div class="progress-bg"><div class="progress-bar" style="width: {progress}%"></div></div>
    </div>
  </div>\n'''
    kpi_html += '</div>'

    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{KPI_HTML}}", kpi_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


def render_ranking_card(
    title: str,
    items: list[dict] | None = None,
    subtitle: str = "",
    footer: str = "",
    style: str = "dark",
) -> str:
    """渲染排行榜卡片"""
    html = load_template("ranking.html")

    if not items:
        items = []
    if not footer:
        footer = "数据来源：公开市场数据"

    # 计算最大值用于进度条
    max_val = 0
    for item in items:
        try:
            val = float(item.get("value", "0").replace(",", "").replace("%", "").replace("亿", "").replace("万", ""))
            max_val = max(max_val, abs(val))
        except:
            pass

    ranking_html = '<div class="ranking-list">\n'
    for i, item in enumerate(items):
        name = item.get("name", "")
        desc = item.get("desc", "")
        value = item.get("value", "")
        is_top = i < 3  # 前3名高亮

        # 计算进度条宽度
        try:
            val = float(value.replace(",", "").replace("%", "").replace("亿", "").replace("万", ""))
            bar_width = int((abs(val) / max_val * 100)) if max_val > 0 else 50
        except:
            bar_width = 50

        top_class = " top" if is_top else ""
        ranking_html += f'''  <div class="rank-item{top_class}">
    <div class="rank-num">{i + 1}</div>
    <div class="rank-content">
      <div class="rank-name">{name}</div>
      <div class="rank-desc">{desc}</div>
    </div>
    <div class="rank-right">
      <div class="rank-value">{value}</div>
      <div class="rank-bar-container">
        <div class="rank-bar-bg"><div class="rank-bar" style="width: {bar_width}%"></div></div>
      </div>
    </div>
  </div>\n'''
    ranking_html += '</div>'

    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{RANKING_HTML}}", ranking_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", style)
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


# ============================================================
# 专业 SVG 图表渲染引擎
# ============================================================

THEME_COLORS = {
    "dark": {
        "bg": "#111844", "card_bg": "rgba(75,86,148,0.15)",
        "text": "#EAE0CF", "text_secondary": "rgba(234,224,207,0.5)",
        "grid": "rgba(114,136,174,0.12)", "axis": "rgba(234,224,207,0.15)",
        "colors": ["#7288AE", "#4ade80", "#EAE0CF", "#f87171", "#a78bfa", "#34d399", "#fbbf24", "#f472b6"],
    },
}


def _nice_scale(v_min: float, v_max: float, ticks: int = 5):
    """计算美观的刻度范围"""
    if v_max == v_min:
        v_max = v_min + 1
    raw = (v_max - v_min) / ticks
    mag = 10 ** int(math.log10(raw)) if raw > 0 else 1
    norm = raw / mag
    if norm <= 1:
        step = 1 * mag
    elif norm <= 2:
        step = 2 * mag
    elif norm <= 5:
        step = 5 * mag
    else:
        step = 10 * mag
    lo = math.floor(v_min / step) * step
    hi = math.ceil(v_max / step) * step
    return lo, hi, step


def render_svg_line_chart(labels, datasets, style="dark"):
    """折线图 SVG"""
    t = THEME_COLORS["dark"]
    W, H = 960, 600
    ml, mr, mt, mb = 70, 30, 30, 80
    cw, ch = W - ml - mr, H - mt - mb

    all_vals = [v for ds in datasets for v in ds["values"]]
    v_min, v_max = min(all_vals), max(all_vals)
    lo, hi, step = _nice_scale(v_min, v_max)
    n = len(labels)
    x_step = cw / max(n - 1, 1)

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT_FAMILY}">\n'

    # 网格线 + Y 轴刻度
    y = lo
    while y <= hi + step * 0.01:
        py = mt + ch - (y - lo) / (hi - lo) * ch
        svg += f'<line x1="{ml}" y1="{py:.1f}" x2="{W - mr}" y2="{py:.1f}" stroke="{t["grid"]}" stroke-width="1"/>\n'
        svg += f'<text x="{ml - 12}" y="{py + 5:.1f}" text-anchor="end" fill="{t["text_secondary"]}" font-size="13">{y:g}</text>\n'
        y += step

    # X 轴标签
    for i, label in enumerate(labels):
        x = ml + i * x_step
        svg += f'<text x="{x:.1f}" y="{H - mb + 30}" text-anchor="middle" fill="{t["text_secondary"]}" font-size="13">{label}</text>\n'

    # 数据线
    for di, ds in enumerate(datasets):
        color = ds.get("color", t["colors"][di % len(t["colors"])])
        vals = ds["values"]
        pts = []
        for i, v in enumerate(vals):
            x = ml + i * x_step
            y = mt + ch - (v - lo) / (hi - lo) * ch
            pts.append(f"{x:.1f},{y:.1f}")
        svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n'
        for i, v in enumerate(vals):
            x = ml + i * x_step
            y = mt + ch - (v - lo) / (hi - lo) * ch
            svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="{t["bg"]}" stroke-width="2"/>\n'

    # 坐标轴线
    svg += f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'
    svg += f'<line x1="{ml}" y1="{mt + ch}" x2="{W - mr}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'

    # 图例
    lx = ml
    ly = H - 20
    for di, ds in enumerate(datasets):
        color = ds.get("color", t["colors"][di % len(t["colors"])])
        svg += f'<circle cx="{lx}" cy="{ly}" r="5" fill="{color}"/>\n'
        svg += f'<text x="{lx + 10}" y="{ly + 5}" fill="{t["text"]}" font-size="14">{ds["label"]}</text>\n'
        lx += len(ds["label"]) * 14 + 30

    svg += '</svg>'
    return svg


def render_svg_area_chart(labels, datasets, style="dark"):
    """面积图 SVG"""
    t = THEME_COLORS["dark"]
    W, H = 960, 600
    ml, mr, mt, mb = 70, 30, 30, 80
    cw, ch = W - ml - mr, H - mt - mb

    all_vals = [v for ds in datasets for v in ds["values"]]
    v_min, v_max = min(all_vals), max(all_vals)
    lo, hi, step = _nice_scale(v_min, v_max)
    n = len(labels)
    x_step = cw / max(n - 1, 1)

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT_FAMILY}">\n'

    # 渐变定义
    for di, ds in enumerate(datasets):
        color = ds.get("color", t["colors"][di % len(t["colors"])])
        svg += f'<defs><linearGradient id="ag{di}" x1="0" y1="0" x2="0" y2="1">\n'
        svg += f'  <stop offset="0%" stop-color="{color}" stop-opacity="0.3"/>\n'
        svg += f'  <stop offset="100%" stop-color="{color}" stop-opacity="0.02"/>\n'
        svg += f'</linearGradient></defs>\n'

    # 网格线 + Y 轴刻度
    y = lo
    while y <= hi + step * 0.01:
        py = mt + ch - (y - lo) / (hi - lo) * ch
        svg += f'<line x1="{ml}" y1="{py:.1f}" x2="{W - mr}" y2="{py:.1f}" stroke="{t["grid"]}" stroke-width="1"/>\n'
        svg += f'<text x="{ml - 12}" y="{py + 5:.1f}" text-anchor="end" fill="{t["text_secondary"]}" font-size="13">{y:g}</text>\n'
        y += step

    # X 轴标签
    for i, label in enumerate(labels):
        x = ml + i * x_step
        svg += f'<text x="{x:.1f}" y="{H - mb + 30}" text-anchor="middle" fill="{t["text_secondary"]}" font-size="13">{label}</text>\n'

    # 面积 + 折线
    base_y = mt + ch - (0 - lo) / (hi - lo) * ch if lo <= 0 <= hi else mt + ch
    for di, ds in enumerate(datasets):
        color = ds.get("color", t["colors"][di % len(t["colors"])])
        vals = ds["values"]
        pts = [(ml + i * x_step, mt + ch - (v - lo) / (hi - lo) * ch) for i, v in enumerate(vals)]
        area_pts = pts + [(pts[-1][0], base_y), (pts[0][0], base_y)]
        area_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in area_pts)
        svg += f'<polygon points="{area_str}" fill="url(#ag{di})"/>\n'
        line_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        svg += f'<polyline points="{line_str}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n'
        for x, y in pts:
            svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}" stroke="{t["bg"]}" stroke-width="2"/>\n'

    # 坐标轴
    svg += f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'
    svg += f'<line x1="{ml}" y1="{mt + ch}" x2="{W - mr}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'

    # 图例
    lx, ly = ml, H - 20
    for di, ds in enumerate(datasets):
        color = ds.get("color", t["colors"][di % len(t["colors"])])
        svg += f'<circle cx="{lx}" cy="{ly}" r="5" fill="{color}"/>\n'
        svg += f'<text x="{lx + 10}" y="{ly + 5}" fill="{t["text"]}" font-size="14">{ds["label"]}</text>\n'
        lx += len(ds["label"]) * 14 + 30

    svg += '</svg>'
    return svg


def render_svg_bar_chart(labels, datasets, style="dark"):
    """柱状图 SVG"""
    t = THEME_COLORS["dark"]
    W, H = 960, 600
    ml, mr, mt, mb = 70, 30, 30, 80
    cw, ch = W - ml - mr, H - mt - mb

    all_vals = [v for ds in datasets for v in ds["values"]]
    v_min, v_max = min(0, min(all_vals)), max(all_vals)
    lo, hi, step = _nice_scale(v_min, v_max)
    n = len(labels)
    nd = len(datasets)
    group_w = cw / n
    bar_w = group_w * 0.7 / nd
    gap = group_w * 0.15

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT_FAMILY}">\n'

    # 网格线 + Y 轴刻度
    y = lo
    while y <= hi + step * 0.01:
        py = mt + ch - (y - lo) / (hi - lo) * ch
        svg += f'<line x1="{ml}" y1="{py:.1f}" x2="{W - mr}" y2="{py:.1f}" stroke="{t["grid"]}" stroke-width="1"/>\n'
        svg += f'<text x="{ml - 12}" y="{py + 5:.1f}" text-anchor="end" fill="{t["text_secondary"]}" font-size="13">{y:g}</text>\n'
        y += step

    # 柱子
    base_y = mt + ch - (0 - lo) / (hi - lo) * ch if lo < 0 else mt + ch
    for i, label in enumerate(labels):
        gx = ml + i * group_w
        svg += f'<text x="{gx + group_w / 2:.1f}" y="{H - mb + 30}" text-anchor="middle" fill="{t["text_secondary"]}" font-size="13">{label}</text>\n'
        for di, ds in enumerate(datasets):
            color = ds.get("color", t["colors"][di % len(t["colors"])])
            v = ds["values"][i]
            bx = gx + gap + di * bar_w
            by = mt + ch - (v - lo) / (hi - lo) * ch
            bh = abs(base_y - by)
            top = min(by, base_y)
            svg += f'<rect x="{bx:.1f}" y="{top:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="4" fill="{color}"/>\n'
            svg += f'<text x="{bx + bar_w / 2:.1f}" y="{top - 8:.1f}" text-anchor="middle" fill="{t["text"]}" font-size="12" font-weight="600">{v:g}</text>\n'

    # 坐标轴
    svg += f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'
    svg += f'<line x1="{ml}" y1="{base_y:.1f}" x2="{W - mr}" y2="{base_y:.1f}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'

    # 图例
    lx, ly = ml, H - 20
    for di, ds in enumerate(datasets):
        color = ds.get("color", t["colors"][di % len(t["colors"])])
        svg += f'<rect x="{lx}" y="{ly - 6}" width="14" height="14" rx="3" fill="{color}"/>\n'
        svg += f'<text x="{lx + 20}" y="{ly + 5}" fill="{t["text"]}" font-size="14">{ds["label"]}</text>\n'
        lx += len(ds["label"]) * 14 + 40

    svg += '</svg>'
    return svg


def render_svg_mixed_chart(labels, datasets, style="dark"):
    """柱状+折线混合图 SVG（双 Y 轴）"""
    t = THEME_COLORS["dark"]
    W, H = 960, 600
    ml, mr, mt, mb = 70, 60, 30, 80
    cw, ch = W - ml - mr, H - mt - mb

    bar_ds = [ds for ds in datasets if ds.get("type", "bar") == "bar"]
    line_ds = [ds for ds in datasets if ds.get("type") == "line"]
    n = len(labels)
    group_w = cw / n
    nb = len(bar_ds)
    bar_w = group_w * 0.6 / max(nb, 1)
    gap = group_w * 0.2

    # 柱状 Y 轴
    bar_vals = [v for ds in bar_ds for v in ds["values"]] or [0]
    blo, bhi, bstep = _nice_scale(min(0, min(bar_vals)), max(bar_vals))
    # 折线 Y 轴
    if line_ds:
        line_vals = [v for ds in line_ds for v in ds["values"]]
        llo, lhi, lstep = _nice_scale(min(line_vals), max(line_vals))
    else:
        llo, lhi, lstep = blo, bhi, bstep

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT_FAMILY}">\n'

    # 左侧网格 + Y 轴（柱状）
    y = blo
    while y <= bhi + bstep * 0.01:
        py = mt + ch - (y - blo) / (bhi - blo) * ch
        svg += f'<line x1="{ml}" y1="{py:.1f}" x2="{W - mr}" y2="{py:.1f}" stroke="{t["grid"]}" stroke-width="1"/>\n'
        svg += f'<text x="{ml - 12}" y="{py + 5:.1f}" text-anchor="end" fill="{t["text_secondary"]}" font-size="13">{y:g}</text>\n'
        y += bstep

    # 右侧 Y 轴（折线）
    if line_ds:
        y = llo
        while y <= lhi + lstep * 0.01:
            py = mt + ch - (y - llo) / (lhi - llo) * ch
            svg += f'<text x="{W - mr + 12}" y="{py + 5:.1f}" text-anchor="start" fill="{t["text_secondary"]}" font-size="13">{y:g}</text>\n'
            y += lstep

    # 柱子
    base_y = mt + ch - (0 - blo) / (bhi - blo) * ch if blo < 0 else mt + ch
    for i, label in enumerate(labels):
        gx = ml + i * group_w
        svg += f'<text x="{gx + group_w / 2:.1f}" y="{H - mb + 30}" text-anchor="middle" fill="{t["text_secondary"]}" font-size="13">{label}</text>\n'
        for di, ds in enumerate(bar_ds):
            color = ds.get("color", t["colors"][di % len(t["colors"])])
            v = ds["values"][i]
            bx = gx + gap + di * bar_w
            by = mt + ch - (v - blo) / (bhi - blo) * ch
            bh = abs(base_y - by)
            top = min(by, base_y)
            svg += f'<rect x="{bx:.1f}" y="{top:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="4" fill="{color}"/>\n'

    # 折线
    x_step = group_w
    for di, ds in enumerate(line_ds):
        color = ds.get("color", t["colors"][len(bar_ds) + di % len(t["colors"])])
        pts = []
        for i, v in enumerate(ds["values"]):
            x = ml + i * x_step + x_step / 2
            y = mt + ch - (v - llo) / (lhi - llo) * ch
            pts.append(f"{x:.1f},{y:.1f}")
        svg += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n'
        for i, v in enumerate(ds["values"]):
            x = ml + i * x_step + x_step / 2
            y = mt + ch - (v - llo) / (lhi - llo) * ch
            svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="{t["bg"]}" stroke-width="2"/>\n'

    # 坐标轴
    svg += f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'
    svg += f'<line x1="{ml}" y1="{base_y:.1f}" x2="{W - mr}" y2="{base_y:.1f}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'
    svg += f'<line x1="{W - mr}" y1="{mt}" x2="{W - mr}" y2="{mt + ch}" stroke="{t["axis"]}" stroke-width="1.5"/>\n'

    # 图例
    lx, ly = ml, H - 20
    for ds in bar_ds:
        color = ds.get("color", t["colors"][0])
        svg += f'<rect x="{lx}" y="{ly - 6}" width="14" height="14" rx="3" fill="{color}"/>\n'
        svg += f'<text x="{lx + 20}" y="{ly + 5}" fill="{t["text"]}" font-size="14">{ds["label"]}</text>\n'
        lx += len(ds["label"]) * 14 + 40
    for di, ds in enumerate(line_ds):
        color = ds.get("color", t["colors"][len(bar_ds) + di % len(t["colors"])])
        svg += f'<circle cx="{lx}" cy="{ly}" r="5" fill="{color}"/>\n'
        svg += f'<text x="{lx + 10}" y="{ly + 5}" fill="{t["text"]}" font-size="14">{ds["label"]}</text>\n'
        lx += len(ds["label"]) * 14 + 30

    svg += '</svg>'
    return svg


def render_svg_pie_chart(items, style="dark", donut=False):
    """饼图/环形图 SVG"""
    t = THEME_COLORS["dark"]
    W, H = 960, 600
    cx, cy, r = W / 2, 260, 180
    total = sum(it["value"] for it in items)

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT_FAMILY}">\n'

    start_angle = -90
    for i, it in enumerate(items):
        color = it.get("color", t["colors"][i % len(t["colors"])])
        pct = it["value"] / total
        angle = pct * 360
        end_angle = start_angle + angle
        large = 1 if angle > 180 else 0

        sr = math.radians(start_angle)
        er = math.radians(end_angle)
        x1 = cx + r * math.cos(sr)
        y1 = cy + r * math.sin(sr)
        x2 = cx + r * math.cos(er)
        y2 = cy + r * math.sin(er)

        if donut:
            ri = r * 0.58
            x3 = cx + ri * math.cos(er)
            y3 = cy + ri * math.sin(er)
            x4 = cx + ri * math.cos(sr)
            y4 = cy + ri * math.sin(sr)
            svg += f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large},1 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} A{ri},{ri} 0 {large},0 {x4:.1f},{y4:.1f} Z" fill="{color}" stroke="{t["bg"]}" stroke-width="2"/>\n'
        else:
            svg += f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large},1 {x2:.1f},{y2:.1f} Z" fill="{color}" stroke="{t["bg"]}" stroke-width="2"/>\n'

        # 百分比标签
        mid = math.radians(start_angle + angle / 2)
        lr = r * (0.72 if donut else 0.65)
        lx = cx + lr * math.cos(mid)
        ly = cy + lr * math.sin(mid)
        if pct >= 0.06:
            svg += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" fill="#fff" font-size="15" font-weight="700">{pct * 100:.0f}%</text>\n'

        start_angle = end_angle

    # 环形图中心文字
    if donut:
        svg += f'<text x="{cx}" y="{cy - 8}" text-anchor="middle" fill="{t["text"]}" font-size="28" font-weight="900">总计</text>\n'
        svg += f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" fill="{t["text_secondary"]}" font-size="16">{total:g}</text>\n'

    # 图例（两列布局）
    cols = 2
    col_w = 260
    lx0 = cx - col_w * cols / 2 + 20
    ly0 = cy + r + 50
    for i, it in enumerate(items):
        color = it.get("color", t["colors"][i % len(t["colors"])])
        col = i % cols
        row = i // cols
        x = lx0 + col * col_w
        y = ly0 + row * 32
        svg += f'<circle cx="{x}" cy="{y}" r="6" fill="{color}"/>\n'
        pct = it["value"] / total * 100
        svg += f'<text x="{x + 16}" y="{y + 5}" fill="{t["text"]}" font-size="14">{it["label"]}  {it["value"]:g} ({pct:.0f}%)</text>\n'

    svg += '</svg>'
    return svg


def render_svg_donut_chart(items, style="dark"):
    """环形图 SVG（饼图的 donut 模式）"""
    return render_svg_pie_chart(items, style, donut=True)


def _build_description_html(desc):
    """从描述数据构建 HTML"""
    if not desc:
        return ""

    parts = ['<div class="description">']

    if isinstance(desc, str):
        # 简单字符串
        parts.append(f'<p class="desc-text">{desc}</p>')
    elif isinstance(desc, dict):
        # 结构化描述
        if desc.get("title"):
            parts.append(f'<div class="desc-title">{desc["title"]}</div>')
        if desc.get("text"):
            parts.append(f'<p class="desc-text">{desc["text"]}</p>')
        if desc.get("points"):
            parts.append('<ul class="desc-list">')
            for pt in desc["points"]:
                if isinstance(pt, dict):
                    label = pt.get("label", "")
                    value = pt.get("value", "")
                    parts.append(f'<li class="desc-item"><span class="desc-highlight">{label}</span> {value}</li>')
                else:
                    parts.append(f'<li class="desc-item">{pt}</li>')
            parts.append('</ul>')
    elif isinstance(desc, list):
        # 简单列表
        parts.append('<ul class="desc-list">')
        for item in desc:
            parts.append(f'<li class="desc-item">{item}</li>')
        parts.append('</ul>')

    parts.append('</div>')
    return "\n    ".join(parts)


def render_chart(title, chart_type, chart_data, subtitle="", footer="", description=None):
    """渲染图表卡片 HTML"""
    html = load_template("chart.html")

    renderers = {
        "line": lambda: render_svg_line_chart(chart_data["labels"], chart_data["datasets"]),
        "area": lambda: render_svg_area_chart(chart_data["labels"], chart_data["datasets"]),
        "bar": lambda: render_svg_bar_chart(chart_data["labels"], chart_data["datasets"]),
        "mixed": lambda: render_svg_mixed_chart(chart_data["labels"], chart_data["datasets"]),
        "pie": lambda: render_svg_pie_chart(chart_data["items"]),
        "donut": lambda: render_svg_donut_chart(chart_data["items"]),
    }

    renderer = renderers.get(chart_type)
    if not renderer:
        print(f"❌ 不支持的图表类型: {chart_type}，可选: {', '.join(renderers.keys())}")
        sys.exit(1)

    chart_svg = renderer()
    desc_html = _build_description_html(description)

    if not footer:
        footer = "以上数据仅供参考，不构成投资建议"

    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SUBTITLE}}", subtitle)
    html = html.replace("{{CHART_HTML}}", chart_svg)
    html = html.replace("{{DESCRIPTION}}", desc_html)
    html = html.replace("{{FOOTER}}", footer)
    html = html.replace("{{STYLE_CLASS}}", "dark")
    html = html.replace("{{FONT_FACE}}", FONT_FACE_CSS)
    html = html.replace("{{FONT_FAMILY}}", FONT_FAMILY)

    return html


def render_post_text(post_data):
    """从帖子配置生成配套文案文本"""
    lines = []

    # 标题
    titles = post_data.get("titles", [])
    if titles:
        lines.append("标题备选：")
        for i, t in enumerate(titles, 1):
            lines.append(f"  {i}. {t}")
        lines.append("")

    # 正文
    body = post_data.get("body", "")
    if body:
        if isinstance(body, list):
            lines.extend(body)
        else:
            lines.append(body)
        lines.append("")

    # 标签
    tags = post_data.get("tags", [])
    if tags:
        lines.append(" ".join(tags))
        lines.append("")

    # 风险提示
    disclaimer = post_data.get("disclaimer", "")
    if disclaimer:
        lines.append(f"---")
        lines.append(disclaimer)

    return "\n".join(lines)


async def cmd_generate(config_path, output_dir):
    """生成完整帖子：图片 + 配套文案"""
    with open(config_path, "r", encoding="utf-8") as f:
        post = json.load(f)

    # 准备输出目录
    out_dir = Path(output_dir) if output_dir else ensure_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. 生成文案
    text = render_post_text(post)
    text_path = out_dir / f"xhs_{timestamp}.txt"
    text_path.write_text(text, encoding="utf-8")
    print(f"文案已生成: {text_path}")

    # 2. 生成封面图
    image_cfg = post.get("image", {})
    if image_cfg:
        tpl = image_cfg.get("template", "chart")
        chart_type = image_cfg.get("chart_type", "line")
        img_config_path = image_cfg.get("config")
        img_title = image_cfg.get("title", post.get("titles", [""])[0] if post.get("titles") else "")
        img_subtitle = image_cfg.get("subtitle", "")
        img_footer = image_cfg.get("footer", post.get("disclaimer", ""))
        description = image_cfg.get("description")

        # 加载图表数据（支持内联或外部文件）
        chart_data = {}
        if img_config_path:
            with open(img_config_path, "r", encoding="utf-8") as f:
                img_cfg = json.load(f)
            chart_data = img_cfg.get("chart_data", {})
            chart_type = img_cfg.get("chart_type", chart_type)
            description = img_cfg.get("description", description)
            img_title = img_cfg.get("title", img_title)
            img_subtitle = img_cfg.get("subtitle", img_subtitle)
            img_footer = img_cfg.get("footer", img_footer)
        else:
            chart_data = image_cfg.get("chart_data", {})

        if tpl == "chart":
            html = render_chart(img_title, chart_type, chart_data, img_subtitle, img_footer, description)
        else:
            # 文字卡片模板
            points = image_cfg.get("points", [])
            html = render_card(title=img_title, subtitle=img_subtitle, points=points, footer=img_footer, style="dark")

        img_path = out_dir / f"xhs_{timestamp}.png"
        await screenshot_html(html, str(img_path))
        print(f"封面图已生成: {img_path}")

    # 3. 输出到控制台
    print("\n" + "=" * 40)
    print(text)
    print("=" * 40)

    return str(text_path)


async def main():
    parser = argparse.ArgumentParser(description="小红书财经封面图生成器")
    subparsers = parser.add_subparsers(dest="command")

    # generate 子命令
    gen_parser = subparsers.add_parser("generate", help="生成完整帖子（图片+文案）")
    gen_parser.add_argument("config", type=str, help="帖子 JSON 配置文件")
    gen_parser.add_argument("--output-dir", type=str, help="输出目录")

    # 原有参数（向后兼容）
    parser.add_argument("--title", type=str, help="卡片标题")
    parser.add_argument("--subtitle", type=str, default="", help="副标题")
    parser.add_argument("--points", nargs="*", help="要点列表")
    parser.add_argument("--footer", type=str, default="", help="底部文字")
    parser.add_argument("--icon", type=str, default="💰", help="图标 emoji")
    parser.add_argument("--template", type=str, default="card", choices=["card", "minimal", "data", "table", "comparison", "kpi", "ranking", "chart"], help="模板类型")
    parser.add_argument("--chart-type", type=str, default="line", choices=["line", "bar", "pie", "donut", "area", "mixed"], help="图表类型（仅 chart 模板）")
    parser.add_argument("--config", type=str, help="JSON 配置文件路径")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--width", type=int, default=1080, help="图片宽度")
    parser.add_argument("--height", type=int, default=1440, help="图片高度")

    args = parser.parse_args()

    # generate 子命令
    if args.command == "generate":
        await cmd_generate(args.config, args.output_dir)
        return

    # 从 JSON 配置加载
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        args.title = config.get("title", args.title)
        args.subtitle = config.get("subtitle", args.subtitle)
        args.points = config.get("points", args.points)
        args.footer = config.get("footer", args.footer)
        args.icon = config.get("icon", args.icon)
        args.template = config.get("template", args.template)
        args.chart_type = config.get("chart_type", args.chart_type)

    if not args.title:
        print("❌ 必须提供 --title 参数")
        sys.exit(1)

    # 渲染 HTML
    if args.template == "minimal":
        html = render_minimal(args.title, args.subtitle, "dark")
    elif args.template == "data":
        # 从 config 加载 data_items
        data_items = []
        if args.config:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
            data_items = config.get("data_items", [])
        html = render_data_card(args.title, data_items, args.footer, "dark")
    elif args.template == "table":
        # 从 config 加载表格数据
        headers = []
        rows = []
        if args.config:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
            headers = config.get("headers", [])
            rows = config.get("rows", [])
        html = render_table_card(args.title, headers, rows, args.subtitle, args.footer, "dark")
    elif args.template == "comparison":
        # 从 config 加载对比数据
        left_name = ""
        right_name = ""
        items = []
        if args.config:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
            left_name = config.get("left_name", "")
            right_name = config.get("right_name", "")
            items = config.get("compare_items", [])
        html = render_comparison_card(args.title, left_name, right_name, items, args.subtitle, args.footer, "dark")
    elif args.template == "kpi":
        # 从 config 加载 KPI 数据
        kpis = []
        if args.config:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
            kpis = config.get("kpis", [])
        html = render_kpi_card(args.title, kpis, args.subtitle, args.footer, "dark")
    elif args.template == "ranking":
        # 从 config 加载排行数据
        items = []
        if args.config:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
            items = config.get("ranking_items", [])
        html = render_ranking_card(args.title, items, args.subtitle, args.footer, "dark")
    elif args.template == "chart":
        # 从 config 加载图表数据
        chart_data = {}
        chart_type = args.chart_type
        description = None
        if args.config:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
            chart_data = config.get("chart_data", {})
            chart_type = config.get("chart_type", chart_type)
            description = config.get("description")
        html = render_chart(
            title=args.title,
            chart_type=chart_type,
            chart_data=chart_data,
            subtitle=args.subtitle,
            footer=args.footer,
            description=description,
        )
    else:
        html = render_card(
            title=args.title,
            subtitle=args.subtitle,
            points=args.points or [],
            footer=args.footer,
            style="dark",
            icon=args.icon,
        )

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        output_dir = ensure_output_dir()
        output_path = str(output_dir / generate_filename())

    # 截图
    print(f"🎨 正在生成封面图...")
    result = await screenshot_html(html, output_path, args.width, args.height)
    print(f"✅ 封面图已生成: {result}")
    return result


if __name__ == "__main__":
    import asyncio
    # Windows 控制台 UTF-8 支持
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    asyncio.run(main())
