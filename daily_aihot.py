"""
每日 AI 热点获取脚本
从 aihot.virxact.com 获取今日 AI 热点精选，格式化输出供选题使用。
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BASE_URL = "https://aihot.virxact.com/api/public"

CATEGORY_MAP = {
    "ai-models": "模型发布/更新",
    "ai-products": "产品发布/更新",
    "industry": "行业动态",
    "paper": "论文研究",
    "tip": "技巧与观点",
}

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_selected_items(hours=24, take=50):
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"{BASE_URL}/items?mode=selected&since={urllib.parse.quote(since)}&take={take}"
    return fetch_json(url)

def get_daily():
    return fetch_json(f"{BASE_URL}/daily")

def format_time(iso_str):
    if not iso_str:
        return ""
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    bj_tz = timezone(timedelta(hours=8))
    bj_time = dt.astimezone(bj_tz)
    now = datetime.now(bj_tz)
    diff = now - bj_time
    if diff.total_seconds() < 3600:
        return f"{int(diff.total_seconds() / 60)} 分钟前"
    elif diff.total_seconds() < 86400:
        return f"{int(diff.total_seconds() / 3600)} 小时前"
    else:
        return bj_time.strftime("%m/%d %H:%M")

def format_items(data):
    items = data.get("items", [])
    if not items:
        return "暂无数据"

    grouped = {}
    for item in items:
        cat = item.get("category") or "other"
        grouped.setdefault(cat, []).append(item)

    lines = []
    idx = 1
    for cat_key in ["ai-models", "ai-products", "industry", "paper", "tip", "other"]:
        if cat_key not in grouped:
            continue
        cat_name = CATEGORY_MAP.get(cat_key, cat_key)
        lines.append(f"\n## {cat_name}\n")
        for item in grouped[cat_key]:
            title = item.get("title", "无标题")
            source = item.get("source", "")
            summary = item.get("summary", "")
            url = item.get("url", "")
            pub_time = format_time(item.get("publishedAt"))
            lines.append(f"{idx}. **{title}** — {source}")
            if pub_time:
                lines.append(f"   {pub_time}")
            if summary:
                lines.append(f"   {summary[:100]}")
            if url:
                lines.append(f"   {url}")
            lines.append("")
            idx += 1

    return "\n".join(lines)

def format_daily(data):
    if "error" in data:
        return f"获取日报失败: {data['error']}"

    date = data.get("date", "")
    lead = data.get("lead", {})
    sections = data.get("sections", [])
    flashes = data.get("flashes", [])

    lines = [f"# AI HOT 日报 · {date}\n"]
    if lead and lead.get("title"):
        lines.append(f"**{lead['title']}**\n")
        if lead.get("leadParagraph"):
            lines.append(f"{lead['leadParagraph']}\n")

    idx = 1
    for section in sections:
        label = section.get("label", "")
        items = section.get("items", [])
        lines.append(f"\n## {label}\n")
        for item in items:
            title = item.get("title", "无标题")
            source = item.get("sourceName", "")
            summary = item.get("summary", "")
            url = item.get("sourceUrl", "")
            lines.append(f"{idx}. **{title}** — {source}")
            if summary:
                lines.append(f"   {summary[:100]}")
            if url:
                lines.append(f"   {url}")
            lines.append("")
            idx += 1

    if flashes:
        lines.append("\n## 快讯\n")
        for flash in flashes:
            title = flash.get("title", "")
            source = flash.get("sourceName", "")
            url = flash.get("sourceUrl", "")
            lines.append(f"- {title} — {source}")
            if url:
                lines.append(f"  {url}")

    return "\n".join(lines)

def save_selected(items_text, filepath="today_selected.md"):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(items_text)
    print(f"已保存到 {filepath}")

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    mode = sys.argv[1] if len(sys.argv) > 1 else "selected"

    if mode == "daily":
        print("正在获取今日日报...")
        data = get_daily()
        print(format_daily(data))
    elif mode == "selected":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        print(f"正在获取最近 {hours} 小时的 AI 热点精选...")
        data = get_selected_items(hours=hours)
        output = format_items(data)
        print(output)
        save_selected(output)
    else:
        print("用法: python daily_aihot.py [daily|selected] [hours]")
