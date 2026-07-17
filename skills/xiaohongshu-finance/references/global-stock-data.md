# 港股美股数据接入指南

所有函数已封装为 Python 模块，直接调用即可。

> 环境要求：**Yahoo 需要 SOCKS5 代理（127.0.0.1:1080）**，其他（新浪、腾讯、东财搜索）全部直连可用。

## 快速使用

```bash
# Yahoo K线（港股美股通用，需SOCKS5代理）
python3 scripts/global_stock_api.py yahoo --symbol ^HSI --range 10y
python3 scripts/global_stock_api.py yahoo --symbol AAPL --range 1y

# 新浪美股日K（直连，回溯至1984）
python3 scripts/global_stock_api.py sina_kline --symbol AAPL --num 2500

# 新浪实时报价
python3 scripts/global_stock_api.py sina_quote --symbol AAPL

# 腾讯实时报价
python3 scripts/global_stock_api.py tencent_quote --symbol AAPL --market us
python3 scripts/global_stock_api.py tencent_quote --symbol 00700 --market hk

# 股票搜索
python3 scripts/global_stock_api.py search --symbol AAPL
```

## import 使用

```python
from scripts.global_stock_api import global_kline_yahoo, us_kline_sina, to_chart_config

# Yahoo拉取恒生指数10年日K
klines = global_kline_yahoo("^HSI")

# 新浪拉取苹果日K
aapl = us_kline_sina("AAPL", 500)

# 转换成driver.py配置
config = to_chart_config("标题", "副标题", {"苹果": aapl})
```

## 数据源说明

| 数据源 | 函数 | 代理 | 说明 |
|--------|------|------|------|
| **新浪K线** (直连) | `us_kline_sina()` | 无 | 美股日K，回溯至1984 |
| **Yahoo K线** | `global_kline_yahoo()` | SOCKS5 | 港股+美股通用，支持10y |
| **新浪报价** (直连) | `us_quote_sina()` | 无 | 美股36字段 |
| **腾讯报价** (直连) | `global_quote_tencent()` | 无 | 美股71/港股78字段 |
| **股票搜索** (直连) | `stock_search()` | 无 | 东财，支持中英文 |
| **技术指标** | `calc_ma/macd/rsi/kdj()` | 无 | 纯Python，零依赖 |

## 常用标的

| 代码 | 名称 | K线 | 报价 |
|------|------|-----|------|
| `^HSI` | 恒生指数 | Yahoo | - |
| `^GSPC` | 标普500 | Yahoo | - |
| `^IXIC` | 纳斯达克 | Yahoo | - |
| `AAPL` | 苹果 | 新浪/Yahoo | 新浪/腾讯 |
| `TSLA` | 特斯拉 | 新浪/Yahoo | 新浪/腾讯 |
| `0700.HK` | 腾讯控股 | Yahoo | 腾讯 |
| `9988.HK` | 阿里巴巴 | Yahoo | 腾讯 |