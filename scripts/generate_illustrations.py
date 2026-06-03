#!/usr/bin/env python3
"""
文章插图生成器
使用 guizang-social-card-skill 的模板生成文章配图
从文章中提取关键段落，生成可视化插图
"""

import sys
import io
import json
import re
from pathlib import Path
from datetime import datetime

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "images"


def extract_key_points(body_content: str, max_points: int = 3) -> list:
    """
    从文章中提取关键要点

    Args:
        body_content: 文章正文内容
        max_points: 最大要点数量

    Returns:
        要点列表，每个要点包含标题和内容
    """
    # 按段落分割
    paragraphs = body_content.split('\n\n')

    key_points = []

    # 寻找包含数据、观点或重要信息的段落
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para or len(para) < 50:
            continue

        # 检测是否包含数字/数据
        has_data = bool(re.search(r'\d+\.?\d*[%亿万千百]', para))

        # 检测是否包含观点（我觉得、我认为、说实话等）
        has_opinion = bool(re.search(r'我觉得|我认为|说实话|坦率的讲|说真的', para))

        # 检测是否包含重要信息（关键、核心、重要等）
        has_importance = bool(re.search(r'关键|核心|重要|最|第一|首先', para))

        # 检测是否包含对比/比较
        has_comparison = bool(re.search(r'对比|比较|超过|不如|胜过|低于', para))

        # 计算段落得分
        score = 0
        if has_data:
            score += 3
        if has_opinion:
            score += 2
        if has_importance:
            score += 2
        if has_comparison:
            score += 2
        if len(para) > 100:
            score += 1

        # 提取段落的核心内容
        # 去掉开头的引导词
        core_content = para
        core_content = re.sub(r'^(说到这个|回到xxx这块|顺着上面的再聊聊|说真的|坦率的讲|我有时候觉得|我一直觉得)', '', core_content)
        core_content = core_content.strip()

        # 截取前100个字符作为摘要
        if len(core_content) > 100:
            core_content = core_content[:97] + "..."

        key_points.append({
            "index": i,
            "content": core_content,
            "original": para,
            "score": score,
            "has_data": has_data,
            "has_opinion": has_opinion
        })

    # 按得分排序，取前 N 个
    key_points.sort(key=lambda x: x["score"], reverse=True)
    selected_points = key_points[:max_points]

    # 按文章顺序排序
    selected_points.sort(key=lambda x: x["index"])

    return selected_points


def generate_illustration_html(point: dict, point_index: int, total_points: int, accent: str = "ikb") -> str:
    """
    为单个要点生成插图 HTML

    Args:
        point: 要点字典
        point_index: 要点索引
        total_points: 总要点数
        accent: 强调色

    Returns:
        HTML 字符串
    """
    content = point["content"]

    # 根据内容类型选择布局
    if point["has_data"]:
        # 数据型内容，使用数据展示布局
        return generate_data_illustration(content, point_index, total_points, accent)
    elif point["has_opinion"]:
        # 观点型内容，使用引言布局
        return generate_quote_illustration(content, point_index, total_points, accent)
    else:
        # 普通内容，使用简洁布局
        return generate_simple_illustration(content, point_index, total_points, accent)


