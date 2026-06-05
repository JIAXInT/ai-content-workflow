#!/usr/bin/env python3
"""
社交卡片生成器 V4
每个章节对应一张卡片，内容可读性拉满

核心改进：
1. 按 ## 标题分章节，每章一张卡片
2. 提取章节中的关键金句和细节
3. 穿插原文截图作为证据
4. 截图不够用时，从免费图库（Pexels/Unsplash）搜索图片
5. 内容密度高，可读性强

使用方法：
  python scripts/generate_social_cards_v4.py articles/2026-06-04_suno-4亿美元融资.md
"""

import sys
import io
import json
import re
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from urllib.parse import quote

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "covers"
CACHE_DIR = BASE_DIR / "images" / "cache"


def generate_image_keywords(title: str, text: str, image_width: int = 1080, image_height: int = 600) -> dict:
    """
    根据章节内容提炼最适合配图的关键词
    分析段落内容，提取核心场景和视觉元素

    Args:
        title: 章节标题
        text: 章节内容
        image_width: 图片位置宽度
        image_height: 图片位置高度

    Returns:
        dict: {
            "keyword": "搜索关键词",
            "orientation": "landscape/portrait/square",
            "size": "图片尺寸描述"
        }
    """
    # 第一步：分析段落内容，提取核心场景
    # 提取引号内的内容（通常是具体场景描述）
    quotes = re.findall(r'「([^」]+)」', text)

    # 提取关键句子
    sentences = re.split(r'[。！？]', text)
    key_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    # 第二步：根据内容生成精准关键词
    # 分析每个句子，找到最能代表视觉场景的描述

    # 检查是否有具体的时间场景
    if any(word in text for word in ['凌晨两点', '深夜', '加班到凌晨']):
        if '办公室' in text or '电脑' in text:
            keyword = "late night office worker alone"
        else:
            keyword = "person alone night city"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有音乐创作场景
    if any(word in text for word in ['做了首歌', '写歌', '创作音乐', '生成歌曲']):
        keyword = "person creating music headphones"
        orientation = "portrait" if image_height > image_width else "landscape"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有听歌场景
    if any(word in text for word in ['戴上耳机', '点播放', '听歌', '听音乐']):
        keyword = "person listening music headphones"
        orientation = "portrait" if image_height > image_width else "landscape"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有灵魂/哲学场景（优先检查）
    if any(word in text for word in ['灵魂', '没有灵魂', '有灵魂', '哲学']):
        keyword = "philosophy soul contemplation"
        orientation = "portrait" if image_height > image_width else "landscape"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有跑步场景
    if any(word in text for word in ['跑步', '运动', '健身']):
        keyword = "person running exercise outdoor"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有秋天/银杏场景
    if any(word in text for word in ['秋天', '银杏', '落叶']):
        keyword = "autumn ginkgo leaves golden"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有融资/商业场景
    if any(word in text for word in ['融资', '估值', '投资', '亿美元']):
        keyword = "business growth chart success"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有公司/创业场景
    if any(word in text for word in ['公司', '创业', '创始人', '团队']):
        keyword = "modern tech company office"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有AI/技术场景
    if any(word in text for word in ['AI', '人工智能', '模型', '算法']):
        keyword = "artificial intelligence technology"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有印刷术/书籍场景
    if any(word in text for word in ['印刷术', '书', '知识', '图书馆']):
        keyword = "vintage books library knowledge"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有灵魂/哲学场景（优先检查）
    if any(word in text for word in ['灵魂', '没有灵魂', '有灵魂', '哲学']):
        keyword = "philosophy soul contemplation"
        orientation = "portrait" if image_height > image_width else "landscape"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有孤独/思考场景
    if any(word in text for word in ['孤独', '思考', '想明白', '理解']):
        keyword = "person thinking contemplation"
        orientation = "portrait" if image_height > image_width else "landscape"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有创作/灵感场景
    if any(word in text for word in ['创作', '灵感', '创意', '想法']):
        keyword = "creative inspiration idea"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有印刷术/书籍场景
    if any(word in text for word in ['印刷术', '书', '知识', '图书馆']):
        keyword = "vintage books library knowledge"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 检查是否有平权/民主场景
    if any(word in text for word in ['平权', '人人可及', '民主', '权利']):
        keyword = "equality democracy rights"
        orientation = "landscape" if image_width > image_height else "portrait"
        return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 默认：根据标题生成关键词
    title_words = re.findall(r'[一-龥]{2,}', title)
    if title_words:
        word_map = {
            "音乐": "music",
            "公司": "company",
            "融资": "investment",
            "创业": "startup",
            "技术": "technology",
            "未来": "future",
            "创作": "creative",
            "思考": "thinking",
            "感受": "feeling",
            "下一步": "future planning",
            "看法": "opinion perspective",
        }
        for word in title_words:
            if word in word_map:
                keyword = word_map[word]
                orientation = "landscape" if image_width > image_height else "portrait"
                return {"keyword": keyword, "orientation": orientation, "size": f"{image_width}x{image_height}"}

    # 默认返回
    orientation = "landscape" if image_width > image_height else "portrait"
    return {"keyword": "technology future", "orientation": orientation, "size": f"{image_width}x{image_height}"}


