#!/usr/bin/env python3
"""
飞书文档保存脚本（完美版）
确保：标题正确、封面图在最上方、插图穿插在文章中间
"""

import subprocess
import sys
import json
import re
import yaml
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# AI创享派文件夹 token
FEISHU_FOLDER_TOKEN = "LSE7fyzmJlikJedhruQcqRuPngg"


def run_command(cmd, check=True):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=check
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode


def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    if not content.startswith('---'):
        return {}, content

    end_index = content.find('---', 3)
    if end_index == -1:
        return {}, content

    yaml_str = content[3:end_index]
    try:
        metadata = yaml.safe_load(yaml_str)
        body = content[end_index + 3:].lstrip('\n')
        return metadata or {}, body
    except yaml.YAMLError:
        return {}, content


def generate_cover(title, tag, date, subtitle):
    """生成封面图"""
    cmd = f'python scripts/generate_cover.py "{title}" "{tag}" "{date}" "{subtitle}" covers/cover.html'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"生成封面 HTML 失败: {stderr}")
        return None

    cmd = 'python scripts/screenshot.py'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"截图失败: {stderr}")
        return None

    return Path("covers/cover-main.png")


def create_doc_with_title(title):
    """创建带标题的空文档"""
    escaped_title = title.replace('"', '\\"')

    # 创建一个包含标题的临时文件
    temp_file = Path("temp_create.md")
    temp_file.write_text(f"# {title}\n\n", encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +create --api-version v2 --title "{escaped_title}" --content @temp_create.md --as bot --parent-token {FEISHU_FOLDER_TOKEN}'
    stdout, stderr, returncode = run_command(cmd, check=False)

    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"创建文档失败: {stderr}")
        return None

    try:
        json_match = re.search(r'\{.*\}', stdout, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            if result.get("ok"):
                doc_url = result["data"]["document"]["url"]
                doc_id = result["data"]["document"]["document_id"]
                return {"url": doc_url, "id": doc_id}
    except json.JSONDecodeError:
        pass

    print(f"解析文档结果失败: {stdout}")
    return None


def overwrite_doc_content(doc_url, content):
    """覆盖文档内容"""
    temp_file = Path("temp_content.md")
    temp_file.write_text(content, encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command overwrite --content @temp_content.md --as bot'
    stdout, stderr, returncode = run_command(cmd, check=False)

    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"覆盖内容失败: {stderr}")
        return False

    return True


def append_doc_content(doc_url, content):
    """追加文档内容"""
    temp_file = Path("temp_content.md")
    temp_file.write_text(content, encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command append --content @temp_content.md --as bot'
    stdout, stderr, returncode = run_command(cmd, check=False)

    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"追加内容失败: {stderr}")
        return False

    return True


def insert_image(doc_url, image_path):
    """插入图片到文档"""
    abs_path = Path(image_path).resolve()

    if not abs_path.exists():
        print(f"图片不存在: {abs_path}")
        return False

    cwd = Path.cwd()
    try:
        rel_path = abs_path.relative_to(cwd)
    except ValueError:
        rel_path = abs_path

    cmd = f'npx @larksuite/cli docs +media-insert --doc "{doc_url}" --file "{rel_path}" --as bot'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"插入图片失败: {stderr}")
        return False

    return True


