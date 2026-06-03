"""
测试 playwright-stealth 截取 X 平台推文
"""
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from pathlib import Path

def test_stealth_screenshot():
    url = "https://x.com/AnthropicAI/status/1929213162397413582"
    output_path = Path("images/test-stealth/screenshot_stealth.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)

        # 创建上下文
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
            locale="en-US",
            timezone_id="America/New_York",
        )

        # 创建页面并应用 stealth
        page = context.new_page()
        stealth = Stealth()
        stealth.apply_stealth_sync(page)

        try:
            # 访问页面
            print(f"正在访问: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # 等待页面加载
            print("等待页面加载...")
            page.wait_for_timeout(10000)

            # 尝试找到推文元素
            selectors = [
                'article[data-testid="tweet"]',
                '[data-testid="tweetText"]',
                'div[role="article"]',
            ]

            for selector in selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        print(f"找到元素: {selector}")
                        element.screenshot(path=str(output_path))
                        print(f"截图已保存: {output_path}")
                        return
                except Exception as e:
                    print(f"选择器 {selector} 失败: {e}")
                    continue

            # 如果没有找到特定元素，截取视口
            print("未找到特定元素，截取视口...")
            page.screenshot(path=str(output_path))
            print(f"截图已保存: {output_path}")

        except Exception as e:
            print(f"截图失败: {e}")

        finally:
            page.close()
            context.close()
            browser.close()

if __name__ == "__main__":
    test_stealth_screenshot()