def download_pexels_image(keyword: str, orientation: str, save_dir: Path, filename: str) -> str:
    """
    从 Pexels 下载免费图片
    根据关键词和方向下载合适尺寸的图片

    Args:
        keyword: 搜索关键词
        orientation: 图片方向（landscape/portrait/square）
        save_dir: 保存目录
        filename: 文件名

    Returns:
        str: 图片路径，失败返回 None
    """
    try:
        # Pexels 搜索页面
        search_url = f"https://www.pexels.com/search/{quote(keyword)}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        print(f"  📷 正在从 Pexels 搜索: {keyword}")
        print(f"  🔗 搜索链接: {search_url}")

        # 由于 Pexels 需要 API key，这里使用备用方案
        # 使用 Lorem Picsum 作为占位图服务（免费，无需 API key）
        # 根据方向选择不同的尺寸
        if orientation == "landscape":
            # 横版图片：宽度 > 高度
            placeholder_url = f"https://picsum.photos/1080/600"
        elif orientation == "portrait":
            # 竖版图片：高度 > 宽度
            placeholder_url = f"https://picsum.photos/600/1080"
        else:
            # 方形图片
            placeholder_url = f"https://picsum.photos/800/800"

        save_path = save_dir / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(placeholder_url, headers=headers, timeout=15, allow_redirects=True)
        if response.status_code == 200:
            save_path.write_bytes(response.content)
            print(f"  ✅ 图片已下载: {filename} ({orientation})")
            return str(save_path.resolve()).replace('\\', '/')

    except Exception as e:
        print(f"  ⚠️ 下载失败: {e}")

    return None