def generate_data_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成数据型插图（1920×1080 横版 - S09 KPI Tower 风格）"""
    # 提取数字
    numbers = re.findall(r'\d+\.?\d*[%亿万千百]?', content)
    main_number = numbers[0] if numbers else "N/A"

    # 提取更多数字用于 KPI 塔
    kpi_items = []
    for i, num in enumerate(numbers[:4]):
        # 提取数字旁边的标签
        pattern = re.escape(num) + r'[^，。]*?([^\d]{2,8})'
        match = re.search(pattern, content)
        label = match.group(1) if match else f"指标{i+1}"
        kpi_items.append({"num": num, "label": label.strip()})

    # 如果数字不足，补充默认项
    while len(kpi_items) < 4:
        kpi_items.append({"num": "—", "label": f"指标{len(kpi_items)+1}"})

    # 计算柱状图高度（基于数字大小）
    def calc_height(num_str):
        try:
            # 提取数字部分
            num = float(re.search(r'\d+\.?\d*', num_str).group())
            # 根据百分比计算高度
            if '%' in num_str:
                return min(num, 100)
            else:
                return min(num / 10, 100)
        except:
            return 50

    kpi_html = ""
    for i, item in enumerate(kpi_items):
        height = calc_height(item["num"])
        muted = "muted" if i == 3 else ""  # 最后一个作为基线对比
        kpi_html += f'''
        <div class="tower-col {muted}">
          <p class="num">{item["num"]}</p>
          <p class="lbl">{item["label"]}</p>
          <div class="bar-tower" style="--h:{height}%;"></div>
        </div>'''

    # 提取关键句子作为描述
    desc_match = re.search(r'[^。]{10,50}。', content)
    desc = desc_match.group(0) if desc_match else content[:50] + "..."

    return f'''<!doctype html>
<html lang="zh-CN" data-accent="{accent}">
<head>
  <meta charset="utf-8">
  <title>文章插图 {index + 1}/{total}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,
    [data-accent="ikb"] {{
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #002FA7;
      --accent-on: #ffffff;
    }}
    :root {{
      --sans: "Inter", "Noto Sans SC", sans-serif;
      --mono: "IBM Plex Mono", monospace;
    }}
    *,*::before,*::after {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      background: #1a1a1a;
      font-family: var(--sans);
      color: var(--ink);
      padding: 32px;
    }}
    .card {{
      width: 1920px;
      height: 1080px;
      position: relative;
      background: var(--paper);
      overflow: hidden;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
    }}
    .dot-mat {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      opacity: .08;
      background-image: radial-gradient(var(--ink) 1.5px, transparent 1.5px);
      background-size: 24px 24px;
    }}
    .left {{
      position: relative;
      z-index: 2;
      padding: 80px 60px 80px 80px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      border-right: 1px solid var(--grey-2);
    }}
    .right {{
      position: relative;
      z-index: 2;
      padding: 80px 80px 80px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .chrome-min {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--grey-2);
      margin-bottom: 32px;
    }}
    .t-cat {{
      font-family: var(--mono);
      font-weight: 600;
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 0;
    }}
    .t-meta {{
      font-family: var(--mono);
      font-weight: 500;
      font-size: 12px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }}
    .h-xl {{
      font-family: var(--sans-zh);
      font-weight: 300;
      font-size: 48px;
      line-height: 1.15;
      letter-spacing: -.01em;
      margin: 0 0 24px;
      color: var(--ink);
    }}
    .main-num {{
      font-family: var(--sans);
      font-weight: 200;
      font-size: 128px;
      line-height: 1;
      letter-spacing: -.02em;
      color: var(--accent);
      margin: 0 0 16px;
    }}
    .desc {{
      font-family: var(--sans-zh);
      font-weight: 400;
      font-size: 20px;
      line-height: 1.6;
      color: var(--ink);
      margin: 0;
    }}
    .kpi-tower-row {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 32px;
      align-items: end;
    }}
    .tower-col {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      align-items: flex-start;
    }}
    .tower-col .num {{
      font-family: var(--sans);
      font-weight: 200;
      font-size: 48px;
      line-height: 1;
      letter-spacing: -.02em;
      margin: 0;
      color: var(--ink);
    }}
    .tower-col .lbl {{
      font-family: var(--mono);
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }}
    .tower-col .bar-tower {{
      width: 100%;
      height: var(--h, 120px);
      background: var(--accent);
    }}
    .tower-col.muted .bar-tower {{
      background: var(--grey-2);
    }}
    .tower-col.muted .num {{
      color: var(--grey-3);
    }}
    .issue-strip {{
      position: absolute;
      bottom: 40px;
      left: 80px;
      right: 80px;
      display: flex;
      justify-content: space-between;
      font-family: var(--mono);
      font-size: 12px;
      color: var(--grey-3);
      border-top: 1px solid var(--grey-2);
      padding-top: 16px;
      z-index: 3;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="left">
      <div class="chrome-min">
        <span class="t-cat">Data · 核心数据</span>
        <span class="t-meta">{index + 1} / {total}</span>
      </div>
      <h2 class="h-xl">一组数字看懂</h2>
      <div class="main-num">{main_number}</div>
      <p class="desc">{desc}</p>
    </div>
    <div class="right">
      <div class="kpi-tower-row">
        {kpi_html}
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>2026.06</span>
    </div>
  </div>
</body>
</html>'''


def generate_quote_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成观点型插图（1920×1080 横版 - M04 Pull Quote 风格）"""
    # 将内容拆分为多个短句
    sentences = re.split(r'[。！？]', content)
    sentences = [s.strip() for s in sentences if s.strip()][:3]

    # 如果句子不足，补充
    while len(sentences) < 3:
        sentences.append("...")

    quotes_html = ""
    for sent in sentences:
        quotes_html += f'<p class="quote-item">{sent}</p>'

    return f'''<!doctype html>
<html lang="zh-CN" data-accent="{accent}">
<head>
  <meta charset="utf-8">
  <title>文章插图 {index + 1}/{total}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,
    [data-accent="ikb"] {{
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #002FA7;
      --accent-on: #ffffff;
    }}
    :root {{
      --sans: "Inter", "Noto Sans SC", sans-serif;
      --mono: "IBM Plex Mono", monospace;
    }}
    *,*::before,*::after {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      background: #1a1a1a;
      font-family: var(--sans);
      color: var(--ink);
      padding: 32px;
    }}
    .card {{
      width: 1920px;
      height: 1080px;
      position: relative;
      background: var(--paper);
      overflow: hidden;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
    }}
    .dot-mat {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      opacity: .08;
      background-image: radial-gradient(var(--ink) 1.5px, transparent 1.5px);
      background-size: 24px 24px;
    }}
    .left {{
      position: relative;
      z-index: 2;
      padding: 80px 60px 80px 80px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      background: var(--ink);
      color: var(--paper);
    }}
    .right {{
      position: relative;
      z-index: 2;
      padding: 80px 80px 80px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .chrome-min {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--grey-2);
      margin-bottom: 32px;
    }}
    .chrome-min-dark {{
      border-bottom-color: rgba(255,255,255,0.2);
    }}
    .t-cat {{
      font-family: var(--mono);
      font-weight: 600;
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 0;
    }}
    .t-meta {{
      font-family: var(--mono);
      font-weight: 500;
      font-size: 12px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }}
    .t-meta-light {{
      color: rgba(255,255,255,0.6);
    }}
    .quote-mark {{
      font-family: var(--sans);
      font-weight: 200;
      font-size: 96px;
      line-height: 1;
      color: var(--accent);
      opacity: 0.6;
      margin: 0 0 24px;
    }}
    .quote {{
      font-family: var(--sans-zh);
      font-weight: 400;
      font-size: 32px;
      line-height: 1.5;
      color: var(--ink);
      margin: 0;
      font-style: italic;
    }}
    .quote-light {{
      color: var(--paper);
    }}
    .source {{
      font-family: var(--mono);
      font-size: 14px;
      color: var(--grey-3);
      margin-top: 24px;
      letter-spacing: .08em;
    }}
    .quote-list {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .quote-item {{
      font-family: var(--sans-zh);
      font-weight: 400;
      font-size: 24px;
      line-height: 1.5;
      color: var(--ink);
      margin: 0;
      padding-left: 20px;
      border-left: 3px solid var(--accent);
    }}
    .issue-strip {{
      position: absolute;
      bottom: 40px;
      left: 80px;
      right: 80px;
      display: flex;
      justify-content: space-between;
      font-family: var(--mono);
      font-size: 12px;
      color: var(--grey-3);
      border-top: 1px solid var(--grey-2);
      padding-top: 16px;
      z-index: 3;
    }}
    .issue-strip-dark {{
      border-top-color: rgba(255,255,255,0.2);
      color: rgba(255,255,255,0.5);
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="left">
      <div class="chrome-min chrome-min-dark">
        <span class="t-cat">Insight · 观点</span>
        <span class="t-meta t-meta-light">{index + 1} / {total}</span>
      </div>
      <div class="quote-mark">"</div>
      <p class="quote quote-light">{sentences[0]}</p>
      <p class="source">— AI创享派</p>
      <div class="issue-strip issue-strip-dark">
        <span>AI创享派</span>
        <span>2026.06</span>
      </div>
    </div>
    <div class="right">
      <div class="chrome-min">
        <span class="t-cat">Key Points</span>
        <span class="t-meta">{index + 1} / {total}</span>
      </div>
      <div class="quote-list">
        {quotes_html}
      </div>
    </div>
  </div>
</body>
</html>'''


