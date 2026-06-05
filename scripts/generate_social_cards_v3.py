#!/usr/bin/env python3
"""
社交卡片生成器 V3
基于 guizang-social-card-skill 最佳实践优化

核心改进（解决 V2 的问题）：
1. 插入素材图片：从文章中提取图片路径，插入到卡片中
2. 内容更丰富：更精细地提取文章内容，包括具体细节、情感表达、关键数据等
3. 品类适配：根据文章类型自动选择视觉风格
4. 布局多样化：引入更多 S01-S12 布局变体

使用方法：
  python scripts/generate_social_cards_v3.py articles/2026-06-04_suno-4亿美元融资.md
  python scripts/generate_social_cards_v3.py articles/your-article.md --style swiss --accent ikb
"""

import sys
import io
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "covers"


# ============================================================
# 1. 内容规划：压缩阶梯 + 页面角色（优化版）
# ============================================================

class ContentPlanner:
    """内容规划器：从原文压缩到页面计划（V3 优化版）"""

    # 页面角色定义（参考 guizang-social-card-skill 的 Good Page Roles）
    PAGE_ROLES = {
        "cover": "封面钩子",
        "problem": "问题场景",
        "misconception": "误解 vs 现实",
        "checklist": "清单/指南",
        "comparison": "对比分析",
        "evidence": "截图/产品证据",
        "quote": "大引用/结论",
        "steps": "步骤流程",
        "gear": "装备/列表",
        "summary": "总结页",
        "data": "数据展示",
        "scene": "场景/氛围",
        "story": "故事/体验",
        "insight": "洞察/观点"
    }

    def __init__(self, article_data: dict):
        self.article_data = article_data
        self.title = article_data.get("title", "")
        self.subtitle = article_data.get("subtitle", "")
        self.content = article_data.get("content", "")
        self.stats = article_data.get("stats", [])
        self.points = article_data.get("points", [])
        self.conclusions = article_data.get("conclusions", [])
        self.tags = article_data.get("tags", [])
        self.urls = article_data.get("urls", [])
        self.images = article_data.get("images", [])
        self.paragraphs = article_data.get("paragraphs", [])

    def compress_to_core_claim(self) -> str:
        """压缩阶梯第1层：核心主张（一句话）"""
        if self.subtitle:
            return f"{self.title}：{self.subtitle[:30]}"
        return self.title[:50]

    def extract_viewer_promise(self) -> str:
        """压缩阶梯第2层：读者承诺（滑动后能得到什么）"""
        if self.conclusions:
            return f"看完你能了解：{self.conclusions[0][:20]}"
        if self.points:
            return f"核心要点：{self.points[0][:20]}"
        return "获取关键洞察"

    def extract_rich_content(self) -> Dict:
        """提取丰富的内容（V3 优化）"""
        rich_content = {
            "emotional_moments": [],  # 情感时刻
            "specific_details": [],   # 具体细节
            "key_quotes": [],         # 关键引用
            "story_segments": [],     # 故事片段
            "insights": [],           # 洞察观点
            "data_points": [],        # 数据点
            "comparisons": [],        # 对比
            "questions": []           # 问题
        }

        # 提取情感时刻（包含情感词的句子）
        emotional_words = ["愣住了", "太爽了", "太牛了", "恐怖", "魔幻", "上瘾", "震惊"]
        for para in self.paragraphs:
            for word in emotional_words:
                if word in para:
                    rich_content["emotional_moments"].append(para[:100])
                    break

        # 提取具体细节（包含具体场景的句子）
        detail_indicators = ["凌晨两点", "办公室", "屏幕", "吉他", "lo-fi", "银杏叶", "长安街"]
        for para in self.paragraphs:
            for indicator in detail_indicators:
                if indicator in para:
                    rich_content["specific_details"].append(para[:100])
                    break

        # 提取关键引用（包含引号的句子）
        for para in self.paragraphs:
            if "「" in para and "」" in para:
                # 提取引号内的内容
                quotes = re.findall(r'「([^」]+)」', para)
                for quote in quotes[:2]:
                    if len(quote) > 10 and len(quote) < 50:
                        rich_content["key_quotes"].append(quote)

        # 提取故事片段（按段落分割的故事）
        story_keywords = ["于是我", "我开始", "第一首", "第二首", "第三首", "后来"]
        for para in self.paragraphs:
            for keyword in story_keywords:
                if keyword in para:
                    rich_content["story_segments"].append(para[:120])
                    break

        # 提取洞察观点（包含"我觉得"、"我认为"的句子）
        insight_indicators = ["我觉得", "我认为", "我后来想明白了", "说到底", "其实"]
        for para in self.paragraphs:
            for indicator in insight_indicators:
                if indicator in para:
                    rich_content["insights"].append(para[:100])
                    break

        # 提取数据点
        rich_content["data_points"] = self.stats[:4]

        # 提取对比（包含"以前"、"现在"的句子）
        comparison_indicators = ["以前", "现在", "不是", "而是"]
        for para in self.paragraphs:
            for indicator in comparison_indicators:
                if indicator in para:
                    rich_content["comparisons"].append(para[:100])
                    break

        # 提取问题（包含问号的句子）
        for para in self.paragraphs:
            if "？" in para or "?" in para:
                rich_content["questions"].append(para[:80])

        return rich_content

    def map_sections(self) -> List[Dict]:
        """压缩阶梯第3层：章节映射（4-8个观点）- V3 优化版"""
        sections = []
        rich_content = self.extract_rich_content()

        # 1. 封面钩子（使用情感时刻或具体细节）
        hook = self._generate_hook()
        if rich_content["emotional_moments"]:
            hook = rich_content["emotional_moments"][0][:30]
        sections.append({
            "role": "cover",
            "hook": hook,
            "visual": "hero_image",
            "image": self.images[0] if self.images else None
        })

        # 2. 数据展示（如果有数据）
        if self.stats:
            sections.append({
                "role": "data",
                "title": "核心数据",
                "items": self.stats[:4],
                "note": "数据来源：官方公告"
            })

        # 3. 故事/体验（使用故事片段）
        if rich_content["story_segments"]:
            sections.append({
                "role": "story",
                "title": "我的体验",
                "items": rich_content["story_segments"][:3],
                "image": self.images[1] if len(self.images) > 1 else None
            })

        # 4. 关键引用（使用引号内容）
        if rich_content["key_quotes"]:
            sections.append({
                "role": "quote",
                "text": rich_content["key_quotes"][0],
                "source": "体验感受"
            })

        # 5. 问题场景（使用问题）
        if rich_content["questions"]:
            sections.append({
                "role": "problem",
                "title": "核心问题",
                "items": rich_content["questions"][:2]
            })

        # 6. 要点清单
        if len(self.points) >= 2:
            sections.append({
                "role": "checklist",
                "title": "核心要点",
                "items": self.points[:5]
            })

        # 7. 对比分析（使用对比内容）
        if rich_content["comparisons"]:
            sections.append({
                "role": "comparison",
                "title": "对比分析",
                "left": {"name": "以前", "items": [rich_content["comparisons"][0]]},
                "right": {"name": "现在", "items": [rich_content["comparisons"][1] if len(rich_content["comparisons"]) > 1 else ""]}
            })

        # 8. 洞察观点
        if rich_content["insights"]:
            sections.append({
                "role": "insight",
                "title": "核心洞察",
                "items": rich_content["insights"][:2]
            })

        # 9. 总结
        sections.append({
            "role": "summary",
            "title": "关键结论",
            "items": self.conclusions[:3] if self.conclusions else ["持续关注"]
        })

        return sections

    def _generate_hook(self) -> str:
        """生成封面钩子（参考 guizang 的 Cover Hook Patterns）"""
        # 根据内容选择合适的钩子
        if "融资" in self.title or "估值" in self.title:
            return f"{self.title[:15]}，发生了什么？"
        elif "AI" in self.title:
            return f"AI 新动态：{self.title[:15]}"
        else:
            return self.title[:20]

    def plan_pages(self, max_pages: int = 7) -> List[Dict]:
        """压缩阶梯第4层：页面计划"""
        sections = self.map_sections()

        # 限制页面数量
        if len(sections) > max_pages:
            sections = [sections[0]] + sections[1:max_pages-1] + [sections[-1]]

        # 为每个章节生成页面计划
        pages = []
        for i, section in enumerate(sections):
            page = {
                "index": i + 1,
                "role": section["role"],
                "layout": self._choose_layout(section["role"]),
                "content": section
            }
            pages.append(page)

        return pages

    def _choose_layout(self, role: str) -> str:
        """根据角色选择布局（参考 guizang 的 S01-S12）"""
        layout_map = {
            "cover": "S01",        # Cover: Hook + Visual
            "data": "S03",         # Data Matrix
            "problem": "S05",      # Problem Scene
            "checklist": "S06",    # Checklist
            "comparison": "S07",   # Comparison
            "evidence": "S08",     # Image Hero
            "quote": "S04",        # Pull Quote
            "steps": "S09",        # Steps Flow
            "gear": "S10",         # Gear List
            "summary": "S11",      # Summary
            "scene": "S02",        # Scene
            "story": "S08",        # Image Hero (for story)
            "insight": "S04",      # Pull Quote (for insight)
        }
        return layout_map.get(role, "S01")


