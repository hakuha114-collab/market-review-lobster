#!/usr/bin/env python3
"""
Market Review Pro - 市场数据获取脚本
支持: A股/港股/美股/日韩 全市场实时数据

Usage:
  python fetch_market_data.py              # 获取A股港股数据（默认）
  python fetch_market_data.py --market us # 获取美股数据
  python fetch_market_data.py --market all# 获取全部市场数据
  python fetch_market_data.py --date 2026-04-16
  python fetch_market_data.py --json      # 输出JSON格式
  python fetch_market_data.py --vix-only  # 仅获取VIX数据
"""

import argparse
import json
import os
import ssl
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SKILL_DIR)
PROXY_PORT = os.getenv("AUTH_GATEWAY_PORT", "19000")
PROXY_HOST = "127.0.0.1"
PROSEARCH_PATH = "/proxy/prosearch/search"
REQUEST_TIMEOUT = 15000


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def prosearch(query: str) -> dict:
    """通过 gateway 代理调用 ProSearch API"""
    body = json.dumps({"keyword": query}).encode("utf-8")
    try:
        req = urllib.request.Request(
            f"http://{PROXY_HOST}:{PROXY_PORT}{PROSEARCH_PATH}",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", "Content-Length": str(len(body))},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return {"success": True, "data": result, "query": query}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return {"success": False, "error": f"HTTP {e.code}", "detail": err_body[:200], "query": query}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"URL error: {e.reason}", "query": query}
    except Exception as e:
        return {"success": False, "error": str(e), "query": query}


def prosearch_parallel(queries: list[dict]) -> dict:
    """并行执行多个 ProSearch 查询"""
    log(f"[ProSearch] 发起 {len(queries)} 个并行查询...")
    results = {}
    for q in queries:
        label = q.get("label", q["keyword"][:20])
        log(f"  -> {q['keyword'][:55]}...")
        r = prosearch(q["keyword"])
        results[label] = r
        status = "OK" if r.get("success") else "FAIL"
        log(f"  <- [{status}] {r.get('error', 'OK')}")
    
    success_count = sum(1 for r in results.values() if r.get("success"))
    log(f"[ProSearch] 完成: {success_count}/{len(queries)} 成功")
    return {"results": results, "summary": {"total": len(queries), "success": success_count}}


def get_vix() -> dict:
    """获取 VIX 恐慌指数（调用 vix-index skill）"""
    vix_script = os.path.join(PARENT_DIR, "vix-index", "scripts", "query.py")
    if os.path.exists(vix_script):
        try:
            result = subprocess.run(
                [sys.executable, vix_script, "--mode", "quick"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    return {"success": False, "error": "vix-index skill not found"}


# ── 查询配置 ──────────────────────────────────────────────────────────

def get_ah_queries(date_str: str) -> list[dict]:
    """A股港股数据查询配置"""
    return [
        {"keyword": f"{date_str} A股收盘 上证指数 深证成指 创业板指 成交额", "label": "a_index"},
        {"keyword": f"{date_str} A股板块 资金流向 净流入 TOP5 净流出", "label": "a_sector"},
        {"keyword": f"{date_str} A股 涨停 连板 封板率 晋级率", "label": "a_limitup"},
        {"keyword": f"{date_str} 港股收盘 恒生指数 恒生科技 南向资金", "label": "hk_index"},
        {"keyword": f"{date_str} 北向资金 净流入 沪股通 深股通", "label": "northbound"},
        {"keyword": f"{date_str} 日韩股市 日经225 韩国KOSPI 收盘", "label": "jp_kr"},
    ]


def get_us_queries(date_str: str) -> list[dict]:
    """美股数据查询配置"""
    return [
        {"keyword": f"{date_str} 美股收盘 纳斯达克 标普500 道琼斯", "label": "us_index"},
        {"keyword": f"{date_str} 美股板块 资金流向 科技股 金融 能源", "label": "us_sector"},
        {"keyword": f"{date_str} 美股 恐慌指数 VIX 期权市场", "label": "us_vix"},
        {"keyword": f"{date_str} 美联储 降息 利率决议 宏观数据", "label": "us_macro"},
        {"keyword": f"{date_str} 美股 热门股票 苹果 英伟达 特斯拉 涨跌", "label": "us_hot"},
        {"keyword": f"{date_str} 华尔街 机构评级 分析师 报告", "label": "us_analyst"},
    ]


def fetch_market_data(market="ah", date_str=None, output_json=False):
    """主入口"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    market_labels = {"us": "美股", "ah": "A股港股", "all": "全部"}
    
    log(f"Market Review Pro 数据获取")
    log(f"  市场: {market_labels.get(market, market)}")
    log(f"  日期: {date_str}")
    log(f"  Gateway: {PROXY_HOST}:{PROXY_PORT}")
    log("=" * 60)
    
    output = {"timestamp": now, "date": date_str, "market": market, "data": {}}
    
    if market in ("us", "all"):
        log("[美股数据]")
        log("[1/7] VIX 恐慌指数...")
        vix = get_vix()
        if vix.get("success"):
            price = vix["data"].get("vix", {}).get("price", "N/A")
            log(f"    VIX = {price}")
        else:
            log(f"    VIX 获取失败: {vix.get('error')}")
        output["data"]["vix"] = vix
        
        log("[2/7] 美股 T日数据...")
        output["data"]["us"] = prosearch_parallel(get_us_queries(date_str))
        
        log("[3/7] 美股 T-1 数据...")
        t1 = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        output["data"]["us_t1"] = prosearch_parallel(get_us_queries(t1))
    
    if market in ("ah", "all"):
        log("[A股港股数据]")
        log("[4/7] A股港股 T日数据...")
        output["data"]["ah"] = prosearch_parallel(get_ah_queries(date_str))
        
        log("[5/7] A股港股 T-1 数据...")
        t1 = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        output["data"]["ah_t1"] = prosearch_parallel(get_ah_queries(t1))
    
    # 汇总
    log("=" * 60)
    total_s, total_n = 0, 0
    for key in output["data"]:
        r = output["data"][key]
        if isinstance(r, dict) and "summary" in r:
            total_s += r["summary"].get("success", 0)
            total_n += r["summary"].get("total", 0)
    log(f"[汇总] {total_s}/{total_n} 查询成功 ({total_s/total_n*100:.0f}%)" if total_n else "[汇总] 无数据")
    
    # 保存（UTF-8，避免 GBK 编码问题）
    data_dir = os.path.join(SKILL_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_file = os.path.join(data_dir, f"market_data_{date_str.replace('-','')}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    log(f"[保存] -> {out_file}")
    
    if output_json:
        # stdout 可能被 PowerShell GBK 截断，改为输出到文件
        print(f"[JSON] 已保存到: {out_file}")
    
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market Review Pro - 市场数据获取")
    parser.add_argument("--market", "-m", default="ah", choices=["us", "ah", "all"], help="市场")
    parser.add_argument("--date", "-d", default=None, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--json", "-j", action="store_true", help="输出JSON格式")
    parser.add_argument("--vix-only", "-v", action="store_true", help="仅获取VIX数据")
    args = parser.parse_args()
    
    if args.vix_only:
        result = get_vix()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        fetch_market_data(market=args.market, date_str=args.date, output_json=args.json)