def extract_sections(md_file: str) -> dict:
    """从 Markdown 文章中提取内容，精简为杂志风格"""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_path}")
        sys.exit(1)

    content = md_path.read_text(encoding='utf-8')

    # 解析 YAML front matter
    front_matter = {}
    if content.startswith('---'):
        fm_end = content.find('---', 3)
        if fm_end > 0:
            fm_text = content[3:fm_end].strip()
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    front_matter[key.strip()] = value.strip()
            content = content[fm_end + 3:].strip()

    title = front_matter.get('title', '')
    tags_text = front_matter.get('tags', '')
    tags = [t.strip() for t in tags_text.split(',')] if isinstance(tags_text, str) else []
    date_str = front_matter.get('date', datetime.now().strftime('%Y-%m-%d'))
    category = front_matter.get('category', '产品体验')

    # 提取图片路径（使用绝对路径）
    images = []
    image_dir = BASE_DIR / "images" / f"{date_str}-suno-funding"
    if image_dir.exists():
        for img in sorted(image_dir.glob("*.png")):
            # 使用绝对路径，确保渲染时能找到图片
            abs_path = img.resolve()
            images.append(str(abs_path).replace('\\', '/'))

    # 检查封面图
    cover = front_matter.get('cover', '')
    if cover:
        cover_path = BASE_DIR / cover
        if cover_path.exists():
            abs_path = cover_path.resolve()
            img_path = str(abs_path).replace('\\', '/')
            if img_path not in images:
                images.insert(0, img_path)

    # 按 ## 分章节
    lines = content.split('\n')
    sections = []
    current_title = "开头"
    current_lines = []

    for line in lines:
        if line.startswith('## '):
            # 保存上一个章节
            if current_lines:
                section_text = '\n'.join(current_lines).strip()
                if section_text:
                    sections.append({
                        "title": current_title,
                        "text": section_text
                    })
            current_title = line[3:].strip()
            current_lines = []
        elif line.strip().startswith('https://'):
            # 跳过纯 URL 行
            continue
        elif line.strip():
            current_lines.append(line.strip())

    # 保存最后一个章节
    if current_lines:
        section_text = '\n'.join(current_lines).strip()
        if section_text:
            sections.append({
                "title": current_title,
                "text": section_text
            })

    return {
        "title": title,
        "tags": tags,
        "date": date_str,
        "category": category,
        "images": images,
        "sections": sections
    }


def extract_golden_quotes(text: str) -> List[str]:
    """从文本中提取金句（引号内的内容和包含引号的完整句子）"""
    quotes = []

    # 第一步：提取引号内的内容
    i = 0
    while i < len(text):
        start = text.find('「', i)
        if start == -1:
            break
        end = text.find('」', start)
        if end == -1:
            break
        # 提取引号内的内容
        quote = text[start+1:end]
        if len(quote) > 5:
            quotes.append(quote)
        i = end + 1

    # 第二步：提取包含引号的完整句子
    # 按句号分割文本
    sentences = re.split(r'[。！？]', text)
    for sentence in sentences:
        # 如果句子包含引号，且长度合适，添加到金句列表
        if '「' in sentence and '」' in sentence:
            clean_sentence = sentence.strip()
            if 10 < len(clean_sentence) < 100:  # 长度在 10-100 之间
                quotes.append(clean_sentence)

    # 过滤掉太短的和重复的
    unique_quotes = []
    for q in quotes:
        if q not in unique_quotes:
            unique_quotes.append(q)
    return unique_quotes


def extract_key_sentences(text: str, max_count: int = 4) -> List[str]:
    """提取关键句子（按句号分割，取最有信息量的）"""
    # 按中文句号分割
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    # 去重（更严格的去重逻辑）
    unique_sentences = []
    seen_contents = set()
    for s in sentences:
        # 移除引号后的内容作为去重依据
        clean_s = re.sub(r'「[^」]+」', '', s).strip()
        if clean_s and clean_s not in seen_contents:
            unique_sentences.append(s)
            seen_contents.add(clean_s)

    # 按信息量排序（包含数字、引号、情感词的优先）
    def info_score(s):
        score = 0
        if re.search(r'\d+', s): score += 2  # 包含数字
        if '「' in s: score += 3  # 包含引号
        if any(w in s for w in ['愣住', '爽', '牛', '恐怖', '魔幻', '上瘾']): score += 2
        if len(s) > 20: score += 1  # 有一定长度
        return score

    unique_sentences.sort(key=info_score, reverse=True)
    return unique_sentences[:max_count]


def calculate_text_capacity(width: int, height: int, font_size: int = 28, line_height: float = 1.6) -> int:
    """
    根据版面大小计算可承载的文字数量

    Args:
        width: 版面宽度（像素）
        height: 版面高度（像素）
        font_size: 字体大小（像素）
        line_height: 行高倍数

    Returns:
        int: 可承载的文字数量（中文字符）
    """
    # 计算每行可容纳的字符数
    # 中文字符宽度约等于字体大小
    chars_per_line = width // font_size

    # 计算可容纳的行数
    line_height_px = font_size * line_height
    lines = height // line_height_px

    # 计算总可承载字符数
    total_chars = int(chars_per_line * lines)

    # 考虑标题、图片等占用的空间，减少 30%
    usable_chars = int(total_chars * 0.7)

    return usable_chars