def split_content_by_sections(body_content, num_splits):
    """
    将文章内容按小标题分成多个部分

    Args:
        body_content: 文章正文
        num_splits: 分成几部分

    Returns:
        列表，每个元素是一部分内容
    """
    paragraphs = body_content.split('\n\n')

    # 找到所有小标题的位置
    section_positions = []
    for i, para in enumerate(paragraphs):
        if para.strip().startswith('## '):
            section_positions.append(i)

    # 确定分割点
    split_points = []
    if len(section_positions) >= num_splits * 2:
        # 如果有足够的小标题，按小标题分割
        for i in range(num_splits):
            # 选择合适的小标题位置
            idx = section_positions[i * 2 + 1] if i * 2 + 1 < len(section_positions) else section_positions[-1]
            split_points.append(idx)
    else:
        # 如果没有足够的小标题，按段落数量分割
        total = len(paragraphs)
        for i in range(num_splits):
            split_points.append(total * (i + 1) // (num_splits + 1))

    # 分割内容
    parts = []
    start = 0
    for point in split_points:
        part = '\n\n'.join(paragraphs[start:point])
        if part.strip():
            parts.append(part)
        start = point

    # 添加最后一部分
    remaining = '\n\n'.join(paragraphs[start:])
    if remaining.strip():
        parts.append(remaining)

    return parts


def extract_urls_from_article(article_file):
    """从文章中提取原文链接"""
    import re
    from urllib.parse import urlparse

    article_path = Path(article_file)
    if not article_path.exists():
        return []

    content = article_path.read_text(encoding="utf-8")

    # 匹配各种 URL 模式
    url_patterns = [
        r'https?://(?:twitter\.com|x\.com)/\w+/status/\d+',
        r'https?://(?:www\.)?github\.com/[\w\-]+/[\w\-]+(?:/issues/\d+)?',
        r'https?://(?:www\.)?zhihu\.com/question/\d+',
        r'https?://(?:www\.)?weibo\.com/\d+/[\w]+',
        r'https?://[^\s\)\]\"\'<>]+',
    ]

    urls = []
    for pattern in url_patterns:
        matches = re.findall(pattern, content)
        urls.extend(matches)

    # 去重并过滤
    unique_urls = []
    seen = set()
    for url in urls:
        # 移除末尾的标点符号
        url = url.rstrip('.,;:!?')
        if url not in seen and 'feishu.cn' not in url:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls


def generate_illustrations(article_file, count=3):
    """使用原文截图作为文章插图"""
    print(f"正在获取原文截图作为插图...")

    # 从文章中提取原文链接
    urls = extract_urls_from_article(article_file)

    if not urls:
        print("未找到原文链接，跳过插图生成")
        return []

    # 限制截图数量
    urls = urls[:count]
    print(f"找到 {len(urls)} 个原文链接，准备截图...")

    # 创建输出目录
    article_path = Path(article_file)
    article_name = article_path.stem
    date_str = article_name[:10] if len(article_name) >= 10 else datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"images/{date_str}_{article_name[11:] if len(article_name) > 11 else article_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 使用截图脚本截取原文
    images = []
    for i, url in enumerate(urls, 1):
        print(f"  截图 {i}/{len(urls)}: {url}")
        try:
            # 调用截图脚本，使用 --type viewport 截取视口（包含标题和正文开头）
            cmd = f'python scripts/screenshot_webpage.py "{url}" -o "{output_dir}" --type viewport'
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            if result.returncode == 0:
                # 查找生成的截图文件
                screenshot_files = list(output_dir.glob(f"screenshot_*.png"))
                if screenshot_files:
                    # 获取最新的截图文件
                    latest_screenshot = max(screenshot_files, key=lambda f: f.stat().st_mtime)
                    images.append({
                        "path": latest_screenshot,
                        "info": {
                            "alt": f"原文截图 {i}",
                            "index": i,
                            "url": url
                        }
                    })
                    print(f"    截图成功: {latest_screenshot.name}")
                else:
                    print(f"    截图文件未找到")
            else:
                print(f"    截图失败: {result.stderr[:100]}")
        except Exception as e:
            print(f"    截图异常: {e}")

    if images:
        print(f"成功获取 {len(images)} 张原文截图作为插图")
    else:
        print("未能获取任何原文截图")

    return images


def save_article_to_feishu_perfect(article_file, generate_cover_flag=True, image_mode="screenshot", count=3):
    """
    完美保存文章到飞书文档

    流程：
    1. 创建带标题的空文档
    2. 覆盖内容为空（清空默认内容）
    3. 插入封面图
    4. 追加文章第一部分
    5. 插入原文截图1
    6. 追加文章第二部分
    7. 插入原文截图2
    8. 追加文章第三部分
    9. 插入原文截图3
    10. 追加文章剩余部分
    """
    # 读取文章内容
    article_path = Path(article_file)
    if not article_path.exists():
        print(f"文章文件不存在: {article_file}")
        return None

    full_content = article_path.read_text(encoding="utf-8")

    # 解析 frontmatter
    metadata, body_content = parse_frontmatter(full_content)

    # 从 frontmatter 获取信息
    title = metadata.get("title", article_path.stem)
    tag = metadata.get("category", "AI资讯")
    date = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))
    tags = metadata.get("tags", [])

    print(f"正在保存到飞书: {title}")

    # 第一步：生成封面图
    cover_path = None
    if generate_cover_flag:
        subtitle = "、".join(tags[:3]) if tags else "AI资讯"
        print("正在生成封面图...")
        cover_path = generate_cover(title, tag, date, subtitle)
        if cover_path:
            print(f"封面图生成成功: {cover_path}")

    # 第二步：获取原文截图作为插图
    article_images = []
    if image_mode == "screenshot":
        print("正在获取原文截图作为插图...")
        article_images = generate_illustrations(article_file, count=count)

    if article_images:
        print(f"成功生成 {len(article_images)} 张插图")

    # 第三步：创建带标题的空文档
    print("正在创建文档...")
    doc_result = create_doc_with_title(title)
    if not doc_result:
        return None

    doc_url = doc_result["url"]
    print(f"文档创建成功: {doc_url}")

    # 第四步：插入封面图
    if cover_path:
        print("正在插入封面图...")
        if insert_image(doc_url, cover_path):
            print("封面图插入成功")
        else:
            print("封面图插入失败")

    # 第六步：处理文章内容
    # 去掉封面图行和 H1 标题行
    body_content_clean = re.sub(r'^!\[.*?\]\(.*?\)\s*\n*', '', body_content, count=1)
    body_content_clean = re.sub(r'^#\s+.*\n*', '', body_content_clean, count=1)

    # 第七步：将文章内容分成多个部分
    num_images = len(article_images)
    if num_images > 0:
        content_parts = split_content_by_sections(body_content_clean, num_images)
    else:
        content_parts = [body_content_clean]

    # 第八步：交替追加内容和插图
    for i, part in enumerate(content_parts):
        # 追加内容
        print(f"正在追加第 {i + 1} 部分内容...")
        if not append_doc_content(doc_url, part):
            print(f"追加第 {i + 1} 部分内容失败")
            continue

        # 插入插图（如果有）
        if i < num_images:
            img = article_images[i]
            img_path = img["path"]
            print(f"正在插入第 {i + 1} 张插图: {img_path.name}")
            if insert_image(doc_url, img_path):
                print(f"第 {i + 1} 张插图插入成功")
            else:
                print(f"第 {i + 1} 张插图插入失败")

    # 第九步：更新文章的 frontmatter
    metadata["feishu_url"] = doc_url
    yaml_str = yaml.dump(metadata, allow_unicode=True, default_flow_style=False)
    new_content = f"---\n{yaml_str}---\n\n{body_content}"
    article_path.write_text(new_content, encoding="utf-8")

    return doc_result


def main():
    if len(sys.argv) < 2:
        print("用法: python save_to_feishu_perfect.py <文章文件路径> [选项]")
        print("示例: python save_to_feishu_perfect.py articles/2026-06-02_minimax-m3.md")
        print("\n选项:")
        print("  --no-cover           不生成封面图")
        print("  --no-images          不添加文章配图")
        print("  --count N            原文截图数量（默认: 3）")
        sys.exit(1)

    article_file = sys.argv[1]
    generate_cover_flag = "--no-cover" not in sys.argv

    if "--no-images" in sys.argv:
        image_mode = "none"
    else:
        image_mode = "screenshot"

    count = 3
    for i, arg in enumerate(sys.argv):
        if arg == "--count" and i + 1 < len(sys.argv):
            count = int(sys.argv[i + 1])

    result = save_article_to_feishu_perfect(article_file, generate_cover_flag, image_mode, count)

    if result:
        print(f"\n保存成功!")
        print(f"文档链接: {result['url']}")
    else:
        print("\n保存失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
