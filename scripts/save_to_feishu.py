#!/usr/bin/env python3
"""
飞书文档保存脚本
用于将文章和封面图保存到飞书文档
支持自动读取 frontmatter、生成封面、保存到文件夹、更新已有文档
"""

import subprocess
import sys
import json
import re
import yaml
import requests
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
            errors='replace',  # 替换无法解码的字符
            check=check
        )
        # 检查命令是否成功执行（返回码为 0 或者输出中包含 "ok": true）
        success = result.returncode == 0 or '"ok": true' in result.stdout
        return result.stdout, result.stderr, 0 if success else result.returncode
    except subprocess.CalledProcessError as e:
        success = e.returncode == 0 or '"ok": true' in (e.stdout or '')
        return e.stdout, e.stderr, 0 if success else e.returncode


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
    # 使用 generate_cover.py 脚本
    cmd = f'python scripts/generate_cover.py "{title}" "{tag}" "{date}" "{subtitle}" covers/cover.html'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"生成封面 HTML 失败: {stderr[:100] if stderr else 'unknown error'}")
        return None

    print("封面 HTML 生成成功")

    # 使用 screenshot.py 截图
    cmd = 'python scripts/screenshot.py'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"截图失败: {stderr[:100] if stderr else 'unknown error'}")
        return None

    print("截图完成")

    # 检查封面图是否存在
    cover_path = Path("covers/cover-main.png")
    if cover_path.exists():
        print(f"封面图生成成功: {cover_path}")
        return cover_path
    else:
        print(f"封面图文件不存在: {cover_path}")
        return None


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

    # 使用截图脚本截取原文（截取视口区域）
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


def split_content_for_images(body_content, image_count):
    """
    将文章内容分成多个部分，用于在适当位置插入图片
    返回一个列表，每个元素是 (content_part, insert_image_after)
    """
    # 按段落分割内容
    paragraphs = body_content.split('\n\n')

    if not paragraphs:
        return [(body_content, False)]

    # 计算每个图片应该插入的位置
    # 图片均匀分布在文章中，但不在第一段和最后一段
    total_paragraphs = len(paragraphs)

    if total_paragraphs <= 3 or image_count == 0:
        return [(body_content, False)]

    # 计算插入位置（跳过第一段和最后一段）
    insert_positions = []
    if image_count >= 1:
        # 第一张图片放在文章 1/3 处
        pos = total_paragraphs // 3
        insert_positions.append(pos)
    if image_count >= 2:
        # 第二张图片放在文章 2/3 处
        pos = (total_paragraphs * 2) // 3
        insert_positions.append(pos)
    if image_count >= 3:
        # 第三张图片放在文章中间偏后
        pos = (total_paragraphs * 3) // 4
        insert_positions.append(pos)

    # 构建结果
    result = []
    for i, para in enumerate(paragraphs):
        result.append((para, i in insert_positions))

    return result


