#!/usr/bin/env python3
"""
渲染社交卡片脚本
使用 Playwright 将 HTML 模板渲染为 PNG 图片
支持公众号封面（21:9 + 1:1）和小红书轮播图（3:4）
"""

import sys
import io
from pathlib import Path
from playwright.sync_api import sync_playwright

# 设置标准输出编码为 UTF-8（解决 Windows 终端 emoji 显示问题）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def render_social_cards(html_file: str, output_dir: str = None, auto_detect: bool = True):
    """
    渲染社交卡片 HTML 为 PNG 图片

    Args:
        html_file: HTML 文件路径
        output_dir: 输出目录，默认为 HTML 文件所在目录
        auto_detect: 是否自动检测卡片元素
    """
    html_path = Path(html_file).resolve()
    if not html_path.exists():
        print(f"❌ HTML 文件不存在: {html_path}")
        return

    # 输出目录：默认为 HTML 文件所在目录
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = html_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # 定义卡片类型和尺寸
    card_types = {
        "wechat-21x9": {"width": 2100, "height": 900, "suffix": "cover-21x9", "desc": "公众号 21:9 主封面"},
        "wechat-1x1": {"width": 1080, "height": 1080, "suffix": "cover-1x1", "desc": "公众号 1:1 方封面"},
        "xhs": {"width": 1080, "height": 1440, "suffix": "xhs", "desc": "小红书轮播图"},
    }

    print(f"📄 正在渲染: {html_path.name}")
    print(f"📁 输出目录: {out_dir}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch()

        if auto_detect:
            # 自动检测页面中的卡片元素
            context = browser.new_context(
                viewport={"width": 2100, "height": 1440},
                device_scale_factor=2
            )
            page = context.new_page()
            page.goto(f"file:///{html_path.as_posix()}")

            # 等待 JavaScript 执行完成（卡片元素被动态生成）
            page.wait_for_timeout(3000)  # 增加等待时间

            # 等待卡片容器加载
            try:
                page.wait_for_selector('#cards-container', timeout=5000)
                # 等待卡片元素出现
                page.wait_for_selector('.poster', timeout=5000)
            except Exception as e:
                print(f"⚠️ 等待卡片加载超时: {e}")

            # 查找所有 poster 元素
            posters = page.query_selector_all('.poster')
            cards = []
            for poster in posters:
                poster_id = poster.get_attribute('id')
                if poster_id:
                    # 根据 ID 确定卡片类型
                    if poster_id.startswith('wechat-21x9'):
                        card_type = card_types["wechat-21x9"]
                    elif poster_id.startswith('wechat-1x1'):
                        card_type = card_types["wechat-1x1"]
                    elif poster_id.startswith('xhs-'):
                        card_type = card_types["xhs"]
                    else:
                        # 默认使用小红书尺寸
                        card_type = card_types["xhs"]

                    cards.append({
                        "id": poster_id,
                        "output": f"{card_type['suffix']}-{poster_id}.png",
                        "width": card_type["width"],
                        "height": card_type["height"],
                        "desc": f"{card_type['desc']} ({poster_id})"
                    })

            page.close()
            context.close()

            if not cards:
                print("⚠️ 未检测到卡片元素，使用默认配置")
                cards = [
                    {"id": "wechat-21x9", "output": "cover-21x9.png", "width": 2100, "height": 900, "desc": "公众号 21:9 主封面"},
                    {"id": "wechat-1x1", "output": "cover-1x1.png", "width": 1080, "height": 1080, "desc": "公众号 1:1 方封面"},
                    {"id": "xhs-01", "output": "xhs-01.png", "width": 1080, "height": 1440, "desc": "小红书 1/5 封面"},
                    {"id": "xhs-02", "output": "xhs-02.png", "width": 1080, "height": 1440, "desc": "小红书 2/5 数据"},
                    {"id": "xhs-03", "output": "xhs-03.png", "width": 1080, "height": 1440, "desc": "小红书 3/5 对比"},
                    {"id": "xhs-04", "output": "xhs-04.png", "width": 1080, "height": 1440, "desc": "小红书 4/5 要点"},
                    {"id": "xhs-05", "output": "xhs-05.png", "width": 1080, "height": 1440, "desc": "小红书 5/5 总结"},
                ]
        else:
            # 使用默认配置
            cards = [
                {"id": "wechat-21x9", "output": "cover-21x9.png", "width": 2100, "height": 900, "desc": "公众号 21:9 主封面"},
                {"id": "wechat-1x1", "output": "cover-1x1.png", "width": 1080, "height": 1080, "desc": "公众号 1:1 方封面"},
                {"id": "xhs-01", "output": "xhs-01.png", "width": 1080, "height": 1440, "desc": "小红书 1/5 封面"},
                {"id": "xhs-02", "output": "xhs-02.png", "width": 1080, "height": 1440, "desc": "小红书 2/5 数据"},
                {"id": "xhs-03", "output": "xhs-03.png", "width": 1080, "height": 1440, "desc": "小红书 3/5 对比"},
                {"id": "xhs-04", "output": "xhs-04.png", "width": 1080, "height": 1440, "desc": "小红书 4/5 要点"},
                {"id": "xhs-05", "output": "xhs-05.png", "width": 1080, "height": 1440, "desc": "小红书 5/5 总结"},
            ]

        print(f"📊 检测到 {len(cards)} 个卡片")
        print()

        for card in cards:
            print(f"🎨 渲染中: {card['desc']}...")

            # 创建上下文，使用 2x 分辨率
            context = browser.new_context(
                viewport={"width": card["width"], "height": card["height"]},
                device_scale_factor=2
            )
            page = context.new_page()

            # 加载 HTML
            page.goto(f"file:///{html_path.as_posix()}", timeout=60000)
            page.wait_for_timeout(2000)  # 等待字体加载

            # 查找目标元素
            element = page.query_selector(f"#{card['id']}")
            if element:
                # 滚动到元素可见
                element.scroll_into_view_if_needed()
                page.wait_for_timeout(500)

                # 截图
                output_path = out_dir / card["output"]
                element.screenshot(path=str(output_path))
                print(f"  ✅ 已生成: {card['output']}")
            else:
                print(f"  ⚠️ 未找到元素: #{card['id']}")

            page.close()
            context.close()

        browser.close()

    print()
    print("✨ 渲染完成！")
    print(f"📁 所有文件已保存到: {out_dir}")

    # 列出生成的文件
    print()
    print("📋 生成的文件:")
    for f in sorted(out_dir.glob("*.png")):
        if f.stat().st_size > 0:
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")


def main():
    if len(sys.argv) < 2:
        print("用法: python render_social_cards.py <html_file> [output_dir]")
        print()
        print("示例:")
        print("  python render_social_cards.py covers/mimo-social-cards.html")
        print("  python render_social_cards.py covers/mimo-social-cards.html output/")
        sys.exit(1)

    html_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    render_social_cards(html_file, output_dir)


if __name__ == "__main__":
    main()
