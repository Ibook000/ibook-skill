#!/usr/bin/env python3
"""
港股美股数据API — import 或 python3 直接执行
依赖: pip install requests PySocks

快速用:
  python3 scripts/global_stock_api.py yahoo --symbol ^HSI --range 1y
  python3 scripts/global_stock_api.py sina_quote --symbol AAPL
  python3 scripts/global_stock_api.py tencent_quote --symbol AAPL --market us
"""
import re, json, sys

PROXY = {'https': 'socks5://127.0.0.1:1080'}
def us_kline_sina(ticker="AAPL", num=2500):
    import requests
    r = requests.get(
        "https://stock.finance.sina.com.cn/usstock/api/jsonp.php/var/US_MinKService.getDailyK",
        params={"symbol": ticker.upper(), "num": num},
        headers={"Referer": "https://finance.sina.com.cn/"}, timeout=15)
    m = re.search(r'\((\[.+\])\)', r.text)
    return [{"date":i.get("d"),"o":float(i.get("o",0)),"h":float(i.get("h",0)),
             "l":float(i.get("l",0)),"c":float(i.get("c",0))}
            for i in __import__('json').loads(m.group(1))] if m else []

# ── 港股/美股K线 · Yahoo（需SOCKS5）──
def global_kline_yahoo(symbol="^HSI", range_="10y"):
    import requests
    from datetime import datetime as dt
    r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
        params={"interval":"1d","range":range_},
        headers={"User-Agent":"Mozilla/5.0"}, proxies=PROXY, timeout=30)
    chart = r.json()["chart"]["result"][0]
    ts, q = chart["timestamp"], chart["indicators"]["quote"][0]
    out = []
    for i,t in enumerate(ts):
        if not q["close"][i]: continue
        out.append({"date":dt.fromtimestamp(t).strftime("%Y-%m-%d"),
                    "o":float(q["open"][i] or q["close"][i]),
                    "h":float(q["high"][i] or q["close"][i]),
                    "l":float(q["low"][i] or q["close"][i]),
                    "c":float(q["close"][i])})
    return out

# ── 美股/港股报价 · 新浪 ──
def us_quote_sina(ticker="AAPL"):
    import requests
    r = requests.get(f"https://hq.sinajs.cn/list=gb_{ticker.lower()}",
        headers={"Referer":"https://finance.sina.com.cn/"}, timeout=10)
    r.encoding = "gbk"
    m = re.search(r'\"(.+)\"', r.text)
    if not m: return {}
    f = m.group(1).split(",")
    if len(f) < 30: return {}
    return {"name":f[0],"price":float(f[1]),"change_pct":float(f[2]),
            "high":float(f[6]),"low":float(f[7]),
            "high_52w":float(f[8] or 0),"low_52w":float(f[9] or 0),
            "market_cap":float(f[12] or 0),"pe":float(f[14] or 0)}

# ── 美股/港股报价 · 腾讯 ──
def global_quote_tencent(ticker="AAPL", market="us"):
    import requests
    prefix = "us" if market == "us" else "r_hk"
    r = requests.get(f"https://qt.gtimg.cn/q={prefix}{ticker}", timeout=10)
    r.encoding = "gbk"
    m = re.search(r'\"(.+)\"', r.text)
    if not m: return {}
    f = m.group(1).split("~")
    if len(f) < 50: return {}
    return {"name":f[1],"price":float(f[3] or 0),"high":float(f[33] or 0),
            "low":float(f[34] or 0),"high_52w":float(f[35] or 0),"low_52w":float(f[36] or 0),
            "change_pct":float(f[32] or 0),"market_cap":float(f[44] or 0),"pe":float(f[53] or 0)}

# ── 工具 ──
def to_chart_config(title, subtitle, data_dict, chart_type="line"):
    colors=["#F44336","#FF9800","#2196F3","#4CAF50","#E91E63"]
    labels=sorted(set(d for v in data_dict.values() for k in v for d in [k["date"]]))
    ds,dc=[],[]
    for i,(n,kl) in enumerate(data_dict.items()):
        lk={k["date"]:k["c"] for k in kl}; b=next(iter(lk.values())); vs=[]
        for d in labels:
            p=b if not vs else vs[-1]; vs.append(round(lk.get(d,p)/b*100,2))
        ds.append({"label":n,"color":colors[i%5],"values":vs})
        dc.append({"label":f"{n}:","value":f"{round((vs[-1]/100-1)*100,2):+.2f}%"})
    return {"title":title,"subtitle":subtitle,"chart_type":chart_type,
            "footer":"不构成投资建议","description":{"title":"累计涨跌幅","points":dc},
            "chart_data":{"labels":labels,"datasets":ds}}

def daily_to_monthly(data):
    m={}
    for i,d in enumerate(data["dates"]):
        k=d[:7]; v=data["values"][i]
        if k not in m: m[k]={"o":v["o"],"h":0,"l":9e9,"c":0,"n":0}
        m[k]["h"]=max(m[k]["h"],v["h"]); m[k]["l"]=min(m[k]["l"],v["l"])
        m[k]["c"]=v["c"]; m[k]["n"]+=1
    f={k:v for k,v in sorted(m.items()) if v["n"]>=5}
    return {"dates":list(f.keys()),"values":list(f.values())}

