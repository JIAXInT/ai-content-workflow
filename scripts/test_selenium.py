"""
测试 Selenium 截取 X 平台推文
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import time

def test_selenium_screenshot():
    url = "https://x.com/AnthropicAI/status/1929213162397413582"
    output_path = Path("images/test-selenium/screenshot_selenium.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 配置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--window-size=1280,900")

    # 设置 User-Agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        # 初始化 WebDriver
        print("正在初始化 WebDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 移除 webdriver 特征
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # 访问页面
        print(f"正在访问: {url}")
        driver.get(url)

        # 等待页面加载
        print("等待页面加载...")
        time.sleep(10)

        # 尝试找到推文元素
        selectors = [
            'article[data-testid="tweet"]',
            '[data-testid="tweetText"]',
            'div[role="article"]',
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element:
                    print(f"找到元素: {selector}")
                    element.screenshot(str(output_path))
                    print(f"截图已保存: {output_path}")
                    return
            except Exception as e:
                print(f"选择器 {selector} 失败: {e}")
                continue

        # 如果没有找到特定元素，截取整个页面
        print("未找到特定元素，截取整个页面...")
        driver.save_screenshot(str(output_path))
        print(f"截图已保存: {output_path}")

    except Exception as e:
        print(f"截图失败: {e}")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    test_selenium_screenshot()