# ============================================================
# 2. 数据提取：从 Markdown 提取结构化数据（优化版）
# ============================================================

def extract_article_data(md_file: str) -> dict:
    """从 Markdown 文章中提取结构化数据（V3 优化版）"""
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
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "未命名文章"

    # 从 front_matter 获取标签
    tags = []
    if 'tags' in front_matter:
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
    patterns = [
        r'(\d+(?:\.\d+)?%)',
        r'(\d+(?:\.\d+)?[×xX]\d*)',
        r'(\d+(?:\.\d+)?(?:亿|万|千|百)?(?:美元|元|人民币|美金))',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches[:3]:
            if match not in stats:
                stats.append(match)

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

    # 提取 URL
    urls = re.findall(r'https?://[^\s\)\]\"\'<>]+', content)

    # 提取图片路径（V3 优化）
    images = []
    # 从文章目录查找图片
    article_dir = md_path.parent
    # 尝试多种可能的图片目录名
    possible_image_dirs = [
        BASE_DIR / "images" / f"{date_str}-{md_path.stem.split('_', 1)[1] if '_' in md_path.stem else md_path.stem}",
        BASE_DIR / "images" / md_path.stem,
        BASE_DIR / "images" / f"{date_str}-suno-funding",
    ]

    for image_dir in possible_image_dirs:
        if image_dir.exists():
            for img_file in image_dir.glob("*.png"):
                img_path = str(img_file.relative_to(BASE_DIR))
                # 将反斜杠替换为正斜杠（Windows 路径问题）
                img_path = img_path.replace('\\', '/')
                if img_path not in images:
                    images.append(img_path)
            for img_file in image_dir.glob("*.jpg"):
                img_path = str(img_file.relative_to(BASE_DIR))
                # 将反斜杠替换为正斜杠（Windows 路径问题）
                img_path = img_path.replace('\\', '/')
                if img_path not in images:
                    images.append(img_path)

    # 从 front_matter 获取封面图
    cover = front_matter.get('cover', '')
    if cover:
        # 将反斜杠替换为正斜杠
        cover = cover.replace('\\', '/')
        if cover not in images:
            images.insert(0, cover)

    # 提取段落（V3 优化）
    paragraphs = []
    current_para = []
    for line in lines:
        if line.strip():
            current_para.append(line.strip())
        else:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
    if current_para:
        paragraphs.append(' '.join(current_para))

    # 如果要点不足，从内容中提取
    if len(points) < 3:
        for line in lines:
            if line.startswith('## '):
                point = line[3:].strip()
                if point and point not in points:
                    points.append(point)

    return {
        "title": title,
        "subtitle": subtitle,
        "content": content,
        "date": date_str,
        "tags": tags[:5] if tags else ["AI", "科技", "前沿"],
        "stats": stats[:4],
        "points": points[:6],
        "conclusions": conclusions[:3],
        "category": category,
        "urls": urls[:5],
        "images": images[:5],  # 最多 5 张图片
        "paragraphs": paragraphs[:20]  # 最多 20 个段落
    }


# ============================================================
# 3. 卡片数据生成：基于页面计划（优化版）
# ============================================================

def generate_card_data_v3(article_data: dict) -> dict:
    """根据文章数据生成卡片数据结构（V3 优化版）"""
    planner = ContentPlanner(article_data)
    pages = planner.plan_pages(max_pages=7)

    title = article_data["title"]
    subtitle = article_data["subtitle"]
    tags = article_data["tags"]
    images = article_data["images"]

    # 构建小红书轮播图数据
    xhs_pages = []

    for page in pages:
        role = page["role"]
        layout = page["layout"]
        content = page["content"]

        if role == "cover":
            xhs_pages.append({
                "type": "cover",
                "layout": layout,
                "headline": title[:20] if len(title) > 20 else title,
                "subline": subtitle[:30] if len(subtitle) > 30 else subtitle,
                "hook": content.get("hook", title[:20]),
                "tags": tags[:3],
                "image": content.get("image") or (images[0] if images else None)
            })

        elif role == "data":
            stats = content.get("items", [])
            xhs_pages.append({
                "type": "data",
                "layout": layout,
                "title": content.get("title", "核心数据"),
                "stats": [
                    {"num": s, "label": f"指标{i+1}", "height": f"{90 - i*15}%"}
                    for i, s in enumerate(stats[:4])
                ],
                "note": content.get("note", "数据来源：文章内容")
            })

        elif role == "story":
            items = content.get("items", [])
            xhs_pages.append({
                "type": "scene",
                "layout": layout,
                "title": content.get("title", "我的体验"),
                "items": items[:3],
                "image": content.get("image") or (images[1] if len(images) > 1 else None),
                "note": "真实体验分享"
            })

        elif role == "quote":
            xhs_pages.append({
                "type": "quote",
                "layout": layout,
                "text": content.get("text", ""),
                "source": content.get("source", "核心观点")
            })

        elif role == "problem":
            items = content.get("items", [])
            xhs_pages.append({
                "type": "scene",
                "layout": layout,
                "title": content.get("title", "核心问题"),
                "items": items[:3],
                "note": "需要关注的问题"
            })

        elif role == "checklist":
            items = content.get("items", [])
            xhs_pages.append({
                "type": "checklist",
                "layout": layout,
                "title": content.get("title", "核心要点"),
                "items": [{"item": p[:25], "note": ""} for p in items[:5]],
                "highlight": items[0] if items else ""
            })

        elif role == "comparison":
            left = content.get("left", {})
            right = content.get("right", {})
            xhs_pages.append({
                "type": "compare",
                "layout": layout,
                "title": content.get("title", "对比分析"),
                "left": {
                    "cat": left.get("name", "以前"),
                    "name": left.get("name", "以前"),
                    "features": left.get("items", [])[:3]
                },
                "right": {
                    "cat": right.get("name", "现在"),
                    "name": right.get("name", "现在"),
                    "features": right.get("items", [])[:3]
                },
                "note": "对比分析"
            })

        elif role == "insight":
            items = content.get("items", [])
            xhs_pages.append({
                "type": "quote",
                "layout": layout,
                "text": items[0] if items else "",
                "source": content.get("title", "核心洞察")
            })

        elif role == "summary":
            items = content.get("items", [])
            xhs_pages.append({
                "type": "summary",
                "layout": layout,
                "title": content.get("title", "关键结论"),
                "conclusions": [
                    {"num": f"0{i+1}", "title": c[:15], "desc": c}
                    for i, c in enumerate(items[:3])
                ],
                "cta": "关注 AI创享派，获取最新 AI 资讯"
            })

    # 构建公众号封面数据
    wechat_headline = title.replace("：", " ").replace("，", " ").replace("、", " ")
    if len(wechat_headline) > 30:
        wechat_headline = wechat_headline[:28] + "..."

    wechat_stats = []
    if article_data["stats"]:
        wechat_stats.append({"num": article_data["stats"][0], "label": "关键指标"})
    if len(article_data["stats"]) > 1:
        wechat_stats.append({"num": article_data["stats"][1], "label": "重要数据"})

    return {
        "title": title,
        "subtitle": subtitle,
        "category": article_data["category"],
        "date": article_data["date"],
        "author": "AI创享派",
        "accent": "ikb",
        "images": images,  # 包含图片路径
        "wechat": {
            "headline": wechat_headline,
            "subline": subtitle[:40] if subtitle else title[:40],
            "stats": wechat_stats if wechat_stats else [
                {"num": "AI", "label": "前沿"}
            ]
        },
        "xhs": xhs_pages
    }


# ============================================================
# 4. HTML 生成：基于模板注入数据（优化版）
# ============================================================

def generate_html_v3(card_data: dict, style: str = "swiss", accent: str = "ikb") -> str:
    """生成社交卡片 HTML（V3 优化版）"""
    card_data["accent"] = accent

    template_file = TEMPLATES_DIR / f"social-card-{style}.html"
    if not template_file.exists():
        print(f"❌ 模板不存在: {template_file}")
        sys.exit(1)

    template = template_file.read_text(encoding='utf-8')

    # 替换模板中的占位符
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
      // 注入的实际数据（V3 优化版）
      var CARD_DATA = {json.dumps(card_data, ensure_ascii=False, indent=2)};
    </script>
    """
    html = html.replace('</head>', inject_script + '\n</head>')

    return html


# ============================================================
# 5. 文件保存
# ============================================================

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


# ============================================================
# 6. 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='社交卡片生成器 V3')
    parser.add_argument('article', help='Markdown 文章路径')
    parser.add_argument('--style', default='swiss', choices=['swiss', 'editorial'],
                       help='卡片样式 (默认: swiss)')
    parser.add_argument('--accent', default='ikb',
                       choices=['ikb', 'lemon-yellow', 'lemon-green', 'safety-orange'],
                       help='强调色 (默认: ikb)')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--json', action='store_true', help='只输出 JSON 数据，不生成 HTML')
    parser.add_argument('--max-pages', type=int, default=7, help='最大页面数 (默认: 7)')

    args = parser.parse_args()

    print(f"📄 正在处理文章: {args.article}")

    # 提取文章数据
    article_data = extract_article_data(args.article)
    print(f"📝 标题: {article_data['title']}")
    print(f"📊 提取到 {len(article_data['stats'])} 个数据点")
    print(f"📌 提取到 {len(article_data['points'])} 个要点")
    print(f"🖼️  提取到 {len(article_data['images'])} 张图片")
    print(f"📄 提取到 {len(article_data['paragraphs'])} 个段落")

    # 生成卡片数据
    card_data = generate_card_data_v3(article_data)
    print(f"🎨 生成 {len(card_data['xhs'])} 个小红书页面")

    # 输出页面计划
    print("\n📋 页面计划:")
    for i, page in enumerate(card_data['xhs']):
        image_info = " (有图片)" if page.get('image') else ""
        print(f"  {i+1}. {page['type']} ({page.get('layout', 'N/A')}){image_info}")

    if args.json:
        # 只输出 JSON
        print(json.dumps(card_data, ensure_ascii=False, indent=2))
    else:
        # 生成 HTML
        html = generate_html_v3(card_data, args.style, args.accent)
        out_path = save_html(html, args.article, args.output)
        print(f"\n✅ 完成！HTML 文件: {out_path}")
        print(f"📌 样式: {args.style}")
        print(f"🎨 强调色: {args.accent}")


if __name__ == "__main__":
    main()
