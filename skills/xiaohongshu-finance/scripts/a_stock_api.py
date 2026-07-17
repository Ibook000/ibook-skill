#!/usr/bin/env python3
"""
A股数据API — import 或 python3 直接执行
依赖: pip install mootdx requests

快速用:
  python3 scripts/a_stock_api.py kline --symbol 510300
  python3 scripts/a_stock_api.py quote --codes 600519 300750 000001
"""
import urllib.request, json, sys

# ── mootdx K线 ──
def get_a_kline(symbol="600519", freq=6, offset=130):
    """A股月K线。freq:4=日 5=周 6=月"""
    from mootdx.quotes import Quotes
    df = Quotes.factory(market='std', timeout=15).bars(symbol=symbol, frequency=freq, offset=offset)
    return [{"date":f"{int(r.year):04d}-{int(r.month):02d}","o":float(r.open),
             "h":float(r.high),"l":float(r.low),"c":float(r.close)} for _, r in df.iterrows()]

# ── 百度K线（自带MA均线） ──
def baidu_kline(code="600519"):
    import requests
    r = requests.get("https://finance.pae.baidu.com/selfselect/getstockquotation",
        params={"all":"1","isIndex":"false","isStock":"true","newFormat":"1",
                "group":"quotation_kline_ab","finClientType":"pc","code":code,"ktype":"1"},
        headers={"Accept":"application/vnd.finance-web.v1+json",
                 "Origin":"https://gushitong.baidu.com",
                 "Referer":"https://gushitong.baidu.com/"}, timeout=10)
    md = r.json()["Result"]["newMarketData"]
    return {"keys": md["keys"], "rows": md["marketData"].split(";")}

# ── 腾讯实时报价 ──
def get_quotes(codes):
    """自动加 sh/sz/bj/hk/us 前缀"""
    prefixed = []
    for c in codes:
        if c.startswith(("hk","us")): prefixed.append(c)
        elif c.startswith("6"): prefixed.append(f"sh{c}")
        elif c.startswith("8"): prefixed.append(f"bj{c}")
        else: prefixed.append(f"sz{c}")
    url = f"https://qt.gtimg.cn/q={','.join(prefixed)}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("gbk")
    out = {}
    for line in raw.strip().split(";"):
        if "=" not in line or '"' not in line: continue
        key = line.split("=")[0].split("_")[-1]
        f = line.split('"')[1].split("~")
        if len(f) < 50: continue
        out[key] = {"name":f[1],"price":float(f[3] or 0),"high":float(f[33] or 0),
                    "low":float(f[34] or 0),"change_pct":float(f[32] or 0),
                    "pe_ttm":float(f[39] or 0),"pb":float(f[46] or 0),
                    "mcap_yi":float(f[44] or 0),"turnover":float(f[38] or 0)}
    return out

# ── 工具 ──
# ── 工具 ──
def to_chart_config(title, subtitle, data_dict, chart_type="line"):
    """{name: [{date,o,h,l,c},...]} → driver.py JSON"""
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

# ── 技术指标（纯Python，零依赖）──
def _ema(vals, period):
    k=2/(period+1); r=[vals[0]]
    for v in vals[1:]: r.append(v*k+r[-1]*(1-k))
    return r

def calc_ma(klines, periods=None):
    """MA/EMA。klines: [{date,close}]  periods默认[5,10,20,60]"""
    if periods is None: periods=[5,10,20,60]
    c=[k["close"] for k in klines]
    e12=_ema(c,12); e26=_ema(c,26)
    r=[]
    for i,k in enumerate(klines):
        row={"date":k["date"],"close":k["close"]}
        for p in periods:
            row[f"ma{p}"]=round(sum(c[i-p+1:i+1])/p,4) if i>=p-1 else None
        row["ema12"]=round(e12[i],4); row["ema26"]=round(e26[i],4)
        r.append(row)
    return r

def calc_macd(klines, fast=12, slow=26, signal=9):
    """MACD。返回 [{date,close,dif,dea,macd_hist}]"""
    c=[k["close"] for k in klines]
    df=[round(f-s,4) for f,s in zip(_ema(c,fast),_ema(c,slow))]
    de=_ema(df,signal)
    r=[]
    for i,k in enumerate(klines):
        r.append({"date":k["date"],"close":k["close"],"dif":round(df[i],4),
                  "dea":round(de[i],4),"macd_hist":round((df[i]-de[i])*2,4)})
    return r

def calc_rsi(klines, periods=None):
    """RSI。periods默认[6,12,24]  超买>70 超卖<30"""
    if periods is None: periods=[6,12,24]
    c=[k["close"] for k in klines]; ch=[0]+[c[i]-c[i-1] for i in range(1,len(c))]
    g=[max(x,0) for x in ch]; l=[max(-x,0) for x in ch]
    r=[]
    for i,k in enumerate(klines):
        row={"date":k["date"],"close":k["close"]}
        for p in periods:
            if i<p: row[f"rsi{p}"]=None; continue
            ag=sum(g[i-p+1:i+1])/p; al=sum(l[i-p+1:i+1])/p
            row[f"rsi{p}"]=100.0 if al==0 else round(100-100/(1+ag/al),2)
        r.append(row)
    return r

def calc_kdj(klines, n=9, m1=3, m2=3):
    """KDJ。K/D>80超买 <20超卖  J>100或<0极端信号"""
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
    p.add_argument("cmd",choices=["kline","quote","baidu"])
    p.add_argument("--symbol",default="510300")
    p.add_argument("--codes",nargs="*")
    a=p.parse_args()
    if a.cmd=="kline":
        d=get_a_kline(a.symbol)
        print(json.dumps({"count":len(d),"latest":d[-1]},ensure_ascii=False))
    elif a.cmd=="quote":
        d=get_quotes(a.codes or [a.symbol])
        print(json.dumps(d,ensure_ascii=False))
    elif a.cmd=="baidu":
        d=baidu_kline(a.symbol)
        print(json.dumps({"keys":d["keys"][:5],"rows":len(d["rows"])},ensure_ascii=False))