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
from pathlib import Path
from datetime import datetime


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
    # 使用 generate_cover.py 脚本
    cmd = f'python scripts/generate_cover.py "{title}" "{tag}" "{date}" "{subtitle}" covers/cover.html'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"生成封面 HTML 失败: {stderr}")
        return None

    # 使用 screenshot.py 截图
    cmd = 'python scripts/screenshot.py'
    stdout, stderr, returncode = run_command(cmd, check=False)

    if returncode != 0:
        print(f"截图失败: {stderr}")
        return None

    return Path("covers/cover-main.png")


def create_feishu_doc(title, content, folder_token=None):
    """创建飞书文档"""
    # 将内容写入临时文件
    temp_file = Path("temp_article_content.md")
    temp_file.write_text(content, encoding="utf-8")

    # 转义标题中的特殊字符
    escaped_title = title.replace('"', '\\"')

    # 构建命令
    cmd = f'npx @larksuite/cli docs +create --api-version v2 --doc-format markdown --as bot --content @temp_article_content.md'

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


def update_feishu_doc(doc_url, content, cover_image_path=None):
    """更新飞书文档内容"""
    # 如果有封面图，先删除文档内容，然后按正确顺序重建
    if cover_image_path:
        # 先清空文档内容（使用一个空格作为内容）
        temp_file = Path("temp_article_content.md")
        temp_file.write_text(" ", encoding="utf-8")

        cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command overwrite --doc-format markdown --as bot --content @temp_article_content.md'
        stdout, stderr, returncode = run_command(cmd, check=False)
        temp_file.unlink(missing_ok=True)

        if returncode != 0:
            print(f"清空文档失败: {stderr}")
            return False

        # 插入封面图到文档开头（现在文档是空的，所以会插入到最上方）
        insert_media_to_doc(doc_url, cover_image_path, insert_at_top=False)

        # 然后追加文章内容
        temp_file = Path("temp_article_content.md")
        temp_file.write_text(content, encoding="utf-8")

        cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command append --doc-format markdown --as bot --content @temp_article_content.md'
        stdout, stderr, returncode = run_command(cmd, check=False)
        temp_file.unlink(missing_ok=True)

        if returncode != 0:
            print(f"追加内容失败: {stderr}")
            return False

        return True
    else:
        # 没有封面图，直接覆盖内容
        temp_file = Path("temp_article_content.md")
        temp_file.write_text(content, encoding="utf-8")

        cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_url}" --command overwrite --doc-format markdown --as bot --content @temp_article_content.md'
        stdout, stderr, returncode = run_command(cmd, check=False)
        temp_file.unlink(missing_ok=True)

        if returncode != 0:
            print(f"更新文档失败: {stderr}")
            return False

        try:
            json_match = re.search(r'\{.*\}', stdout, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("ok", False)
        except json.JSONDecodeError:
            pass

        print(f"解析更新结果失败: {stdout}")
        return False


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


def save_article_to_feishu(article_file, generate_cover_flag=True):
    """保存文章到飞书文档"""
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
    feishu_url = metadata.get("feishu_url")

    print(f"正在保存到飞书: {title}")

    # 生成封面图
    cover_path = None
    if generate_cover_flag:
        # 生成副标题（从 tags 中提取）
        tags = metadata.get("tags", [])
        subtitle = "、".join(tags[:3]) if tags else "AI资讯"

        print("正在生成封面图...")
        cover_path = generate_cover(title, tag, date, subtitle)
        if cover_path:
            print(f"封面图生成成功: {cover_path}")

    # 如果已有飞书文档链接，更新文档
    if feishu_url:
        print(f"文档已存在，正在更新: {feishu_url}")

        # 更新文档内容（如果有封面图，会自动按正确顺序重建）
        if update_feishu_doc(feishu_url, body_content, cover_path):
            print("文档更新成功")
            return {"url": feishu_url, "updated": True}
        else:
            print("文档更新失败，将创建新文档")

    # 创建新文档（先创建带标题的空文档，然后按顺序插入内容）
    # 先创建一个带标题的空文档
    empty_content = f"<title>{title}</title><p> </p>"
    doc_result = create_feishu_doc(title, empty_content, FEISHU_FOLDER_TOKEN)
    if not doc_result:
        return None

    print(f"文档创建成功: {doc_result['url']}")

    # 插入封面图到文档开头
    if cover_path:
        print("正在插入封面图...")
        if insert_media_to_doc(doc_result["url"], cover_path, insert_at_top=False):
            print("封面图插入成功")

    # 处理文章内容：去掉开头的封面图和 H1 标题（因为标题已经设置为文档标题）
    # 先去掉封面图行，再去掉 H1 标题行
    import re
    # 去掉封面图行（以 ![] 开头的行）
    body_content_without_cover = re.sub(r'^!\[.*?\]\(.*?\)\s*\n*', '', body_content, count=1)
    # 去掉 H1 标题行（以 # 开头的行）
    body_content_without_title = re.sub(r'^#\s+.*\n*', '', body_content_without_cover, count=1)

    # 追加文章内容
    temp_file = Path("temp_article_content.md")
    temp_file.write_text(body_content_without_title, encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +update --api-version v2 --doc "{doc_result["url"]}" --command append --doc-format markdown --as bot --content @temp_article_content.md'
    stdout, stderr, returncode = run_command(cmd, check=False)
    temp_file.unlink(missing_ok=True)

    if returncode != 0:
        print(f"追加内容失败: {stderr}")
        return None

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
        print("用法: python save_to_feishu.py <文章文件路径> [--no-cover]")
        print("示例: python save_to_feishu.py articles/2025-05-27_mimo-price-drop.md")
        sys.exit(1)

    article_file = sys.argv[1]
    generate_cover_flag = "--no-cover" not in sys.argv

    result = save_article_to_feishu(article_file, generate_cover_flag)

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