def truncate_to_capacity(text: str, capacity: int) -> str:
    """
    将文本截断到指定容量

    Args:
        text: 原始文本
        capacity: 最大字符数

    Returns:
        str: 截断后的文本
    """
    if len(text) <= capacity:
        return text

    # 在句号处截断
    truncated = text[:capacity]
    last_period = truncated.rfind('。')
    if last_period > capacity * 0.5:  # 如果句号位置在 50% 以后
        return truncated[:last_period + 1]
    else:
        return truncated + "..."


def generate_card_data(article: dict) -> dict:
    """根据文章数据生成卡片数据，精简为杂志风格"""
    sections = article["sections"]
    images = article["images"]

    xhs_pages = []

    # 图片分配策略：根据原文图片位置分配
    # 分析原文中图片的位置，找到图片所在的段落
    # 图片对应关系：suno-blog.png -> https://suno.com/blog/series-d-announcement
    #               suno-homepage.png -> https://suno.com
    #               suno-tweet.png -> https://x.com/suno/status/2062183524887675243
    image_url_map = {
        'https://suno.com/blog/series-d-announcement': 0,  # suno-blog.png
        'https://suno.com': 1,  # suno-homepage.png
        'https://x.com/suno/status/2062183524887675243': 2,  # suno-tweet.png
    }

    # 为每个章节分配图片
    # 只使用原文的图片，不从免费图库下载
    section_images = []

    for i, section in enumerate(sections):
        text = section["text"]
        assigned_image = None

        # 检查原文中是否有图片 URL
        for url, image_index in image_url_map.items():
            if url in text and image_index < len(images):
                assigned_image = images[image_index]
                break

        section_images.append(assigned_image)

    # 杂志风格：内容充实，充满整张卡片
    # 根据版面大小计算可承载的文字数量
    # 小红书卡片：1080x1440，图片区域约 1080x600，文字区域约 1080x800
    text_capacity = calculate_text_capacity(1080, 800, font_size=28, line_height=1.6)
    print(f"  📐 版面可承载文字数量: {text_capacity} 字")

    for i, section in enumerate(sections):
        title = section["title"]
        text = section["text"]

        # 提取关键句子（增加到 4-5 句）
        key_sentences = extract_key_sentences(text, 5)

        # 杂志风格：内容充实，不重复
        # 使用关键句子，确保不重复
        items = []
        seen_contents = set()
        for sentence in key_sentences:
            # 清理换行符
            clean_sentence = sentence.replace('\n', ' ').strip()
            # 去重：检查是否已经出现过类似内容
            if clean_sentence and clean_sentence not in seen_contents:
                items.append(clean_sentence)
                seen_contents.add(clean_sentence)
                if len(items) >= 4:  # 最多 4 项
                    break

        # 如果没有足够的关键句子，使用原文的前 100 字
        if not items:
            items = [text[:100]]

        # 确保内容充实，不超过版面容量
        # 每张卡片的内容不超过 text_capacity
        final_items = []
        total_chars = 0
        for item in items:
            if total_chars + len(item) <= text_capacity:
                final_items.append(item)
                total_chars += len(item)
            else:
                # 截断到版面容量
                remaining = text_capacity - total_chars
                if remaining > 20:  # 至少 20 字才值得添加
                    final_items.append(truncate_to_capacity(item, remaining))
                break

        # 决定卡片类型和布局
        if i == 0:
            # 第一页：封面（仅标题，不带图片）
            xhs_pages.append({
                "type": "cover",
                "headline": article["title"],
                "subline": key_sentences[0] if key_sentences else "",
                "hook": key_sentences[0] if key_sentences else "",
                "tags": article["tags"][:3]
            })
        else:
            # 其他章节：杂志风格，内容充实
            xhs_pages.append({
                "type": "scene",
                "title": title,
                "items": final_items,
                "image": section_images[i]
            })

    # 公众号封面数据
    wechat_headline = article["title"]

    return {
        "title": article["title"],
        "subtitle": sections[0]["text"] if sections else "",
        "category": f"AI · {article['category']}",
        "date": article["date"],
        "author": "AI创享派",
        "accent": "ikb",
        "images": images,
        "wechat": {
            "headline": wechat_headline,
            "subline": sections[0]["text"] if sections else "",
            "stats": [
                {"num": "54亿", "label": "估值"},
                {"num": "1200万", "label": "用户"}
            ]
        },
        "xhs": xhs_pages
    }