def insert_images_to_content(body_content, images):
    """在文章内容中插入图片标记"""
    if not images:
        return body_content

    # 按段落分割内容
    paragraphs = body_content.split('\n\n')

    # 确定插图插入位置
    # 策略：根据小标题位置智能插入
    total_paragraphs = len(paragraphs)

    # 找到所有小标题的位置
    section_positions = []
    for i, para in enumerate(paragraphs):
        if para.strip().startswith('## '):
            section_positions.append(i)

    insert_positions = []

    if len(images) >= 1 and len(section_positions) >= 2:
        # 第一张：第二个小标题后（技术细节开始处）
        insert_positions.append(section_positions[1] + 1)
    elif len(images) >= 1:
        # 如果没有足够的小标题，在 1/3 处插入
        insert_positions.append(total_paragraphs // 3)

    if len(images) >= 2 and len(section_positions) >= 4:
        # 第二张：第四个小标题后（定价部分）
        insert_positions.append(section_positions[3] + 1)
    elif len(images) >= 2:
        # 如果没有足够的小标题，在 2/3 处插入
        insert_positions.append((total_paragraphs * 2) // 3)

    if len(images) >= 3 and len(section_positions) >= 6:
        # 第三张：第六个小标题后（应用场景）
        insert_positions.append(section_positions[5] + 1)
    elif len(images) >= 3:
        # 如果没有足够的小标题，在 3/4 处插入
        insert_positions.append((total_paragraphs * 3) // 4)

    # 构建新内容
    new_content = []
    image_index = 0

    for i, para in enumerate(paragraphs):
        new_content.append(para)

        # 检查是否需要插入图片
        if i in insert_positions and image_index < len(images):
            img = images[image_index]
            img_path = img["path"]

            # 使用相对路径
            try:
                rel_path = img_path.relative_to(Path.cwd())
            except ValueError:
                rel_path = img_path

            # 插入图片（使用 markdown 语法）
            new_content.append(f"\n![插图 {image_index + 1}]({rel_path})\n")

            image_index += 1

    return '\n\n'.join(new_content)


def create_feishu_doc(title, content, folder_token=None):
    """创建飞书文档"""
    # 将内容写入临时文件
    temp_file = Path("temp_article_content.md")
    temp_file.write_text(content, encoding="utf-8")

    # 转义标题中的特殊字符
    escaped_title = title.replace('"', '\\"')

    # 构建命令 - 使用 --title 和 --content 参数
    cmd = f'npx @larksuite/cli docs +create --api-version v2 --title "{escaped_title}" --content @temp_article_content.md --as bot'

    # 如果指定了文件夹，添加 parent-token 参数
    if folder_token:
        cmd += f' --parent-token {folder_token}'

    stdout, stderr, returncode = run_command(cmd, check=False)

    # 清理临时文件
    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"创建文档失败: {stderr}")
        return None

    # 解析 JSON 输出
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


def update_feishu_doc(doc_url, content, cover_image_path=None, title=None):
    """更新飞书文档内容"""
    # 清空文档内容
    temp_file = Path("temp_article_content.md")
    temp_file.write_text(" ", encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command overwrite --content @temp_article_content.md --as bot'
    stdout, stderr, returncode = run_command(cmd, check=False)
    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"清空文档失败: {stderr}")
        return False

    # 如果有标题，更新文档标题
    if title:
        escaped_title = title.replace('"', '\\"')
        cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --new-title "{escaped_title}" --as bot'
        stdout, stderr, returncode = run_command(cmd, check=False)
        if returncode != 0:
            print(f"更新标题失败: {stderr}")

    # 如果有封面图，插入到文档开头
    if cover_image_path:
        insert_media_to_doc(doc_url, cover_image_path, insert_at_top=False)

    # 追加文章内容
    temp_file = Path("temp_article_content.md")
    temp_file.write_text(content, encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command append --content @temp_article_content.md --as bot'
    stdout, stderr, returncode = run_command(cmd, check=False)
    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"追加内容失败: {stderr}")
        return False

    return True


def insert_media_to_doc(doc_url, file_path, insert_at_top=False):
    """插入媒体文件到文档"""
    abs_path = Path(file_path).resolve()

    if not abs_path.exists():
        print(f"文件不存在: {abs_path}")
        return False

    # 使用相对路径
    cwd = Path.cwd()
    try:
        rel_path = abs_path.relative_to(cwd)
    except ValueError:
        rel_path = abs_path

    # 构建命令
    cmd = f'npx @larksuite/cli docs +media-insert --doc "{doc_url}" --file "{rel_path}" --as bot'

    # 如果需要插入到文档最上方
    if insert_at_top:
        # 获取文档内容以找到第一个块
        doc_content = get_doc_content(doc_url)
        if doc_content:
            # 找到第一个非空行作为锚点
            first_line = find_first_content_line(doc_content)
            if first_line:
                # 使用 --before 在第一个内容块之前插入
                cmd += f' --before --selection-with-ellipsis "{first_line}"'

    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        # 安全地打印错误信息，处理编码问题
        try:
            print(f"插入媒体失败: {stderr}")
        except UnicodeEncodeError:
            print(f"插入媒体失败: (编码错误，无法显示详细信息)")
        return False

    try:
        json_match = re.search(r'\{.*\}', stdout, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result.get("ok", False)
    except json.JSONDecodeError:
        pass

    try:
        print(f"解析媒体插入结果失败: {stdout}")
    except UnicodeEncodeError:
        print("解析媒体插入结果失败: (编码错误，无法显示详细信息)")
    return False


def get_doc_content(doc_url):
    """获取文档内容"""
    cmd = f'npx @larksuite/cli docs +fetch --api-version v2 --doc "{doc_url}" --as bot'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        return None

    # 从 JSON 中提取 content 字段
    try:
        import json
        # 找到 JSON 部分
        json_match = re.search(r'\{.*\}', stdout, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return data.get("document", {}).get("content", "")
    except json.JSONDecodeError:
        pass

    return stdout


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


def find_first_content_line(content):
    """找到文档内容的第一个非空行（跳过标题）"""
    # 尝试解析 XML 格式的内容
    import re

    # 查找第一个 <p> 标签的内容
    match = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
    if match:
        first_para = match.group(1)
        # 移除 HTML 标签
        first_para = re.sub(r'<[^>]+>', '', first_para)
        # 截取前 20 个字符作为锚点
        if len(first_para) > 20:
            return first_para[:17] + "..."
        return first_para

    # 如果不是 XML 格式，按行处理
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        # 跳过空行和 YAML frontmatter
        if stripped and not stripped.startswith('---') and not stripped.startswith('#'):
            # 截取前 20 个字符作为锚点（避免过长）
            if len(stripped) > 20:
                return stripped[:17] + "..."
            return stripped
    return None


def save_article_to_feishu(article_file, generate_cover_flag=True, image_mode="screenshot", count=3):
    """
    保存文章到飞书文档

    Args:
        article_file: 文章文件路径
        generate_cover_flag: 是否生成封面图
        image_mode: 图片模式 - "screenshot" 使用原文截图, "none" 不添加图片
        count: 插图数量
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
    feishu_url = metadata.get("feishu_url")

    print(f"正在保存到飞书: {title}")

    # 生成封面图
    cover_path = None
    if generate_cover_flag:
        # 生成副标题（从 tags 中提取）
        subtitle = "、".join(tags[:3]) if tags else "AI资讯"

        print("正在生成封面图...")
        cover_path = generate_cover(title, tag, date, subtitle)
        if cover_path:
            print(f"封面图生成成功: {cover_path}")

    # 获取文章配图（使用原文截图）
    article_images = []
    if image_mode == "screenshot":
        print("正在获取原文截图作为插图...")
        article_images = generate_illustrations(article_file, count=count)

    if article_images:
        print(f"成功获取 {len(article_images)} 张配图")

    # 在文章内容中插入图片标记
    if article_images:
        body_content = insert_images_to_content(body_content, article_images)

    # 如果已有飞书文档链接，更新现有文档
    if feishu_url:
        print(f"文档已存在，将更新现有文档: {feishu_url}")
        doc_result = {"url": feishu_url, "id": feishu_url.split("/")[-1]}

        # 更新文档标题（使用 <title> HTML 标签，因为 --new-title 参数不起作用）
        if title:
            escaped_title = title.replace('"', '\\"')
            # 使用 <title> HTML 标签来设置标题
            title_content = f'<title>{escaped_title}</title><p> </p>'
            temp_title_file = Path("temp_title.md")
            temp_title_file.write_text(title_content, encoding="utf-8")
            cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{feishu_url}" --command overwrite --content @temp_title.md --as bot'
            stdout, stderr, returncode = run_command(cmd, check=False)
            temp_title_file.unlink(missing_ok=True)
            if returncode != 0:
                print(f"更新标题失败: {stderr[:200] if stderr else 'unknown error'}")
            else:
                print("标题更新成功")
    else:
        # 创建新文档 - 只使用 --title 参数设置标题，content 不包含 <title> 标签
        # 使用空的段落内容，后续会追加实际文章内容
        empty_content = "<p> </p>"
        doc_result = create_feishu_doc(title, empty_content, FEISHU_FOLDER_TOKEN)
        if not doc_result:
            return None

        print(f"文档创建成功: {doc_result['url']}")

    # 插入封面图到文档开头
    if cover_path:
        print("正在插入封面图...")
        if insert_media_to_doc(doc_result["url"], cover_path, insert_at_top=True):
            print("封面图插入成功")

    # 处理文章内容：去掉开头的封面图和 H1 标题（因为标题已经设置为文档标题）
    import re
    # 去掉封面图行（以 ![] 开头的行）
    body_content_without_cover = re.sub(r'^!\[.*?\]\(.*?\)\s*\n*', '', body_content, count=1)
    # 去掉 H1 标题行（以 # 开头的行）
    body_content_without_title = re.sub(r'^#\s+.*\n*', '', body_content_without_cover, count=1)

    # 去掉文章配图的 markdown 标记（因为需要用 media-insert 命令插入）
    body_content_clean = re.sub(r'\n!\[.*?\]\(.*?\)\n', '\n', body_content_without_title)

    # 将文章内容分成多个部分，交替插入截图
    num_images = len(article_images)
    if num_images > 0:
        content_parts = split_content_by_sections(body_content_clean, num_images)
    else:
        content_parts = [body_content_clean]

    # 交替追加内容和插图
    # 追加文章正文内容
    print("正在追加文章正文内容...")
    for i, part in enumerate(content_parts):
        # 追加内容
        print(f"正在追加第 {i + 1}/{len(content_parts)} 部分内容...")
        temp_file = Path("temp_article_content.md")
        temp_file.write_text(part, encoding="utf-8")

        cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_result["url"]}" --command append --content @temp_article_content.md --as bot'
        stdout, stderr, returncode = run_command(cmd, check=False)
        temp_file.unlink(missing_ok=True)

        if returncode != 0:
            print(f"追加第 {i + 1} 部分内容失败: {stderr[:100] if stderr else 'unknown error'}")
            continue

        # 插入插图（如果有）
        if i < num_images:
            img = article_images[i]
            img_path = img["path"]
            print(f"正在插入第 {i + 1} 张插图: {img_path.name}")
            if insert_media_to_doc(doc_result["url"], img_path, insert_at_top=False):
                print(f"第 {i + 1} 张插图插入成功")
            else:
                print(f"第 {i + 1} 张插图插入失败")

    # 更新文章的 frontmatter，添加飞书链接
    update_article_frontmatter(article_path, metadata, doc_result["url"])

    return doc_result


def update_article_frontmatter(article_path, metadata, feishu_url):
    """更新文章的 frontmatter，添加飞书链接"""
    # 更新 feishu_url
    metadata["feishu_url"] = feishu_url

    # 读取文章内容
    content = article_path.read_text(encoding="utf-8")

    # 解析 frontmatter
    _, body_content = parse_frontmatter(content)

    # 生成新的 frontmatter
    yaml_str = yaml.dump(metadata, allow_unicode=True, default_flow_style=False)

    # 组合新内容
    new_content = f"---\n{yaml_str}---\n\n{body_content}"

    # 写入文件
    article_path.write_text(new_content, encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("用法: python save_to_feishu.py <文章文件路径> [选项]")
        print("示例: python save_to_feishu.py articles/2026-06-02_minimax-m3.md")
        print("\n选项:")
        print("  --no-cover           不生成封面图")
        print("  --no-images          不添加文章配图")
        print("  --count N            原文截图数量（默认: 3）")
        sys.exit(1)

    article_file = sys.argv[1]
    generate_cover_flag = "--no-cover" not in sys.argv

    # 确定图片模式
    if "--no-images" in sys.argv:
        image_mode = "none"
    else:
        image_mode = "screenshot"

    # 获取插图数量
    count = 3
    for i, arg in enumerate(sys.argv):
        if arg == "--count" and i + 1 < len(sys.argv):
            count = int(sys.argv[i + 1])

    result = save_article_to_feishu(article_file, generate_cover_flag, image_mode, count)

    if result:
        print(f"\n保存成功!")
        print(f"文档链接: {result['url']}")
        if result.get("updated"):
            print("(已更新现有文档)")
    else:
        print("\n保存失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