def generate_simple_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成简洁型插图（1920×1080 横版 - S07 Takeaway Ledger 风格）"""
    # 将内容拆分为要点
    points = content.split('。')
    points = [p.strip() for p in points if p.strip()][:3]

    # 如果要点不足，补充
    while len(points) < 3:
        points.append("...")

    # 提取关键标签
    tags = []
    tag_patterns = [
        r'(AI|人工智能|机器学习|深度学习|大模型|LLM|GPT|Claude|MiMo|DeepSeek)',
        r'(开源|闭源|API|模型|训练|推理|部署)',
        r'(降价|涨价|免费|付费|订阅|套餐)',
    ]
    for pattern in tag_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        tags.extend(matches[:2])

    tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags[:4]])

    points_html = ""
    for i, point in enumerate(points, 1):
        points_html += f'''
        <div class="ledger-row">
          <span class="ledger-nb">0{i}</span>
          <div class="ledger-content">
            <p class="ledger-title">{point}</p>
          </div>
        </div>'''

    return f'''<!doctype html>
<html lang="zh-CN" data-accent="{accent}">
<head>
  <meta charset="utf-8">
  <title>文章插图 {index + 1}/{total}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,
    [data-accent="ikb"] {{
      --paper: #fafaf8;
      --ink: #0a0a0a;
      --grey-1: #f0f0ee;
      --grey-2: #d4d4d2;
      --grey-3: #737373;
      --accent: #002FA7;
      --accent-on: #ffffff;
    }}
    :root {{
      --sans: "Inter", "Noto Sans SC", sans-serif;
      --mono: "IBM Plex Mono", monospace;
    }}
    *,*::before,*::after {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      background: #1a1a1a;
      font-family: var(--sans);
      color: var(--ink);
      padding: 32px;
    }}
    .card {{
      width: 1920px;
      height: 1080px;
      position: relative;
      background: var(--paper);
      overflow: hidden;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
    }}
    .dot-mat {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      opacity: .08;
      background-image: radial-gradient(var(--ink) 1.5px, transparent 1.5px);
      background-size: 24px 24px;
    }}
    .left {{
      position: relative;
      z-index: 2;
      padding: 80px 60px 80px 80px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      border-right: 1px solid var(--grey-2);
    }}
    .right {{
      position: relative;
      z-index: 2;
      padding: 80px 80px 80px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .chrome-min {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--grey-2);
      margin-bottom: 32px;
    }}
    .t-cat {{
      font-family: var(--mono);
      font-weight: 600;
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 0;
    }}
    .t-meta {{
      font-family: var(--mono);
      font-weight: 500;
      font-size: 12px;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--grey-3);
      margin: 0;
    }}
    .h-xl {{
      font-family: var(--sans-zh);
      font-weight: 300;
      font-size: 48px;
      line-height: 1.15;
      letter-spacing: -.01em;
      margin: 0 0 32px;
      color: var(--ink);
    }}
    .tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: auto;
    }}
    .tag {{
      font-family: var(--mono);
      font-size: 14px;
      padding: 8px 16px;
      border: 1px solid var(--ink);
      color: var(--ink);
    }}
    .ledger {{
      display: flex;
      flex-direction: column;
      gap: 0;
    }}
    .ledger-row {{
      display: grid;
      grid-template-columns: 60px 1fr;
      gap: 24px;
      align-items: baseline;
      padding: 24px 0;
      border-bottom: 1px solid var(--grey-2);
    }}
    .ledger-row:last-child {{
      border-bottom: 0;
    }}
    .ledger-nb {{
      font-family: var(--mono);
      font-size: 24px;
      color: var(--accent);
      letter-spacing: .08em;
    }}
    .ledger-content {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .ledger-title {{
      font-family: var(--sans-zh);
      font-weight: 500;
      font-size: 24px;
      letter-spacing: .02em;
      color: var(--ink);
      margin: 0;
      line-height: 1.4;
    }}
    .issue-strip {{
      position: absolute;
      bottom: 40px;
      left: 80px;
      right: 80px;
      display: flex;
      justify-content: space-between;
      font-family: var(--mono);
      font-size: 12px;
      color: var(--grey-3);
      border-top: 1px solid var(--grey-2);
      padding-top: 16px;
      z-index: 3;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="left">
      <div class="chrome-min">
        <span class="t-cat">Summary · 要点</span>
        <span class="t-meta">{index + 1} / {total}</span>
      </div>
      <h2 class="h-xl">三个关键要点</h2>
      <div class="tags">
        {tags_html}
      </div>
    </div>
    <div class="right">
      <div class="ledger">
        {points_html}
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>2026.06</span>
    </div>
  </div>
</body>
</html>'''


def render_illustration_to_png(html_file: Path, output_file: Path) -> bool:
    """
    将 HTML 渲染为 PNG

    Args:
        html_file: HTML 文件路径
        output_file: 输出 PNG 文件路径

    Returns:
        是否成功
    """
    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=2
            )
            page = context.new_page()

            # 加载 HTML
            page.goto(f"file:///{html_file.resolve().as_posix()}")
            page.wait_for_timeout(1500)  # 等待字体加载

            # 查找卡片元素
            card = page.query_selector('.card')
            if card:
                card.screenshot(path=str(output_file))
                page.close()
                context.close()
                browser.close()
                return True
            else:
                print(f"  ⚠️ 未找到卡片元素")
                page.close()
                context.close()
                browser.close()
                return False
    except Exception as e:
        print(f"  ❌ 渲染失败: {e}")
        return False


def generate_article_illustrations(article_file: str, max_illustrations: int = 3) -> list:
    """
    为文章生成插图

    Args:
        article_file: 文章文件路径
        max_illustrations: 最大插图数量

    Returns:
        生成的插图路径列表
    """
    article_path = Path(article_file)
    if not article_path.exists():
        print(f"❌ 文章文件不存在: {article_file}")
        return []

    # 读取文章内容
    content = article_path.read_text(encoding='utf-8')

    # 解析 frontmatter
    if content.startswith('---'):
        end_index = content.find('---', 3)
        if end_index > 0:
            body_content = content[end_index + 3:].strip()
        else:
            body_content = content
    else:
        body_content = content

    # 提取关键要点
    print("正在提取文章关键要点...")
    key_points = extract_key_points(body_content, max_illustrations)

    if not key_points:
        print("未找到关键要点")
        return []

    print(f"找到 {len(key_points)} 个关键要点")

    # 创建输出目录
    article_name = article_path.stem
    output_dir = OUTPUT_DIR / article_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成插图
    illustrations = []
    for i, point in enumerate(key_points):
        print(f"正在生成插图 {i + 1}/{len(key_points)}...")

        # 生成 HTML
        html_content = generate_illustration_html(point, i, len(key_points))
        html_file = output_dir / f"illustration_{i + 1}.html"
        html_file.write_text(html_content, encoding='utf-8')

        # 渲染为 PNG
        png_file = output_dir / f"illustration_{i + 1}.png"
        if render_illustration_to_png(html_file, png_file):
            illustrations.append({
                "path": png_file,
                "index": point["index"],
                "content": point["content"][:50] + "..."
            })
            print(f"  ✅ 已生成: {png_file.name}")
        else:
            print(f"  ❌ 生成失败")

    print(f"\n✨ 插图生成完成！共 {len(illustrations)} 张")
    print(f"📁 保存位置: {output_dir}")

    return illustrations


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_illustrations.py <文章文件路径> [最大插图数量]")
        print("示例: python generate_illustrations.py articles/2026-06-02_minimax-m3.md 3")
        sys.exit(1)

    article_file = sys.argv[1]
    max_illustrations = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    illustrations = generate_article_illustrations(article_file, max_illustrations)

    if illustrations:
        print("\n生成的插图:")
        for i, img in enumerate(illustrations, 1):
            print(f"  {i}. {img['path'].name}")
            print(f"     内容: {img['content']}")


if __name__ == "__main__":
    main()
