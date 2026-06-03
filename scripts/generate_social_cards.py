#!/usr/bin/env python3
"""
社交卡片生成器
从 Markdown 文章中提取内容，生成社交卡片 HTML

支持：
- 公众号封面（21:9 + 1:1）
- 小红书轮播图（3:4 × 5-9 页）

使用方法：
  python scripts/generate_social_cards.py articles/2025-05-27_mimo-25-pro-price-drop.md
  python scripts/generate_social_cards.py articles/your-article.md --style swiss --accent ikb
"""

import sys
import io
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "covers"


def extract_article_data(md_file: str) -> dict:
    """
    从 Markdown 文章中提取结构化数据

    Args:
        md_file: Markdown 文件路径

    Returns:
        提取的数据字典
    """
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

    # 从 front_matter 获取标题
    title = front_matter.get('title', '')
    if not title:
        # 尝试从内容提取标题（第一个 # 标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "未命名文章"

    # 从 front_matter 获取标签
    tags = []
    if 'tags' in front_matter:
        # 处理 YAML 列表格式
        tags_text = front_matter['tags']
        if isinstance(tags_text, str):
            tags = [t.strip().strip('- ') for t in tags_text.split(',')]
        else:
            tags = tags_text

    # 从 front_matter 获取日期
    date_str = front_matter.get('date', datetime.now().strftime('%Y-%m-%d'))

    # 从 front_matter 获取分类
    category_text = front_matter.get('category', '产品发布')
    category = f"AI · {category_text}"

    # 提取副标题（第一个非标题段落）
    subtitle = ""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('## ') and i > 0:
            subtitle = line[3:].strip()
            break
        elif line.strip() and not line.startswith('#') and not line.startswith('!') and i > 2:
            subtitle = line.strip()[:50]
            break

    # 提取关键数据点（数字、百分比）
    stats = []
    # 匹配常见数据模式
    patterns = [
        r'(\d+(?:\.\d+)?%)',  # 百分比
        r'(\d+(?:\.\d+)?[×xX]\d*)',  # 倍数
        r'(\d+(?:\.\d+)?(?:亿|万|千|百)?(?:美元|元|人民币|美金))',  # 金额
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches[:3]:  # 最多取 3 个
            if match not in stats:
                stats.append(match)

    # 提取标签（从文件名或内容中）
    tags = []
    # 从文件名提取日期
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', md_path.name)
    date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')

    # 从内容提取关键词
    keyword_patterns = [
        r'(?:AI|人工智能|机器学习|深度学习|大模型|LLM|GPT|Claude|MiMo|DeepSeek)',
        r'(?:开源|闭源|API|模型|训练|推理|部署)',
        r'(?:降价|涨价|免费|付费|订阅|套餐)',
    ]
    for pattern in keyword_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches[:2]:
            if match not in tags:
                tags.append(match)

    # 如果标签不足，添加默认标签
    if len(tags) < 3:
        tags.extend(["AI", "科技", "前沿"][:3 - len(tags)])

    # 提取要点列表
    points = []
    for line in lines:
        if re.match(r'^\s*[-*]\s+', line):
            point = re.sub(r'^\s*[-*]\s+', '', line).strip()
            if point and len(point) < 100:
                points.append(point)

    # 提取结论
    conclusions = []
    in_conclusion = False
    for line in lines:
        if '总结' in line or '结论' in line:
            in_conclusion = True
            continue
        if in_conclusion and re.match(r'^\s*\d+[\.\)、]', line):
            conclusion = re.sub(r'^\s*\d+[\.\)、]\s*', '', line).strip()
            if conclusion:
                conclusions.append(conclusion)

    return {
        "title": title,
        "subtitle": subtitle,
        "date": date_str,
        "tags": tags[:5] if tags else ["AI", "科技", "前沿"],
        "stats": stats[:4],
        "points": points[:5],
        "conclusions": conclusions[:3],
        "category": category
    }


def generate_card_data(article_data: dict) -> dict:
    """
    根据文章数据生成卡片数据结构

    Args:
        article_data: 文章提取的数据

    Returns:
        卡片数据字典
    """
    title = article_data["title"]
    subtitle = article_data["subtitle"]
    stats = article_data["stats"]
    points = article_data["points"]
    conclusions = article_data["conclusions"]
    tags = article_data["tags"]

    # 构建公众号封面数据
    wechat_headline = title.replace("：", " ").replace("，", " ").replace("、", " ")
    # 如果标题太长，截断
    if len(wechat_headline) > 30:
        wechat_headline = wechat_headline[:28] + "..."

    wechat_stats = []
    if stats:
        wechat_stats.append({"num": stats[0], "label": "关键指标"})
    if len(stats) > 1:
        wechat_stats.append({"num": stats[1], "label": "重要数据"})

    # 构建小红书轮播图数据
    xhs_pages = []

    # 第 1 页：封面
    xhs_pages.append({
        "type": "cover",
        "headline": title[:20] if len(title) > 20 else title,
        "subline": subtitle[:30] if len(subtitle) > 30 else subtitle,
        "tags": tags
    })

    # 第 2 页：核心数据（如果有数据）
    if stats:
        xhs_pages.append({
            "type": "data",
            "title": "核心数据",
            "stats": [
                {"num": stats[0] if len(stats) > 0 else "N/A", "label": "指标1", "height": "90%"},
                {"num": stats[1] if len(stats) > 1 else "N/A", "label": "指标2", "height": "75%"},
                {"num": stats[2] if len(stats) > 2 else "N/A", "label": "指标3", "height": "60%"},
                {"num": stats[3] if len(stats) > 3 else "N/A", "label": "指标4", "height": "85%"}
            ],
            "note": "数据来源：文章内容"
        })

    # 第 3 页：要点列表（如果有要点）
    if points:
        xhs_pages.append({
            "type": "checklist",
            "title": "核心要点",
            "items": [{"item": p[:20], "note": ""} for p in points[:5]],
            "highlight": points[0] if points else ""
        })

    # 第 4 页：对比（如果有足够内容）
    if len(points) >= 2:
        xhs_pages.append({
            "type": "compare",
            "title": "对比分析",
            "left": {
                "cat": "优势",
                "name": "亮点",
                "features": points[:3]
            },
            "right": {
                "cat": "挑战",
                "name": "风险",
                "features": points[3:6] if len(points) > 3 else ["待补充"]
            },
            "note": "综合分析"
        })

    # 第 5 页：总结
    if conclusions:
        xhs_pages.append({
            "type": "summary",
            "title": "关键结论",
            "conclusions": [
                {"num": "01", "title": c[:15], "desc": c}
                for c in conclusions[:3]
            ],
            "cta": "关注 AI创享派，获取最新 AI 资讯"
        })
    else:
        # 如果没有明确的结论，生成默认总结
        xhs_pages.append({
            "type": "summary",
            "title": "三个关键结论",
            "conclusions": [
                {"num": "01", "title": "技术驱动", "desc": title},
                {"num": "02", "title": "行业影响", "desc": subtitle or "值得关注"},
                {"num": "03", "title": "未来趋势", "desc": "持续关注 AI 发展"}
            ],
            "cta": "关注 AI创享派，获取最新 AI 资讯"
        })

    return {
        "title": title,
        "subtitle": subtitle,
        "category": article_data["category"],
        "date": article_data["date"],
        "author": "AI创享派",
        "accent": "ikb",
        "wechat": {
            "headline": wechat_headline,
            "subline": subtitle[:40] if subtitle else title[:40],
            "stats": wechat_stats if wechat_stats else [
                {"num": "AI", "label": "前沿"}
            ]
        },
        "xhs": xhs_pages
    }


def generate_html(card_data: dict, style: str = "swiss", accent: str = "ikb") -> str:
    """
    生成社交卡片 HTML

    Args:
        card_data: 卡片数据
        style: 样式（swiss 或 editorial）
        accent: 强调色

    Returns:
        HTML 字符串
    """
    # 设置强调色
    card_data["accent"] = accent

    # 加载模板
    template_file = TEMPLATES_DIR / f"social-card-{style}.html"
    if not template_file.exists():
        print(f"❌ 模板不存在: {template_file}")
        sys.exit(1)

    template = template_file.read_text(encoding='utf-8')

    # 替换模板中的占位符
    html = template.replace('{{accent}}', accent)
    html = html.replace('{{title}}', card_data.get('title', '社交卡片'))

    # 删除模板中的默认 CARD_DATA 定义
    # 找到默认数据的开始和结束位置
    default_data_start = html.find('    var CARD_DATA = {')
    if default_data_start != -1:
        # 找到默认数据的结束位置（对应的闭合大括号）
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

        # 删除默认数据定义
        html = html[:default_data_start] + html[default_data_end:]

    # 在模板中注入实际数据
    inject_script = f"""
    <script>
      // 注入的实际数据
      var CARD_DATA = {json.dumps(card_data, ensure_ascii=False, indent=2)};
    </script>
    """

    # 在 </head> 前注入数据脚本
    html = html.replace('</head>', inject_script + '\n</head>')

    return html


def save_html(html: str, article_file: str = None, output_file: str = None) -> Path:
    """
    保存 HTML 文件

    Args:
        html: HTML 内容
        article_file: 文章文件路径（用于生成目录名）
        output_file: 输出文件路径

    Returns:
        保存的文件路径
    """
    if output_file:
        out_path = Path(output_file)
    elif article_file:
        # 从文章文件名生成目录名
        article_path = Path(article_file)
        article_name = article_path.stem  # 例如：2025-05-27_mimo-25-pro-price-drop

        # 创建以文章名命名的子目录
        output_subdir = OUTPUT_DIR / article_name
        output_subdir.mkdir(parents=True, exist_ok=True)

        # HTML 文件保存到子目录中
        out_path = output_subdir / "social-cards.html"
    else:
        # 生成默认文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_path = OUTPUT_DIR / f"social-cards-{timestamp}.html"

    # 确保目录存在
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存文件
    out_path.write_text(html, encoding='utf-8')
    print(f"✅ HTML 已保存: {out_path}")

    return out_path


def main():
    parser = argparse.ArgumentParser(description='社交卡片生成器')
    parser.add_argument('article', help='Markdown 文章路径')
    parser.add_argument('--style', default='swiss', choices=['swiss', 'editorial'],
                       help='卡片样式 (默认: swiss)')
    parser.add_argument('--accent', default='ikb',
                       choices=['ikb', 'lemon-yellow', 'lemon-green', 'safety-orange'],
                       help='强调色 (默认: ikb)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--json', action='store_true', help='只输出 JSON 数据，不生成 HTML')

    args = parser.parse_args()

    print(f"📄 正在处理文章: {args.article}")
    print()

    # 提取文章数据
    article_data = extract_article_data(args.article)
    print(f"📝 提取的数据:")
    print(f"  - 标题: {article_data['title']}")
    print(f"  - 日期: {article_data['date']}")
    print(f"  - 标签: {', '.join(article_data['tags'])}")
    print(f"  - 数据点: {len(article_data['stats'])} 个")
    print(f"  - 要点: {len(article_data['points'])} 个")
    print()

    # 生成卡片数据
    card_data = generate_card_data(article_data)

    if args.json:
        # 只输出 JSON
        print(json.dumps(card_data, ensure_ascii=False, indent=2))
        return

    # 生成 HTML
    print(f"🎨 正在生成 {args.style} 风格卡片...")
    html = generate_html(card_data, args.style, args.accent)

    # 保存文件
    saved_path = save_html(html, args.article, args.output)

    print()
    print("✨ 生成完成！")
    print(f"📁 文件: {saved_path}")
    print()
    print("下一步:")
    print(f"  1. 在浏览器中打开查看效果")
    print(f"  2. 运行渲染脚本生成 PNG:")
    print(f"     python scripts/render_social_cards.py {saved_path}")


if __name__ == "__main__":
    main()
