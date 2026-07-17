# A股数据接入指南

所有函数已封装为 Python 模块，直接调用即可。

> 环境要求：全部直连，无需代理。mootdx 走 TCP 7709，百度/腾讯走 HTTP。

---

## 快速使用

```bash
# 月K线（freq: 4=日 5=周 6=月）
python3 scripts/a_stock_api.py kline --symbol 510300

# 实时报价
python3 scripts/a_stock_api.py quote --codes 600519 300750 000001

# 百度K线（自带MA5/10/20）
python3 scripts/a_stock_api.py baidu --symbol 600519
```

## import 使用

```python
from scripts.a_stock_api import get_a_kline, get_quotes, to_chart_config

klines = get_a_kline("510300", freq=6, offset=130)
quotes = get_quotes(["000001", "600519"])
config = to_chart_config("走势图", "说明", {"沪深300ETF": klines})
```

## 数据源

| 数据源 | 函数 | 说明 |
|--------|------|------|
| mootdx (直连) | `get_a_kline()` | 通达信TCP，不封IP，offset上限800 |
| 百度股市通 (直连) | `baidu_kline()` | 自带MA5/MA10/MA20 |
| 腾讯财经 (直连) | `get_quotes()` | PE/PB/市值/换手率 |
| 技术指标 | `calc_ma/macd/rsi/kdj()` | 纯Python，零依赖 |

## 常用标的

| 代码 | 名称 | K线 | 报价 |
|------|------|-----|------|
| `510300` | 沪深300ETF | 有 | 有 |
| `600519` | 贵州茅台 | 有 | 有 |
| `300750` | 宁德时代 | 有 | 有 |
| `000001` | 上证指数 | 无 | 有 |
| `000300` | 沪深300 | 无 | 有 |