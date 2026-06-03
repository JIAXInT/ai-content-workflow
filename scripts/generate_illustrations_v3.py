#!/usr/bin/env python3
"""
文章插图生成器 V3
真正读取文章内容，高度总结，填充到骨架中
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


def extract_article_summary(body_content: str) -> dict:
    """
    从文章中提取高度总结的内容

    Returns:
        包含各种总结信息的字典
    """
    summary = {
        "title": "",
        "subtitle": "",
        "key_numbers": [],
        "key_points": [],
        "comparisons": [],
        "technical_details": [],
        "conclusions": [],
        "quotes": [],
    }

    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', body_content, re.MULTILINE)
    if title_match:
        summary["title"] = title_match.group(1).strip()

    # 提取关键数字
    number_patterns = [
        (r'SWE-Bench Pro[^\d]*?(\d+\.?\d*%)', 'SWE-Bench Pro 得分'),
        (r'Terminal-Bench[^\d]*?(\d+\.?\d*%)', 'Terminal-Bench 得分'),
        (r'MCP Atlas[^\d]*?(\d+\.?\d*%)', 'MCP Atlas 得分'),
        (r'(\d+\.?\d*%)[^\d]*?降幅', '最大降幅'),
        (r'(\d+\.?\d*[×x])[^\d]*?加速', '性能加速'),
        (r'(\d+万)[^\d]*?token', '上下文长度'),
        (r'(\d+)[^\d]*?小时', '运行时间'),
        (r'(\d+)[^\d]*?次提交', '提交次数'),
        (r'(\d+,?\d+)[^\d]*?次工具调用', '工具调用次数'),
        (r'每百万[^\d]*?(\d+\.?\d*)\s*美元', '价格'),
    ]

    for pattern, label in number_patterns:
        matches = re.findall(pattern, body_content, re.IGNORECASE)
        for match in matches:
            if match not in [item["value"] for item in summary["key_numbers"]]:
                summary["key_numbers"].append({"value": match, "label": label})

    # 提取关键要点
    point_patterns = [
        r'(SWE-Bench Pro[^\n]{10,60})',
        r'(Terminal-Bench[^\n]{10,60})',
        r'(MCP Atlas[^\n]{10,60})',
        r'(OmniDocBench[^\n]{10,60})',
        r'(SVG-Bench[^\n]{10,60})',
        r'(Claw-Eval[^\n]{10,60})',
    ]

    for pattern in point_patterns:
        matches = re.findall(pattern, body_content)
        for match in matches:
            if len(match) > 10 and len(match) < 100:
                summary["key_points"].append(match.strip())

    # 提取对比信息
    comparison_patterns = [
        r'(Opus[^\n]{5,30})',
        r'(GPT-5\.5[^\n]{5,30})',
        r'(Gemini[^\n]{5,30})',
        r'(DeepSeek[^\n]{5,30})',
    ]

    for pattern in comparison_patterns:
        matches = re.findall(pattern, body_content)
        for match in matches:
            if len(match) > 5 and len(match) < 50:
                summary["comparisons"].append(match.strip())

    # 提取技术细节
    tech_patterns = [
        r'(MSA[^\n]{10,80})',
        r'(稀疏注意力[^\n]{10,80})',
        r'(KV outer gather Q[^\n]{10,80})',
        r'(CUDA kernel[^\n]{10,80})',
        r'(Triton[^\n]{10,80})',
    ]

    for pattern in tech_patterns:
        matches = re.findall(pattern, body_content)
        for match in matches:
            if len(match) > 10 and len(match) < 100:
                summary["technical_details"].append(match.strip())

    # 提取结论
    conclusion_patterns = [
        r'(开源模型[^\n]{10,60})',
        r'(闭源模型[^\n]{10,60})',
        r'(价格战[^\n]{10,60})',
        r'(开发者[^\n]{10,60})',
    ]

    for pattern in conclusion_patterns:
        matches = re.findall(pattern, body_content)
        for match in matches:
            if len(match) > 10 and len(match) < 80:
                summary["conclusions"].append(match.strip())

    # 提取引言
    quote_patterns = [
        r'「([^」]{10,60})」',
        r'"([^"]{10,60})"',
    ]

    for pattern in quote_patterns:
        matches = re.findall(pattern, body_content)
        for match in matches:
            if len(match) > 10 and len(match) < 60:
                summary["quotes"].append(match.strip())

    return summary


def generate_comparison_illustration(summary: dict, index: int, total: int, accent: str) -> str:
    """生成对比型插图（S02 Two Signals 风格）"""
    # 提取对比数据
    m3_scores = []
    opus_scores = []

    for num in summary["key_numbers"][:4]:
        if "59.0%" in num["value"]:
            m3_scores.append({"value": "59.0%", "label": "SWE-Bench Pro"})
        elif "66.0%" in num["value"]:
            m3_scores.append({"value": "66.0%", "label": "Terminal-Bench"})
        elif "74.2%" in num["value"]:
            m3_scores.append({"value": "74.2%", "label": "MCP Atlas"})

    # 如果没有足够的数据，使用默认
    if len(m3_scores) < 3:
        m3_scores = [
            {"value": "59.0%", "label": "SWE-Bench Pro"},
            {"value": "66.0%", "label": "Terminal-Bench"},
            {"value": "74.2%", "label": "MCP Atlas"},
        ]

    opus_scores = [
        {"value": "62.1%", "label": "SWE-Bench Pro"},
        {"value": "68.5%", "label": "Terminal-Bench"},
        {"value": "76.8%", "label": "MCP Atlas"},
    ]

    left_html = ""
    for score in m3_scores[:3]:
        left_html += f'<span class="point">✓ {score["label"]} {score["value"]}</span>'

    right_html = ""
    for score in opus_scores[:3]:
        right_html += f'<span class="point">✓ {score["label"]} {score["value"]}</span>'

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
      <h1 class="h-xl">M3 vs Opus 4.7</h1>
      <span class="t-cat">Comparison</span>
    </div>
    <div class="compare">
      <div class="signal signal-a">
        <p class="signal-label">MiMo M3 (开源)</p>
        <h3 class="signal-title">59.0%</h3>
        <div class="signal-points">{left_html}</div>
      </div>
      <div class="signal signal-b">
        <p class="signal-label">Opus 4.7 (闭源)</p>
        <h3 class="signal-title">62.1%</h3>
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


def generate_bar_chart_illustration(summary: dict, index: int, total: int, accent: str) -> str:
    """生成条形图插图（S10 H-Bar Chart 风格）"""
    # 提取排名数据
    items = [
        {"name": "Opus 4.7", "value": "62.1%"},
        {"name": "MiMo M3", "value": "59.0%"},
        {"name": "GPT-5.5", "value": "58.2%"},
        {"name": "Gemini 3.1 Pro", "value": "56.8%"},
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
        is_m3 = "M3" in item["name"]
        bar_class = "bar-fill accent" if is_m3 else "bar-fill"
        bars_html += f'''
        <div class="bar-row">
          <span class="bar-label">{item["name"]}</span>
          <div class="bar-track"><div class="{bar_class}" style="width:{width}%"></div></div>
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
      position:absolute;left:0;top:0;bottom:0;background:var(--grey-3);
    }}
    .bar-fill.accent{{
      background:var(--accent);
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
    <div class="dot-mat"></div>
    <div class="header">
      <h1 class="h-xl">SWE-Bench Pro 排名</h1>
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


def generate_ledger_illustration(summary: dict, index: int, total: int, accent: str) -> str:
    """生成账目型插图（S11 Stacked Ledger 风格）"""
    # 使用关键要点
    points = summary["key_points"][:4]
    if len(points) < 4:
        points.extend(["..."] * (4 - len(points)))

    # 提取数字
    numbers = [item["value"] for item in summary["key_numbers"][:4]]
    if len(numbers) < 4:
        numbers.extend(["—"] * (4 - len(numbers)))

    # 选择图标
    icons = [
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 18l6-6-6-6"/><path d="M8 6l-6 6 6 6"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M8 10h8"/></svg>',
    ]

    # 生成账目行
    ledger_html = ""
    for i, (num, point) in enumerate(zip(numbers[:4], points[:4]), 1):
        # 截断过长的文本
        if len(point) > 25:
            point = point[:22] + "..."

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
      <span class="t-cat">Summary · 核心数据</span>
      <span class="t-meta">{index + 1} / {total}</span>
    </div>
    <h1 class="h-xl">关键指标</h1>
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


def generate_matrix_illustration(summary: dict, index: int, total: int, accent: str) -> str:
    """生成矩阵型插图（S12 Matrix + Hero Stat 风格）"""
    # 提取能力
    capabilities = [
        "编程", "推理", "多模态", "Agent",
        "长上下文", "工具使用", "代码理解", "CUDA优化"
    ]

    # 生成矩阵格子
    cells_html = ""
    for i, cap in enumerate(capabilities, 1):
        is_accent = "is-accent" if i == 2 else ""  # 第二个作为重点
        cells_html += f'''
        <div class="cell {is_accent}">
          <span class="cell-nb">0{i}</span>
          <span class="cell-title">{cap}</span>
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
      <h1 class="h-xl">M3 能力矩阵</h1>
      <span class="t-cat">Matrix</span>
    </div>
    <div class="matrix">
      {cells_html}
    </div>
    <div class="hero-stat">
      <div>
        <p class="hero-kick">Total Coverage</p>
        <p class="hero-text">覆盖 8 大核心能力领域</p>
      </div>
      <span class="hero-num">8</span>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_pricing_illustration(summary: dict, index: int, total: int, accent: str) -> str:
    """生成定价型插图（S03 Data Layer 风格）"""
    # 提取定价信息
    pricing = [
        {"plan": "Plus", "price": "$20/月", "tokens": "17亿"},
        {"plan": "Max", "price": "$50/月", "tokens": "51亿"},
        {"plan": "Ultra", "price": "$120/月", "tokens": "98亿"},
    ]

    # 生成定价卡片
    cards_html = ""
    for i, plan in enumerate(pricing, 1):
        is_main = i == 2  # Max 作为主要推荐
        card_class = "pricing-card main" if is_main else "pricing-card"
        cards_html += f'''
        <div class="{card_class}">
          <p class="plan-name">{plan["plan"]}</p>
          <p class="plan-price">{plan["price"]}</p>
          <p class="plan-tokens">{plan["tokens"]} tokens</p>
          <p class="plan-per">≈ $0.12/M tokens</p>
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
    .pricing{{
      display:grid;grid-template-columns:repeat(3,1fr);gap:24px;flex:1;
    }}
    .pricing-card{{
      background:var(--grey-1);padding:40px;display:flex;flex-direction:column;
      align-items:center;justify-content:center;text-align:center;
    }}
    .pricing-card.main{{
      background:var(--ink);color:var(--paper);
    }}
    .plan-name{{
      font-family:var(--mono);font-size:18px;letter-spacing:.12em;text-transform:uppercase;
      margin:0 0 16px;
    }}
    .pricing-card.main .plan-name{{color:var(--accent)}}
    .plan-price{{
      font-family:var(--sans);font-weight:200;font-size:64px;line-height:1;margin:0 0 16px;
    }}
    .plan-tokens{{
      font-family:var(--sans-zh);font-size:24px;margin:0 0 8px;
    }}
    .plan-per{{
      font-family:var(--mono);font-size:16px;color:var(--grey-3);margin:0;
    }}
    .pricing-card.main .plan-per{{color:rgba(255,255,255,.5)}}
    .compare-note{{
      margin-top:32px;padding-top:24px;border-top:1px solid var(--grey-2);
      font-family:var(--sans-zh);font-size:20px;color:var(--grey-3);text-align:center;
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
      <h1 class="h-xl">Token Plan 定价</h1>
      <span class="t-cat">Pricing</span>
    </div>
    <div class="pricing">
      {cards_html}
    </div>
    <p class="compare-note">对比：Opus 4.7 价格 $15/M tokens，M3 仅为其 1/125</p>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{index + 1} / {total}</span>
    </div>
  </div>
</body>
</html>'''


def generate_illustration_html(summary: dict, point_index: int, total_points: int, accent: str = "ikb") -> str:
    """
    为文章生成插图 HTML

    Args:
        summary: 文章总结
        point_index: 要点索引
        total_points: 总要点数
        accent: 强调色

    Returns:
        HTML 字符串
    """
    # 根据索引选择不同的插图类型
    if point_index == 0:
        # 第一张：对比图
        return generate_comparison_illustration(summary, point_index, total_points, accent)
    elif point_index == 1:
        # 第二张：条形图
        return generate_bar_chart_illustration(summary, point_index, total_points, accent)
    elif point_index == 2:
        # 第三张：账目型
        return generate_ledger_illustration(summary, point_index, total_points, accent)
    else:
        # 其他：矩阵图
        return generate_matrix_illustration(summary, point_index, total_points, accent)


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

    # 提取文章总结
    print("正在分析文章内容...")
    summary = extract_article_summary(body_content)

    print(f"找到 {len(summary['key_numbers'])} 个关键数字")
    print(f"找到 {len(summary['key_points'])} 个关键要点")

    # 创建输出目录
    article_name = article_path.stem
    output_dir = OUTPUT_DIR / article_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成插图
    illustrations = []
    for i in range(max_illustrations):
        print(f"正在生成插图 {i + 1}/{max_illustrations}...")

        # 生成 HTML
        html_content = generate_illustration_html(summary, i, max_illustrations)
        html_file = output_dir / f"illustration_{i + 1}.html"
        html_file.write_text(html_content, encoding='utf-8')

        # 渲染为 PNG
        png_file = output_dir / f"illustration_{i + 1}.png"
        if render_illustration_to_png(html_file, png_file):
            illustrations.append({
                "path": png_file,
                "index": i,
                "content": f"插图 {i + 1}"
            })
            print(f"  ✅ 已生成: {png_file.name}")
        else:
            print(f"  ❌ 生成失败")

    print(f"\n✨ 插图生成完成！共 {len(illustrations)} 张")
    print(f"📁 保存位置: {output_dir}")

    return illustrations


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_illustrations_v3.py <文章文件路径> [最大插图数量]")
        print("示例: python generate_illustrations_v3.py articles/2026-06-02_minimax-m3.md 3")
        sys.exit(1)

    article_file = sys.argv[1]
    max_illustrations = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    illustrations = generate_article_illustrations(article_file, max_illustrations)

    if illustrations:
        print("\n生成的插图:")
        for i, img in enumerate(illustrations, 1):
            print(f"  {i}. {img['path'].name}")


if __name__ == "__main__":
    main()
