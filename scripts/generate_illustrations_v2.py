#!/usr/bin/env python3
"""
文章插图生成器 V2
使用 S 系列骨架，丰富内容展示
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

        # 检测是否包含技术术语
        has_tech = bool(re.search(r'模型|算法|架构|API|Token|上下文|注意力|稀疏', para))

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
        if has_tech:
            score += 1
        if len(para) > 100:
            score += 1

        # 提取段落的核心内容
        core_content = para
        core_content = re.sub(r'^(说到这个|回到xxx这块|顺着上面的再聊聊|说真的|坦率的讲|我有时候觉得|我一直觉得)', '', core_content)
        core_content = core_content.strip()

        # 截取前150个字符作为摘要
        if len(core_content) > 150:
            core_content = core_content[:147] + "..."

        key_points.append({
            "index": i,
            "content": core_content,
            "original": para,
            "score": score,
            "has_data": has_data,
            "has_opinion": has_opinion,
            "has_tech": has_tech
        })

    # 按得分排序，取前 N 个
    key_points.sort(key=lambda x: x["score"], reverse=True)
    selected_points = key_points[:max_points]

    # 按文章顺序排序
    selected_points.sort(key=lambda x: x["index"])

    return selected_points


def generate_comparison_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成对比型插图（S02 Two Signals 风格）"""
    # 提取对比内容
    # 尝试找到两个对比对象
    comparison_patterns = [
        r'([^，。]+)[和与]([^，。]+)的[对比比较]',
        r'([^，。]+)[vs对比]([^，。]+)',
        r'([^，。]+)超过[了]?([^，。]+)',
        r'([^，。]+)不如([^，。]+)',
    ]

    left_name = "MiMo M3"
    right_name = "Opus 4.7"
    left_points = ["开源", "100万 Token", "$0.12/M"]
    right_points = ["闭源", "20万 Token", "$15/M"]

    for pattern in comparison_patterns:
        match = re.search(pattern, content)
        if match:
            left_name = match.group(1).strip()[:10]
            right_name = match.group(2).strip()[:10]
            break

    # 提取特性列表
    features = re.findall(r'[✓✔☑]([^✓✔☑，。]{2,15})', content)
    if len(features) >= 4:
        left_points = features[:2]
        right_points = features[2:4]

    left_html = "".join([f'<span class="point">✓ {p}</span>' for p in left_points])
    right_html = "".join([f'<span class="point">✓ {p}</span>' for p in right_points])

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
    :root,[data-accent="ikb"]{{
      --paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;
      --accent:#002FA7;--accent-on:#ffffff;
    }}
    :root{{
      --sans:"Inter","Noto Sans SC",sans-serif;
      --mono:"IBM Plex Mono",monospace;
    }}
    *,*::before,*::after{{box-sizing:border-box}}
    html,body{{margin:0;padding:0}}
    body{{background:#1a1a1a;font-family:var(--sans);color:var(--ink);padding:32px}}
    .card{{
      width:1920px;height:1080px;position:relative;background:var(--paper);overflow:hidden;
      padding:60px 80px;display:flex;flex-direction:column;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .header{{
      display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:56px;margin:0;color:var(--ink);
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);
    }}
    .compare{{
      display:grid;grid-template-columns:1fr 1fr;gap:40px;flex:1;
    }}
    .signal{{
      padding:40px;display:flex;flex-direction:column;
    }}
    .signal-a{{
      background:var(--ink);color:var(--paper);
    }}
    .signal-b{{
      background:var(--grey-1);border:2px solid var(--ink);
    }}
    .signal-label{{
      font-family:var(--mono);font-size:16px;letter-spacing:.12em;text-transform:uppercase;
      margin:0 0 24px;
    }}
    .signal-a .signal-label{{color:var(--accent)}}
    .signal-b .signal-label{{color:var(--grey-3)}}
    .signal-title{{
      font-family:var(--sans-zh);font-weight:600;font-size:48px;margin:0 0 24px;
    }}
    .signal-points{{
      display:flex;flex-direction:column;gap:16px;margin-top:auto;
    }}
    .point{{
      font-family:var(--sans-zh);font-size:20px;
    }}
    .issue-strip{{
      position:absolute;bottom:40px;left:80px;right:80px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:16px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="header">
      <h1 class="h-xl">对比分析</h1>
      <span class="t-cat">Comparison</span>
    </div>
    <div class="compare">
      <div class="signal signal-a">
        <p class="signal-label">{left_name}</p>
        <h3 class="signal-title">优势</h3>
        <div class="signal-points">{left_html}</div>
      </div>
      <div class="signal signal-b">
        <p class="signal-label">{right_name}</p>
        <h3 class="signal-title">特点</h3>
        <div class="signal-points">{right_html}</div>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_matrix_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成矩阵型插图（S12 Matrix + Hero Stat 风格）"""
    # 提取关键能力/特性
    capabilities = []
    cap_patterns = [
        r'(编程|代码|编码)',
        r'(推理|思考|分析)',
        r'(多模态|图像|视频)',
        r'(Agent|智能体|代理)',
        r'(上下文|长文本|Context)',
        r'(工具|API|调用)',
        r'(优化|加速|性能)',
        r'(开源|开放|免费)',
    ]

    for pattern in cap_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            capabilities.append(matches[0])

    # 如果不足8个，补充
    while len(capabilities) < 8:
        capabilities.append(f"能力{len(capabilities)+1}")

    # 取前8个
    capabilities = capabilities[:8]

    # 生成矩阵格子
    cells_html = ""
    for i, cap in enumerate(capabilities, 1):
        is_accent = "is-accent" if i == 2 else ""  # 第二个作为重点
        cells_html += f'''
        <div class="cell {is_accent}">
          <span class="cell-nb">0{i}</span>
          <span class="cell-title">{cap}</span>
        </div>'''

    # 提取主要数字
    numbers = re.findall(r'\d+\.?\d*[%亿万千百]?', content)
    main_num = numbers[0] if numbers else "8"

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
    :root,[data-accent="ikb"]{{
      --paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;
      --accent:#002FA7;--accent-on:#ffffff;
    }}
    :root{{
      --sans:"Inter","Noto Sans SC",sans-serif;
      --mono:"IBM Plex Mono",monospace;
    }}
    *,*::before,*::after{{box-sizing:border-box}}
    html,body{{margin:0;padding:0}}
    body{{background:#1a1a1a;font-family:var(--sans);color:var(--ink);padding:32px}}
    .card{{
      width:1920px;height:1080px;position:relative;background:var(--paper);overflow:hidden;
      padding:60px 80px;display:flex;flex-direction:column;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .header{{
      display:flex;justify-content:space-between;align-items:baseline;margin-bottom:32px;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:48px;margin:0;color:var(--ink);
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);
    }}
    .matrix{{
      display:grid;grid-template-columns:repeat(4,1fr);gap:16px;flex:1;margin-bottom:32px;
    }}
    .cell{{
      background:var(--grey-1);padding:24px;display:flex;flex-direction:column;gap:8px;
    }}
    .cell-nb{{
      font-family:var(--mono);font-size:16px;color:var(--grey-3);
    }}
    .cell-title{{
      font-family:var(--sans-zh);font-weight:500;font-size:22px;color:var(--ink);
    }}
    .cell.is-accent{{
      background:var(--accent);color:var(--accent-on);
    }}
    .cell.is-accent .cell-nb,.cell.is-accent .cell-title{{
      color:var(--accent-on);
    }}
    .hero-stat{{
      display:flex;justify-content:space-between;align-items:end;
      padding-top:32px;border-top:1px solid var(--grey-2);
    }}
    .hero-kick{{
      font-family:var(--mono);font-size:16px;color:var(--grey-3);margin:0 0 8px;
    }}
    .hero-text{{
      font-family:var(--sans-zh);font-size:24px;color:var(--ink);margin:0;
    }}
    .hero-num{{
      font-family:var(--sans);font-weight:200;font-size:168px;line-height:1;color:var(--accent);
    }}
    .issue-strip{{
      position:absolute;bottom:40px;left:80px;right:80px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:16px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="header">
      <h1 class="h-xl">能力矩阵</h1>
      <span class="t-cat">Matrix</span>
    </div>
    <div class="matrix">
      {cells_html}
    </div>
    <div class="hero-stat">
      <div>
        <p class="hero-kick">Total Coverage</p>
        <p class="hero-text">覆盖核心能力领域</p>
      </div>
      <span class="hero-num">{main_num}</span>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_architecture_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成架构型插图（S06 Pipeline 风格）"""
    # 提取架构组件
    components = []
    comp_patterns = [
        r'(输入|输入层|接收)',
        r'(处理|处理层|分析)',
        r'(输出|输出层|生成)',
        r'(存储|存储层|保存)',
        r'(训练|训练层|学习)',
        r'(推理|推理层|预测)',
    ]

    for pattern in comp_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            components.append(matches[0])

    # 如果不足3个，补充
    while len(components) < 3:
        components.append(f"组件{len(components)+1}")

    # 取前3个
    components = components[:3]

    # 生成架构模块
    stages_html = ""
    for i, comp in enumerate(components, 1):
        stages_html += f'''
        <div class="stage">
          <p class="stage-nb">0{i}</p>
          <h3 class="stage-title">{comp}</h3>
          <p class="stage-desc">核心功能模块</p>
          <p class="stage-action">处理中...</p>
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
    :root,[data-accent="ikb"]{{
      --paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;
      --accent:#002FA7;--accent-on:#ffffff;
    }}
    :root{{
      --sans:"Inter","Noto Sans SC",sans-serif;
      --mono:"IBM Plex Mono",monospace;
    }}
    *,*::before,*::after{{box-sizing:border-box}}
    html,body{{margin:0;padding:0}}
    body{{background:#1a1a1a;font-family:var(--sans);color:var(--ink);padding:32px}}
    .card{{
      width:1920px;height:1080px;position:relative;background:var(--paper);overflow:hidden;
      padding:60px 80px;display:flex;flex-direction:column;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .header{{
      display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:56px;margin:0;color:var(--ink);
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);
    }}
    .pipeline{{
      display:grid;grid-template-columns:repeat(3,1fr);gap:24px;flex:1;
    }}
    .stage{{
      background:var(--grey-1);padding:32px;display:flex;flex-direction:column;
    }}
    .stage-nb{{
      font-family:var(--mono);font-size:24px;color:var(--accent);margin:0 0 16px;
    }}
    .stage-title{{
      font-family:var(--sans-zh);font-weight:600;font-size:28px;color:var(--ink);margin:0 0 12px;
    }}
    .stage-desc{{
      font-family:var(--sans-zh);font-size:18px;color:var(--grey-3);margin:0 0 24px;
    }}
    .stage-action{{
      font-family:var(--mono);font-size:16px;color:var(--accent);margin-top:auto;
      padding-top:16px;border-top:1px solid var(--grey-2);
    }}
    .issue-strip{{
      position:absolute;bottom:40px;left:80px;right:80px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:16px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="header">
      <h1 class="h-xl">系统架构</h1>
      <span class="t-cat">Architecture</span>
    </div>
    <div class="pipeline">
      {stages_html}
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_code_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成代码型插图（S04 Interface 风格）"""
    # 提取代码相关内容
    code_lines = [
        "# 安装 MiniMax M3",
        "pip install minimax-m3",
        "",
        "# 导入库",
        "from minimax import M3",
        "",
        "# 加载模型",
        "model = M3.from_pretrained('m3-base')",
        "",
        "# 生成代码",
        "result = model.generate(",
        "    'Write a Python function'",
        ")",
    ]

    # 尝试从内容中提取代码片段
    code_match = re.search(r'```python(.*?)```', content, re.DOTALL)
    if code_match:
        code_text = code_match.group(1).strip()
        code_lines = code_text.split('\n')[:12]

    code_html = ""
    for line in code_lines:
        # 高亮注释
        if line.strip().startswith('#'):
            code_html += f'<div class="code-line comment">{line}</div>'
        # 高亮关键字
        elif any(kw in line for kw in ['import', 'from', 'def', 'class', 'return']):
            code_html += f'<div class="code-line keyword">{line}</div>'
        else:
            code_html += f'<div class="code-line">{line}</div>'

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
    :root,[data-accent="ikb"]{{
      --paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;
      --accent:#002FA7;--accent-on:#ffffff;
    }}
    :root{{
      --sans:"Inter","Noto Sans SC",sans-serif;
      --mono:"IBM Plex Mono",monospace;
    }}
    *,*::before,*::after{{box-sizing:border-box}}
    html,body{{margin:0;padding:0}}
    body{{background:#1a1a1a;font-family:var(--sans);color:var(--ink);padding:32px}}
    .card{{
      width:1920px;height:1080px;position:relative;background:var(--paper);overflow:hidden;
      display:grid;grid-template-columns:1fr 1fr;gap:0;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .left{{
      position:relative;z-index:2;padding:80px 60px 80px 80px;
      display:flex;flex-direction:column;justify-content:center;
      border-right:1px solid var(--grey-2);
    }}
    .right{{
      position:relative;z-index:2;padding:80px 80px 80px 60px;
      display:flex;flex-direction:column;justify-content:center;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:16px;border-bottom:1px solid var(--grey-2);margin-bottom:32px;
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);margin:0;
    }}
    .t-meta{{
      font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.14em;
      text-transform:uppercase;color:var(--grey-3);margin:0;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:48px;line-height:1.15;
      letter-spacing:-.01em;margin:0 0 24px;color:var(--ink);
    }}
    .desc{{
      font-family:var(--sans-zh);font-weight:400;font-size:20px;line-height:1.6;
      color:var(--ink);margin:0;
    }}
    .browser{{
      background:var(--paper);border:1px solid var(--grey-2);border-radius:8px;
      overflow:hidden;flex:1;
    }}
    .browser-bar{{
      height:40px;background:var(--grey-1);border-bottom:1px solid var(--grey-2);
      display:flex;align-items:center;padding:0 16px;gap:8px;
    }}
    .dot{{width:12px;height:12px;border-radius:50%}}
    .dot-r{{background:#f08080}}
    .dot-y{{background:#f5c450}}
    .dot-g{{background:#7ec98f}}
    .browser-url{{
      margin-left:16px;font-family:var(--mono);font-size:14px;color:var(--grey-3);
    }}
    .browser-content{{
      padding:24px;display:flex;flex-direction:column;gap:4px;
    }}
    .code-line{{
      font-family:var(--mono);font-size:16px;color:var(--ink);
      background:var(--grey-1);padding:8px 12px;
    }}
    .code-line.comment{{
      color:var(--grey-3);
    }}
    .code-line.keyword{{
      color:var(--accent);
    }}
    .issue-strip{{
      position:absolute;bottom:40px;left:80px;right:80px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:16px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="left">
      <div class="chrome-min">
        <span class="t-cat">Code · 代码示例</span>
        <span class="t-meta">{index + 1} / {total}</span>
      </div>
      <h2 class="h-xl">快速开始</h2>
      <p class="desc">几行代码即可体验 M3 的强大能力</p>
    </div>
    <div class="right">
      <div class="browser">
        <div class="browser-bar">
          <span class="dot dot-r"></span>
          <span class="dot dot-y"></span>
          <span class="dot dot-g"></span>
          <span class="browser-url">example.py</span>
        </div>
        <div class="browser-content">
          {code_html}
        </div>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_ledger_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成账目型插图（S11 Stacked Ledger 风格）"""
    # 提取要点
    points = content.split('。')
    points = [p.strip() for p in points if p.strip() and len(p.strip()) > 10][:4]

    # 如果不足4个，补充
    while len(points) < 4:
        points.append(f"要点{len(points)+1}")

    # 提取数字
    numbers = re.findall(r'\d+\.?\d*[%亿万千百]?', content)
    if len(numbers) < 4:
        numbers.extend(["—"] * (4 - len(numbers)))

    # 生成账目行
    ledger_html = ""
    for i, (num, point) in enumerate(zip(numbers[:4], points[:4]), 1):
        # 截断过长的文本
        if len(point) > 20:
            point = point[:17] + "..."

        # 选择图标
        icons = [
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 18l6-6-6-6"/><path d="M8 6l-6 6 6 6"/></svg>',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M8 10h8"/></svg>',
        ]
        icon = icons[i-1] if i <= len(icons) else icons[0]

        ledger_html += f'''
        <div class="ledger-row">
          <span class="ledger-num">{num}</span>
          <span class="ledger-text">{point}</span>
          <svg class="ledger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{icon}</svg>
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
    :root,[data-accent="ikb"]{{
      --paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;
      --accent:#002FA7;--accent-on:#ffffff;
    }}
    :root{{
      --sans:"Inter","Noto Sans SC",sans-serif;
      --mono:"IBM Plex Mono",monospace;
    }}
    *,*::before,*::after{{box-sizing:border-box}}
    html,body{{margin:0;padding:0}}
    body{{background:#1a1a1a;font-family:var(--sans);color:var(--ink);padding:32px}}
    .card{{
      width:1920px;height:1080px;position:relative;background:var(--ink);overflow:hidden;
      padding:80px 120px;display:flex;flex-direction:column;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,.2);margin-bottom:48px;
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:16px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);margin:0;
    }}
    .t-meta{{
      font-family:var(--mono);font-weight:500;font-size:14px;letter-spacing:.14em;
      text-transform:uppercase;color:rgba(255,255,255,.5);margin:0;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:200;font-size:72px;line-height:1.1;
      margin:0 0 48px;color:var(--paper);
    }}
    .ledger{{
      display:flex;flex-direction:column;gap:0;flex:1;
    }}
    .ledger-row{{
      display:grid;grid-template-columns:120px 1fr 80px;gap:32px;align-items:center;
      padding:28px 0;border-bottom:1px solid rgba(255,255,255,.2);
    }}
    .ledger-row:last-child{{border-bottom:0}}
    .ledger-num{{
      font-family:var(--sans);font-weight:200;font-size:72px;line-height:1;color:var(--ink);
    }}
    .ledger-text{{
      font-family:var(--sans-zh);font-size:28px;color:var(--paper);
    }}
    .ledger-icon{{
      width:56px;height:56px;color:var(--accent);
    }}
    .issue-strip{{
      position:absolute;bottom:80px;left:120px;right:120px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:rgba(255,255,255,.4);
      border-top:1px solid rgba(255,255,255,.2);padding-top:20px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="chrome-min">
      <span class="t-cat">Summary · 总结</span>
      <span class="t-meta">{index + 1} / {total}</span>
    </div>
    <h1 class="h-xl">关键要点</h1>
    <div class="ledger">
      {ledger_html}
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_bar_chart_illustration(content: str, index: int, total: int, accent: str) -> str:
    """生成条形图插图（S10 H-Bar Chart 风格）"""
    # 提取排名数据
    items = []

    # 尝试找到排名列表
    rank_patterns = [
        r'(\d+)[\.、]([^，。]{2,10})[：:](\d+\.?\d*[%亿万千百]?)',
        r'([^，。]{2,10})[是为](\d+\.?\d*[%亿万千百]?)',
    ]

    for pattern in rank_patterns:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches[:5]:
                if len(match) == 3:
                    items.append({"name": match[1].strip(), "value": match[2]})
                else:
                    items.append({"name": match[0].strip(), "value": match[1]})
            break

    # 如果没有找到，使用默认数据
    if not items:
        items = [
            {"name": "Opus 4.7", "value": "62.1%"},
            {"name": "MiMo M3", "value": "59.0%"},
            {"name": "GPT-5.5", "value": "58.2%"},
            {"name": "Gemini 3.1", "value": "56.8%"},
            {"name": "DeepSeek V4", "value": "53.4%"},
        ]

    # 计算条形宽度（百分比）
    def calc_width(val_str):
        try:
            num = float(re.search(r'\d+\.?\d*', val_str).group())
            if '%' in val_str:
                return min(num, 100)
            else:
                return min(num / 10, 100)
        except:
            return 50

    # 生成条形行
    bars_html = ""
    for item in items[:5]:
        width = calc_width(item["value"])
        bars_html += f'''
        <div class="bar-row">
          <span class="bar-label">{item["name"]}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div>
          <span class="bar-val">{item["value"]}</span>
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
    :root,[data-accent="ikb"]{{
      --paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;
      --accent:#002FA7;--accent-on:#ffffff;
    }}
    :root{{
      --sans:"Inter","Noto Sans SC",sans-serif;
      --mono:"IBM Plex Mono",monospace;
    }}
    *,*::before,*::after{{box-sizing:border-box}}
    html,body{{margin:0;padding:0}}
    body{{background:#1a1a1a;font-family:var(--sans);color:var(--ink);padding:32px}}
    .card{{
      width:1920px;height:1080px;position:relative;background:var(--paper);overflow:hidden;
      padding:60px 80px;display:flex;flex-direction:column;
    }}
    .header{{
      display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:56px;margin:0;color:var(--ink);
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:14px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);
    }}
    .chart{{
      display:flex;flex-direction:column;gap:24px;flex:1;
    }}
    .bar-row{{
      display:grid;grid-template-columns:200px 1fr 100px;gap:24px;align-items:center;
    }}
    .bar-label{{
      font-family:var(--sans-zh);font-weight:500;font-size:22px;color:var(--ink);
    }}
    .bar-track{{
      height:32px;background:var(--grey-1);position:relative;
    }}
    .bar-fill{{
      position:absolute;left:0;top:0;bottom:0;background:var(--accent);
    }}
    .bar-val{{
      font-family:var(--mono);font-size:22px;text-align:right;color:var(--ink);
    }}
    .issue-strip{{
      position:absolute;bottom:40px;left:80px;right:80px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:16px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">排名对比</h1>
      <span class="t-cat">Ranking</span>
    </div>
    <div class="chart">
      {bars_html}
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


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
        # 数据型内容，使用条形图布局
        return generate_bar_chart_illustration(content, point_index, total_points, accent)
    elif point["has_tech"]:
        # 技术型内容，使用架构图布局
        return generate_architecture_illustration(content, point_index, total_points, accent)
    elif point["has_opinion"]:
        # 观点型内容，使用对比布局
        return generate_comparison_illustration(content, point_index, total_points, accent)
    else:
        # 普通内容，使用账目型布局
        return generate_ledger_illustration(content, point_index, total_points, accent)


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
        print("用法: python generate_illustrations_v2.py <文章文件路径> [最大插图数量]")
        print("示例: python generate_illustrations_v2.py articles/2026-06-02_minimax-m3.md 3")
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
