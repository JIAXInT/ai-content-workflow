"""截图脚本：将 HTML 封面图转为 PNG"""
from playwright.sync_api import sync_playwright
from pathlib import Path

base_dir = Path(__file__).parent

covers = [
    {"html": "cover.html", "output": "cover-main.png", "width": 900, "height": 383},
    {"html": "cover-square.html", "output": "cover-square.png", "width": 383, "height": 383},
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for c in covers:
        page = browser.new_page(viewport={"width": c["width"], "height": c["height"]})
        page.goto(f"file:///{(base_dir / c['html']).resolve()}")
        page.wait_for_timeout(500)
        # 截取 .cover 元素
        el = page.query_selector(".cover")
        if el:
            el.screenshot(path=str(base_dir / c["output"]))
            print(f"已生成 {c['output']} ({c['width']}x{c['height']})")
        else:
            print(f"未找到 .cover 元素: {c['html']}")
        page.close()
    browser.close()