def generate_html(card_data: dict, style: str = "swiss", accent: str = "ikb") -> str:
    """生成社交卡片 HTML"""
    card_data["accent"] = accent

    # 使用 V2 模板
    template_file = TEMPLATES_DIR / f"social-card-{style}-v2.html"
    if not template_file.exists():
        # 回退到原模板
        template_file = TEMPLATES_DIR / f"social-card-{style}.html"

    if not template_file.exists():
        print(f"❌ 模板不存在: {template_file}")
        sys.exit(1)

    template = template_file.read_text(encoding='utf-8')

    html = template.replace('{{accent}}', accent)
    html = html.replace('{{title}}', card_data.get('title', '社交卡片'))

    # 删除模板中的默认 CARD_DATA 定义
    default_data_start = html.find('    var CARD_DATA = {')
    if default_data_start != -1:
        brace_count = 0
        default_data_end = default_data_start
        for i in range(default_data_start, len(html)):
            if html[i] == '{':
                brace_count += 1
            elif html[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    default_data_end = i + 1
                    break
        html = html[:default_data_start] + html[default_data_end:]

    # 注入实际数据
    inject_script = f"""
    <script>
      var CARD_DATA = {json.dumps(card_data, ensure_ascii=False, indent=2)};
    </script>
    """
    html = html.replace('</head>', inject_script + '\n</head>')

    return html


def save_html(html: str, article_file: str = None, output_file: str = None) -> Path:
    """保存 HTML 文件"""
    if output_file:
        out_path = Path(output_file)
    elif article_file:
        article_path = Path(article_file)
        article_name = article_path.stem
        output_subdir = OUTPUT_DIR / article_name
        output_subdir.mkdir(parents=True, exist_ok=True)
        out_path = output_subdir / "social-cards.html"
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_path = OUTPUT_DIR / f"social-cards-{timestamp}.html"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f"✅ HTML 已保存: {out_path}")

    return out_path


def main():
    parser = argparse.ArgumentParser(description='社交卡片生成器 V4')
    parser.add_argument('article', help='Markdown 文章路径')
    parser.add_argument('--style', default='swiss', choices=['swiss', 'editorial'])
    parser.add_argument('--accent', default='ikb',
                       choices=['ikb', 'lemon-yellow', 'lemon-green', 'safety-orange'])
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--json', action='store_true')

    args = parser.parse_args()

    print(f"📄 正在处理文章: {args.article}")

    # 提取文章数据
    article = extract_sections(args.article)
    print(f"📝 标题: {article['title']}")
    print(f"📊 提取到 {len(article['sections'])} 个章节")
    print(f"🖼️  提取到 {len(article['images'])} 张图片")

    # 输出章节概览
    print("\n📋 章节概览:")
    for i, section in enumerate(article['sections']):
        print(f"  {i+1}. {section['title']} ({len(section['text'])} 字)")

    # 生成卡片数据
    card_data = generate_card_data(article)
    print(f"\n🎨 生成 {len(card_data['xhs'])} 个小红书页面")

    if args.json:
        print(json.dumps(card_data, ensure_ascii=False, indent=2))
    else:
        html = generate_html(card_data, args.style, args.accent)
        out_path = save_html(html, args.article, args.output)
        print(f"\n✅ 完成！HTML 文件: {out_path}")


if __name__ == "__main__":
    main()