# ── 股票搜索（东财，全球市场）──
def stock_search(keyword: str, count: int = 10) -> list[dict]:
    """支持中英文，返回 {code, name, mkt_num, market_name}
    mkt_num: 105=NASDAQ 106=NYSE 107=US_OTHER 116=HK"""
    import requests
    r = requests.get("https://searchapi.eastmoney.com/api/suggest/get",
        params={"input":keyword,"type":14,"token":"D43BF722C8E33BDC906FB84D85E326E8","count":count},
        timeout=10)
    items = r.json().get("QuotationCodeTable",{}).get("Data",[])
    out = []
    mkt_map = {"105":"NASDAQ","106":"NYSE","107":"US_OTHER","116":"HK"}
    for s in items:
        m = str(s.get("MktNum",""))
        if m not in mkt_map: continue
        out.append({"code":s.get("Code"),"name":s.get("Name"),"mkt_num":int(m),"market_name":mkt_map[m]})
    return out

# ── 技术指标（纯Python，零依赖）──
def _ema(vals, period):
    k=2/(period+1); r=[vals[0]]
    for v in vals[1:]: r.append(v*k+r[-1]*(1-k))
    return r

def calc_ma(klines, periods=None):
    if periods is None: periods=[5,10,20,60]
    c=[k["close"] for k in klines]; e12=_ema(c,12); e26=_ema(c,26); r=[]
    for i,k in enumerate(klines):
        row={"date":k["date"],"close":k["close"]}
        for p in periods: row[f"ma{p}"]=round(sum(c[i-p+1:i+1])/p,4) if i>=p-1 else None
        row["ema12"]=round(e12[i],4); row["ema26"]=round(e26[i],4); r.append(row)
    return r

def calc_macd(klines, fast=12, slow=26, signal=9):
    c=[k["close"] for k in klines]
    df=[round(f-s,4) for f,s in zip(_ema(c,fast),_ema(c,slow))]
    de=_ema(df,signal)
    return [{"date":k["date"],"close":k["close"],"dif":round(df[i],4),
             "dea":round(de[i],4),"macd_hist":round((df[i]-de[i])*2,4)} for i,k in enumerate(klines)]

def calc_rsi(klines, periods=None):
    if periods is None: periods=[6,12,24]
    c=[k["close"] for k in klines]; ch=[0]+[c[i]-c[i-1] for i in range(1,len(c))]
    g=[max(x,0) for x in ch]; l=[max(-x,0) for x in ch]; r=[]
    for i,k in enumerate(klines):
        row={"date":k["date"],"close":k["close"]}
        for p in periods:
            if i<p: row[f"rsi{p}"]=None; continue
            ag=sum(g[i-p+1:i+1])/p; al=sum(l[i-p+1:i+1])/p
            row[f"rsi{p}"]=100.0 if al==0 else round(100-100/(1+ag/al),2)
        r.append(row)
    return r

def calc_kdj(klines, n=9, m1=3, m2=3):
    kv=dv=50.0; r=[]
    for i,k in enumerate(klines):
        if i<n-1: r.append({"date":k["date"],"close":k["close"],"k":None,"d":None,"j":None}); continue
        w=klines[i-n+1:i+1]; hn=max(x["high"] for x in w); ln=min(x["low"] for x in w)
        rsv=(k["close"]-ln)/(hn-ln)*100 if hn!=ln else 50.0
        kv=(1/m1)*rsv+(1-1/m1)*kv; dv=(1/m2)*kv+(1-1/m2)*dv
        r.append({"date":k["date"],"close":k["close"],"k":round(kv,2),"d":round(dv,2),"j":round(3*kv-2*dv,2)})
    return r

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("cmd",choices=["yahoo","sina_kline","sina_quote","tencent_quote","search"])
    p.add_argument("--symbol",default="^HSI")
    p.add_argument("--range",default="1y")
    p.add_argument("--market",default="us")
    p.add_argument("--num",type=int,default=2500)
    a=p.parse_args()
    if a.cmd=="yahoo":
        d=global_kline_yahoo(a.symbol,a.range)
        print(json.dumps({"count":len(d),"latest":d[-1]},ensure_ascii=False))
    elif a.cmd=="sina_kline":
        d=us_kline_sina(a.symbol,a.num)
        print(json.dumps({"count":len(d),"latest":d[-1]},ensure_ascii=False))
    elif a.cmd=="sina_quote":
        d=us_quote_sina(a.symbol)
        print(json.dumps(d,ensure_ascii=False))
    elif a.cmd=="tencent_quote":
        d=global_quote_tencent(a.symbol,a.market)
        print(json.dumps(d,ensure_ascii=False))
    elif a.cmd=="search":
        d=stock_search(a.symbol)
        print(json.dumps(d,ensure_ascii=False))