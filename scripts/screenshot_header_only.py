"""
只截取博客文章的标题和引言部分
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urlparse
import re


def get_blog_type(url: str) -> str:
    """根据 URL 判断博客类型"""
    if "claude.com" in url:
        return "claude"
    elif "openai.com" in url:
        return "openai"
    elif "anthropic.com" in url:
        return "anthropic"
    else:
        return "generic"


def screenshot_blog_header(url: str, output_path: Path) -> Path:
    """截取博客文章的标题和引言部分"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
            locale="en-US",
        )
        page = context.new_page()

        try:
            print(f"正在访问: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            blog_type = get_blog_type(url)

            if blog_type == "claude":
                # Claude 博客的特殊处理
                # 尝试找到标题和引言的容器
                selectors = [
                    "main > div:first-child",  # 主内容区的第一个 div
                    "article:first-of-type",   # 文章的第一个 article
                    "div[class*='hero']",      # hero 区域
                    "div[class*='header']",    # header 区域
                    "h1",                      # 标题
                ]

                for selector in selectors:
                    try:
                        element = page.query_selector(selector)
                        if element:
                            # 获取元素的边界框
                            box = element.bounding_box()
                            if box and box['height'] > 100:  # 确保有足够的高度
                                print(f"找到元素: {selector}, 高度: {box['height']}px")

                                # 截取从页面顶部到元素底部的区域
                                page.screenshot(
                                    path=str(output_path),
                                    clip={
                                        "x": 0,
                                        "y": 0,
                                        "width": 1280,
                                        "height": min(box['y'] + box['height'] + 100, 900)
                                    }
                                )
                                print(f"截图已保存: {output_path}")
                                return output_path
                    except Exception as e:
                        continue

            # 通用处理：截取页面上半部分
            print("使用通用方法截取上半部分...")
            page.screenshot(
                path=str(output_path),
                clip={"x": 0, "y": 0, "width": 1280, "height": 600}
            )
            print(f"截图已保存: {output_path}")
            return output_path

        except Exception as e:
            print(f"截图失败: {e}")
            return None

        finally:
            page.close()
            context.close()
            browser.close()


if __name__ == "__main__":
    # 截取第一篇博客
    url1 = "https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code"
    output1 = Path("images/2026-06-03_claude-code-agentic/screenshot_claude_header.png")
    screenshot_blog_header(url1, output1)

    # 截取第二篇博客
    url2 = "https://claude.com/blog/running-an-ai-native-engineering-org"
    output2 = Path("images/2026-06-03_claude-code-agentic/screenshot_running_header.png")
    screenshot_blog_header(url2, output2)
