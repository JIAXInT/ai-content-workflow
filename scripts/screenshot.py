"""截图脚本：将 HTML 封面图转为 PNG"""
from playwright.sync_api import sync_playwright
from pathlib import Path

# 获取项目根目录（scripts 的父目录）
base_dir = Path(__file__).parent.parent / "covers"

covers = [
    {"html": "cover.html", "output": "cover-main.png", "width": 900, "height": 383},
    {"html": "cover-square.html", "output": "cover-square.png", "width": 383, "height": 383},
]

with sync_playwright() as p:
    # 使用 3x 分辨率来获得更清晰的文字
    browser = p.chromium.launch()
    for c in covers:
        # 设置 device_scale_factor=3 来提高分辨率
        context = browser.new_context(
            viewport={"width": c["width"], "height": c["height"]},
            device_scale_factor=3
        )
        page = context.new_page()
        page.goto(f"file:///{(base_dir / c['html']).resolve()}")
        page.wait_for_timeout(1000)  # 增加等待时间确保字体加载
        # 截取 .cover 元素
        el = page.query_selector(".cover")
        if el:
            el.screenshot(path=str(base_dir / c["output"]))
            print(f"已生成 {c['output']} ({c['width']}x{c['height']} @3x)")
        else:
            print(f"未找到 .cover 元素: {c['html']}")
        page.close()
        context.close()
    browser.close()
