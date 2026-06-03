"""
浏览器截图工具
打开浏览器让用户手动操作，然后截取用户看到的内容。
用于获取 X 平台等需要登录或有反爬虫机制的网站截图。
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def get_platform_from_url(url: str) -> str:
    """根据 URL 获取平台名称"""
    parsed = urlparse(url)
    domain = parsed.hostname or ""

    if "twitter.com" in domain or "x.com" in domain:
        return "twitter"
    elif "weibo.com" in domain or "weibo.cn" in domain:
        return "weibo"
    elif "zhihu.com" in domain:
        return "zhihu"
    elif "github.com" in domain:
        return "github"
    else:
        return "web"


def generate_filename(url: str, platform: str, output_dir: Path) -> Path:
    """生成截图文件名"""
    parsed = urlparse(url)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 从 URL 提取 ID
    path = parsed.path
    url_id = ""
    if platform == "twitter":
        import re
        tweet_match = re.search(r"/status/(\d+)", path)
        if tweet_match:
            url_id = tweet_match.group(1)
    elif platform == "github":
        parts = [p for p in path.split("/") if p]
        if parts:
            url_id = "_".join(parts[:2])

    if not url_id:
        url_id = "screenshot"

    filename = f"{platform}_{date_str}_{url_id}.png"
    return output_dir / filename


def browser_screenshot(url: str, output_dir: Path = None, wait_seconds: int = 0) -> Path:
    """
    打开浏览器让用户手动操作，然后截取屏幕

    Args:
        url: 要访问的网页 URL
        output_dir: 输出目录（默认 images/manual/）
        wait_seconds: 截图前等待的秒数（让用户有时间操作）

    Returns:
        截图文件路径
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "images" / "manual"
    output_dir.mkdir(parents=True, exist_ok=True)

    platform = get_platform_from_url(url)
    output_path = generate_filename(url, platform, output_dir)

    print(f"\n{'='*60}")
    print(f"📱 浏览器截图工具")
    print(f"{'='*60}")
    print(f"目标 URL: {url}")
    print(f"平台: {platform}")
    print(f"输出路径: {output_path}")
    print(f"{'='*60}")

    with sync_playwright() as p:
        # 启动浏览器（非无头模式）
        print("\n🌐 正在启动浏览器...")
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            slow_mo=100,  # 稍微放慢操作，便于观察
        )

        # 创建上下文
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )

        # 创建页面
        page = context.new_page()

        try:
            # 访问页面
            print(f"📄 正在访问: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            print("\n" + "="*60)
            print("✅ 浏览器已打开！")
            print("="*60)
            print("\n📋 操作说明：")
            print("  1. 在浏览器中手动操作（登录、滚动、点击等）")
            print("  2. 找到要截取的内容")
            print("  3. 按 Enter 键截取当前屏幕")
            print("  4. 或输入 'q' 退出不截图")
            print("  5. 或输入等待秒数（如 '5'）等待后自动截图")
            print("="*60)

            # 等待用户操作或自动截图
            if wait_seconds > 0:
                # 如果指定了等待时间，自动截图
                print(f"⏳ 等待 {wait_seconds} 秒后自动截图...")
                page.wait_for_timeout(wait_seconds * 1000)
            else:
                # 否则等待用户操作
                try:
                    while True:
                        user_input = input("\n⏸️  按 Enter 截图，输入 'q' 退出，或输入秒数等待: ").strip()

                        if user_input.lower() == 'q':
                            print("❌ 已取消截图")
                            return None

                        if user_input.isdigit():
                            wait_sec = int(user_input)
                            print(f"⏳ 等待 {wait_sec} 秒后截图...")
                            page.wait_for_timeout(wait_sec * 1000)
                            break
                        elif user_input == '':
                            break
                        else:
                            print("⚠️  请输入 Enter、'q' 或数字")
                except EOFError:
                    # 非交互式环境，直接截图
                    print("⏳ 非交互式环境，直接截图...")
                    page.wait_for_timeout(2000)

            # 截图
            print("\n📸 正在截图...")
            page.screenshot(path=str(output_path))

            print(f"\n✅ 截图已保存: {output_path}")
            print(f"📁 文件大小: {output_path.stat().st_size / 1024:.1f} KB")

            return output_path

        except Exception as e:
            print(f"\n❌ 截图失败: {e}")
            return None

        finally:
            print("\n🔒 正在关闭浏览器...")
            page.close()
            context.close()
            browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="浏览器截图工具 - 打开浏览器手动操作后截取屏幕",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 截取 X 平台推文
  python browser_screenshot.py "https://x.com/user/status/123456"

  # 截取需要登录的页面
  python browser_screenshot.py "https://twitter.com/home"

  # 指定输出目录
  python browser_screenshot.py "url" -o images/my-article/

  # 等待 5 秒后自动截图
  python browser_screenshot.py "url" --wait 5
        """
    )

    parser.add_argument(
        "url",
        help="要截取的网页 URL"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出目录（默认 images/manual/）",
        default=None
    )

    parser.add_argument(
        "-w", "--wait",
        help="截图前等待的秒数（默认手动确认）",
        type=int,
        default=0
    )

    args = parser.parse_args()

    # 设置输出目录
    output_dir = Path(args.output) if args.output else None

    # 执行截图
    result = browser_screenshot(
        url=args.url,
        output_dir=output_dir,
        wait_seconds=args.wait,
    )

    if result:
        print(f"\n{'='*60}")
        print(f"✅ 截图完成！")
        print(f"{'='*60}")
        print(f"文件路径: {result}")
        print(f"\n在文章中引用：")
        print(f"![截图]({result})")
        print(f"{'='*60}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    # 设置标准输出编码
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    sys.exit(main())
