"""
网页截图脚本
使用 Playwright 截取网页内容，支持 Twitter/X、微博、知乎等平台的特殊处理。
用于在文章创作中获取原文素材，增强文章可信度。
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


# 平台特定配置
PLATFORM_CONFIGS = {
    "twitter": {
        "name": "Twitter/X",
        "domains": ["twitter.com", "x.com"],
        "selectors": [
            'article[data-testid="tweet"]',  # 推文卡片
            '[data-testid="tweetText"]',      # 推文文本
            'div[role="article"]',            # 文章角色
            '[data-testid="cellInnerDiv"]',   # 单元格内部
            'div[data-testid="tweet"]',       # 推文容器
            'div[class*="tweet"]',            # 推文类名
            'div[class*="Tweet"]',            # 推文类名（大写）
        ],
        "wait_time": 10000,  # 等待 10 秒加载动态内容
        "wait_for_selector": 'article[data-testid="tweet"]',  # 等待推文元素出现
        "wait_for_load_state": "networkidle",  # 等待网络空闲
        "viewport": {"width": 1280, "height": 900},
    },
    "weibo": {
        "name": "微博",
        "domains": ["weibo.com", "weibo.cn"],
        "selectors": [
            ".weibo-text",           # 微博文本
            ".card-wrap",            # 卡片容器
            ".WB_detail",            # 详情区域
        ],
        "wait_time": 3000,
        "wait_for_selector": ".weibo-text",
        "wait_for_load_state": "networkidle",
        "viewport": {"width": 1280, "height": 900},
    },
    "zhihu": {
        "name": "知乎",
        "domains": ["zhihu.com", "zhuanlan.zhihu.com"],
        "selectors": [
            ".RichContent",          # 富文本内容
            ".Post-RichText",        # 文章正文
            ".AnswerItem",           # 回答内容
        ],
        "wait_time": 3000,
        "wait_for_selector": ".RichContent",
        "wait_for_load_state": "networkidle",
        "viewport": {"width": 1280, "height": 900},
    },
    "github": {
        "name": "GitHub",
        "domains": ["github.com"],
        "selectors": [
            ".markdown-body",        # README 内容
            ".js-issue-title",       # Issue 标题
            ".comment-body",         # 评论内容
        ],
        "wait_time": 2000,
        "wait_for_selector": ".markdown-body",
        "wait_for_load_state": "domcontentloaded",
        "viewport": {"width": 1280, "height": 900},
    },
    "default": {
        "name": "通用网页",
        "domains": [],
        "selectors": [
            "article",               # 文章标签
            "main",                  # 主内容区
            ".content",              # 内容类名
            "#content",              # 内容 ID
        ],
        "wait_time": 2000,
        "wait_for_selector": None,
        "wait_for_load_state": "domcontentloaded",
        "viewport": {"width": 1280, "height": 900},
    },
}


def detect_platform(url: str) -> dict:
    """根据 URL 检测平台类型"""
    parsed = urlparse(url)
    domain = parsed.hostname or ""

    for platform_key, config in PLATFORM_CONFIGS.items():
        if platform_key == "default":
            continue
        for d in config["domains"]:
            if d in domain:
                return config

    return PLATFORM_CONFIGS["default"]


def extract_id_from_url(url: str) -> str:
    """从 URL 中提取唯一标识符"""
    parsed = urlparse(url)
    path = parsed.path

    # Twitter 推文 ID
    tweet_match = re.search(r"/status/(\d+)", path)
    if tweet_match:
        return tweet_match.group(1)

    # GitHub Issue/PR 编号
    github_match = re.search(r"/(issues|pull)/(\d+)", path)
    if github_match:
        return github_match.group(2)

    # 通用：使用路径的最后部分
    parts = [p for p in path.split("/") if p]
    if parts:
        return parts[-1][:20]  # 限制长度

    # 使用域名哈希
    return str(hash(parsed.hostname))[:8]


def generate_filename(url: str, output_dir: Path) -> Path:
    """生成截图文件名"""
    parsed = urlparse(url)
    domain = (parsed.hostname or "unknown").replace("www.", "")
    date_str = datetime.now().strftime("%Y%m%d")
    url_id = extract_id_from_url(url)

    # 清理域名，只保留字母数字
    domain_clean = re.sub(r"[^a-zA-Z0-9]", "", domain)[:20]

    filename = f"screenshot_{domain_clean}_{date_str}_{url_id}.png"
    return output_dir / filename


def screenshot_url(
    url: str,
    output_path: Path = None,
    screenshot_type: str = "element",
    output_dir: Path = None,
    custom_selector: str = None,
    clip_region: str = None,
) -> Path:
    """
    截取网页内容

    Args:
        url: 要截取的网页 URL
        output_path: 输出文件路径（优先级高于 output_dir）
        screenshot_type: 截图类型 - "element"（关键元素）, "viewport"（视口）, "full"（全文）, "custom"（自定义选择器）
        output_dir: 输出目录（默认 images/）
        custom_selector: 自定义 CSS 选择器（当 screenshot_type="custom" 时使用）
        clip_region: 截取区域 - "top"（上半部分）, "header"（头部区域）, "center"（中间部分）

    Returns:
        截图文件路径
    """
    # 确定输出路径
    if output_path:
        target_path = Path(output_path)
    else:
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "images"
        output_dir.mkdir(parents=True, exist_ok=True)
        target_path = generate_filename(url, output_dir)

    # 确保目录存在
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 检测平台
    platform = detect_platform(url)
    print(f"检测到平台: {platform['name']}")
    print(f"目标 URL: {url}")
    print(f"输出路径: {target_path}")

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)

        # 创建上下文
        context = browser.new_context(
            viewport=platform["viewport"],
            device_scale_factor=2,  # 2x 分辨率
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )

        # 设置 User-Agent
        page = context.new_page()
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        try:
            # 访问页面
            print("正在加载页面...")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # 智能等待页面加载
            print(f"等待页面加载完成...")

            # 1. 等待网络空闲（如果配置了）
            if platform.get("wait_for_load_state"):
                try:
                    page.wait_for_load_state(platform["wait_for_load_state"], timeout=15000)
                    print(f"网络状态: {platform['wait_for_load_state']}")
                except Exception as e:
                    print(f"等待网络状态超时: {e}")

            # 2. 等待特定元素出现（如果配置了）
            if platform.get("wait_for_selector"):
                try:
                    page.wait_for_selector(platform["wait_for_selector"], timeout=10000)
                    print(f"找到目标元素: {platform['wait_for_selector']}")
                except Exception as e:
                    print(f"等待元素超时: {e}")
                    # 继续尝试其他选择器

            # 3. 额外等待时间（作为兜底）
            print(f"额外等待 {platform['wait_time']}ms 确保内容加载...")
            page.wait_for_timeout(platform["wait_time"])

            # 4. 对于 Twitter/X，多次滚动页面以触发更多内容加载
            if "twitter" in platform.get("name", "").lower() or "x.com" in url:
                try:
                    # 多次滚动以触发懒加载
                    for i in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(1500)
                        # 滚动回顶部
                        page.evaluate("window.scrollTo(0, 0)")
                        page.wait_for_timeout(500)
                    print("已多次滚动页面触发内容加载")
                except Exception as e:
                    print(f"滚动页面失败: {e}")

            # 5. 检查页面是否有实际内容
            try:
                body_text = page.inner_text("body")
                if len(body_text.strip()) < 50:
                    print("警告: 页面内容较少，可能未完全加载")
                else:
                    print(f"页面内容长度: {len(body_text)} 字符")
            except Exception as e:
                print(f"检查页面内容失败: {e}")

            # 根据截图类型处理
            if screenshot_type == "full":
                # 全文截图
                print("截取全文...")
                page.screenshot(path=str(target_path), full_page=True)

            elif screenshot_type == "viewport":
                # 视口截图
                print("截取视口...")
                page.screenshot(path=str(target_path))

            elif screenshot_type == "custom" and custom_selector:
                # 自定义选择器截图
                print(f"使用自定义选择器: {custom_selector}")
                try:
                    element = page.query_selector(custom_selector)
                    if element:
                        print(f"找到元素: {custom_selector}")
                        element.screenshot(path=str(target_path))
                    else:
                        print(f"未找到元素: {custom_selector}，截取视口...")
                        page.screenshot(path=str(target_path))
                except Exception as e:
                    print(f"选择器失败: {e}，截取视口...")
                    page.screenshot(path=str(target_path))

            elif clip_region:
                # 区域截图
                print(f"截取区域: {clip_region}")
                try:
                    # 获取视口尺寸
                    viewport = page.viewport_size
                    width = viewport['width']
                    height = viewport['height']

                    if clip_region == "top":
                        # 截取上半部分（0 到 50%）
                        page.screenshot(
                            path=str(target_path),
                            clip={"x": 0, "y": 0, "width": width, "height": height // 2}
                        )
                    elif clip_region == "header":
                        # 截取头部区域（0 到 30%）
                        page.screenshot(
                            path=str(target_path),
                            clip={"x": 0, "y": 0, "width": width, "height": int(height * 0.3)}
                        )
                    elif clip_region == "center":
                        # 截取中间部分（25% 到 75%）
                        page.screenshot(
                            path=str(target_path),
                            clip={"x": 0, "y": height // 4, "width": width, "height": height // 2}
                        )
                    else:
                        print(f"未知区域: {clip_region}，截取视口...")
                        page.screenshot(path=str(target_path))
                except Exception as e:
                    print(f"区域截图失败: {e}，截取视口...")
                    page.screenshot(path=str(target_path))

            else:
                # 元素截图（默认）
                screenshot_taken = False
                for selector in platform["selectors"]:
                    try:
                        element = page.query_selector(selector)
                        if element:
                            print(f"找到元素: {selector}")
                            element.screenshot(path=str(target_path))
                            screenshot_taken = True
                            break
                    except Exception as e:
                        print(f"选择器 {selector} 失败: {e}")
                        continue

                # 如果没有找到特定元素，尝试截取所有推文
                if not screenshot_taken and "twitter" in platform.get("name", "").lower():
                    try:
                        tweets = page.query_selector_all('article[data-testid="tweet"]')
                        if tweets:
                            print(f"找到 {len(tweets)} 条推文，截取第一条...")
                            tweets[0].screenshot(path=str(target_path))
                            screenshot_taken = True
                    except Exception as e:
                        print(f"截取推文列表失败: {e}")

                # 如果还是没有找到特定元素，截取视口
                if not screenshot_taken:
                    print("未找到特定元素，截取视口...")
                    page.screenshot(path=str(target_path))

            print(f"截图已保存: {target_path}")
            return target_path

        except Exception as e:
            print(f"截图失败: {e}")
            # 尝试截取当前状态
            try:
                page.screenshot(path=str(target_path))
                print(f"已保存错误状态截图: {target_path}")
                return target_path
            except:
                raise e

        finally:
            page.close()
            context.close()
            browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="网页截图工具 - 截取网页内容作为文章素材",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 截取推文
  python screenshot_webpage.py "https://twitter.com/user/status/123456"

  # 截取多个网页
  python screenshot_webpage.py "url1" "url2" "url3"

  # 截取全文
  python screenshot_webpage.py "url" --type full

  # 截取特定元素（如标题和引言）
  python screenshot_webpage.py "url" --type custom --selector "article header"

  # 截取博客文章的标题部分
  python screenshot_webpage.py "url" -t custom -s "h1, .post-title, article > header"

  # 截取页面上半部分（包含标题和引言）
  python screenshot_webpage.py "url" --clip top

  # 截取页面头部区域（30%）
  python screenshot_webpage.py "url" --clip header

  # 指定输出目录
  python screenshot_webpage.py "url" -o images/my-article/
        """
    )

    parser.add_argument(
        "urls",
        nargs="+",
        help="要截取的网页 URL（支持多个）"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出目录（默认 images/）",
        default=None
    )

    parser.add_argument(
        "-t", "--type",
        choices=["element", "viewport", "full", "custom"],
        default="element",
        help="截图类型: element=关键元素, viewport=视口, full=全文, custom=自定义选择器（默认: element）"
    )

    parser.add_argument(
        "-s", "--selector",
        help="自定义 CSS 选择器（当 --type=custom 时使用）",
        default=None
    )

    parser.add_argument(
        "--clip",
        choices=["top", "header", "center"],
        help="截取区域: top=上半部分, header=头部区域, center=中间部分",
        default=None
    )

    parser.add_argument(
        "--output-file",
        help="单个 URL 时指定输出文件路径",
        default=None
    )

    args = parser.parse_args()

    # 设置输出目录
    output_dir = Path(args.output) if args.output else None

    # 处理每个 URL
    results = []
    for url in args.urls:
        print(f"\n{'='*50}")
        print(f"处理: {url}")
        print('='*50)

        try:
            # 单个 URL 且指定了输出文件
            if len(args.urls) == 1 and args.output_file:
                output_path = Path(args.output_file)
            else:
                output_path = None

            result = screenshot_url(
                url=url,
                output_path=output_path,
                screenshot_type=args.type,
                output_dir=output_dir,
                custom_selector=args.selector,
                clip_region=args.clip,
            )
            results.append({"url": url, "path": str(result), "success": True})

        except Exception as e:
            print(f"处理失败: {e}")
            results.append({"url": url, "error": str(e), "success": False})

    # 输出结果摘要
    print(f"\n{'='*50}")
    print("处理完成")
    print('='*50)
    print(f"成功: {sum(1 for r in results if r['success'])}/{len(results)}")
    for r in results:
        if r["success"]:
            print(f"  ✓ {r['url']}")
            print(f"    → {r['path']}")
        else:
            print(f"  ✗ {r['url']}")
            print(f"    错误: {r.get('error', '未知错误')}")

    return 0 if all(r["success"] for r in results) else 1


if __name__ == "__main__":
    # 设置标准输出编码
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    sys.exit(main())
