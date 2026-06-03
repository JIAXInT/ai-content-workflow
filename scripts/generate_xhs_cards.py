#!/usr/bin/env python3
"""
小红书套图生成器
基于文章内容生成丰富的小红书轮播图
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
OUTPUT_DIR = BASE_DIR / "covers"


def generate_xhs_cover(article_data: dict) -> str:
    """生成小红书封面图"""
    title = article_data["title"]
    subtitle = article_data["subtitle"]
    tags = article_data["tags"]

    # 截断标题
    if len(title) > 20:
        title_display = title[:18] + "..."
    else:
        title_display = title

    tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags[:4]])

    return f'''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>小红书封面</title>
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
      width:1080px;height:1440px;position:relative;background:var(--paper);overflow:hidden;
      padding:96px 88px;display:flex;flex-direction:column;justify-content:center;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .content{{
      position:relative;z-index:2;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:48px;
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:16px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);margin:0;
    }}
    .t-meta{{
      font-family:var(--mono);font-weight:500;font-size:14px;letter-spacing:.14em;
      text-transform:uppercase;color:var(--grey-3);margin:0;
    }}
    .h-statement{{
      font-family:var(--sans-zh);font-weight:200;font-size:96px;line-height:1.05;
      letter-spacing:-.015em;margin:0 0 32px;color:var(--ink);
    }}
    .accent-block{{
      background:var(--accent);color:var(--accent-on);padding:32px;margin-bottom:48px;
    }}
    .accent-text{{
      font-family:var(--mono);font-size:20px;margin:0;
    }}
    .tags{{
      display:flex;flex-wrap:wrap;gap:12px;
    }}
    .tag{{
      font-family:var(--mono);font-size:14px;padding:8px 16px;
      border:1px solid var(--ink);color:var(--ink);
    }}
    .issue-strip{{
      position:absolute;bottom:96px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:20px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="content">
      <div class="chrome-min">
        <span class="t-cat">AI · 模型发布</span>
        <span class="t-meta">2026.06.02</span>
      </div>
      <h1 class="h-statement">{title_display}</h1>
      <div class="accent-block">
        <p class="accent-text">SWE-Bench Pro 59.0% · 接近 Opus 4.7</p>
      </div>
      <div class="tags">
        {tags_html}
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>1 / 5</span>
    </div>
  </div>
</body>
</html>'''


def generate_xhs_data(article_data: dict) -> str:
    """生成小红书数据图"""
    return f'''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>小红书数据图</title>
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
      width:1080px;height:1440px;position:relative;background:var(--paper);overflow:hidden;
      padding:96px 88px;display:flex;flex-direction:column;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .content{{
      position:relative;z-index:2;flex:1;display:flex;flex-direction:column;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:40px;
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:16px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);margin:0;
    }}
    .t-meta{{
      font-family:var(--mono);font-weight:500;font-size:14px;letter-spacing:.14em;
      text-transform:uppercase;color:var(--grey-3);margin:0;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:64px;line-height:1.1;
      margin:0 0 48px;color:var(--ink);
    }}
    .kpi-row{{
      display:grid;grid-template-columns:repeat(2,1fr);gap:32px;flex:1;align-items:center;
    }}
    .kpi-item{{
      display:flex;flex-direction:column;gap:12px;
    }}
    .kpi-num{{
      font-family:var(--sans);font-weight:200;font-size:88px;line-height:1;
      letter-spacing:-.02em;color:var(--accent);
    }}
    .kpi-label{{
      font-family:var(--mono);font-size:18px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--grey-3);
    }}
    .kpi-desc{{
      font-family:var(--sans-zh);font-size:20px;color:var(--ink);
    }}
    .issue-strip{{
      position:absolute;bottom:96px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:20px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="content">
      <div class="chrome-min">
        <span class="t-cat">Data · 核心数据</span>
        <span class="t-meta">2 / 5</span>
      </div>
      <h2 class="h-xl">一组数字看懂 M3</h2>
      <div class="kpi-row">
        <div class="kpi-item">
          <span class="kpi-num">59.0%</span>
          <span class="kpi-label">SWE-Bench Pro</span>
          <span class="kpi-desc">编程能力，接近 Opus 4.7</span>
        </div>
        <div class="kpi-item">
          <span class="kpi-num">100万</span>
          <span class="kpi-label">Token 上下文</span>
          <span class="kpi-desc">超长上下文窗口</span>
        </div>
        <div class="kpi-item">
          <span class="kpi-num">$0.12</span>
          <span class="kpi-label">每百万 Token</span>
          <span class="kpi-desc">Opus 的 1/125</span>
        </div>
        <div class="kpi-item">
          <span class="kpi-num">9.4×</span>
          <span class="kpi-label">CUDA 加速</span>
          <span class="kpi-desc">优化后性能提升</span>
        </div>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>2 / 5</span>
    </div>
  </div>
</body>
</html>'''


def generate_xhs_compare(article_data: dict) -> str:
    """生成小红书对比图"""
    return f'''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>小红书对比图</title>
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
      width:1080px;height:1440px;position:relative;background:var(--paper);overflow:hidden;
      padding:96px 88px;display:flex;flex-direction:column;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .content{{
      position:relative;z-index:2;flex:1;display:flex;flex-direction:column;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:40px;
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:16px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);margin:0;
    }}
    .t-meta{{
      font-family:var(--mono);font-weight:500;font-size:14px;letter-spacing:.14em;
      text-transform:uppercase;color:var(--grey-3);margin:0;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:56px;line-height:1.1;
      margin:0 0 40px;color:var(--ink);
    }}
    .compare{{
      display:grid;grid-template-columns:1fr 1fr;gap:24px;flex:1;
    }}
    .signal{{
      padding:32px;display:flex;flex-direction:column;
    }}
    .signal-a{{
      background:var(--ink);color:var(--paper);
    }}
    .signal-b{{
      background:var(--grey-1);border:2px solid var(--ink);
    }}
    .signal-label{{
      font-family:var(--mono);font-size:14px;letter-spacing:.12em;text-transform:uppercase;
      margin:0 0 20px;
    }}
    .signal-a .signal-label{{color:var(--accent)}}
    .signal-b .signal-label{{color:var(--grey-3)}}
    .signal-title{{
      font-family:var(--sans-zh);font-weight:600;font-size:40px;margin:0 0 20px;
    }}
    .signal-price{{
      font-family:var(--sans);font-weight:200;font-size:48px;margin:0 0 16px;
    }}
    .signal-points{{
      display:flex;flex-direction:column;gap:12px;margin-top:auto;
    }}
    .point{{
      font-family:var(--sans-zh);font-size:18px;
    }}
    .issue-strip{{
      position:absolute;bottom:96px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:20px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="content">
      <div class="chrome-min">
        <span class="t-cat">Compare · 价格对比</span>
        <span class="t-meta">3 / 5</span>
      </div>
      <h2 class="h-xl">现在，它们同价了</h2>
      <div class="compare">
        <div class="signal signal-a">
          <p class="signal-label">MiMo M3</p>
          <h3 class="signal-title">开源</h3>
          <p class="signal-price">$0.12/M</p>
          <div class="signal-points">
            <span class="point">✓ SWE-Bench 59.0%</span>
            <span class="point">✓ 100万 Token</span>
            <span class="point">✓ 多模态支持</span>
            <span class="point">✓ 可本地部署</span>
          </div>
        </div>
        <div class="signal signal-b">
          <p class="signal-label">Opus 4.7</p>
          <h3 class="signal-title">闭源</h3>
          <p class="signal-price">$15/M</p>
          <div class="signal-points">
            <span class="point">✓ SWE-Bench 62.1%</span>
            <span class="point">✓ 20万 Token</span>
            <span class="point">✓ 成熟生态</span>
            <span class="point">✓ 企业支持</span>
          </div>
        </div>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>3 / 5</span>
    </div>
  </div>
</body>
</html>'''


def generate_xhs_features(article_data: dict) -> str:
    """生成小红书特性图"""
    return f'''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>小红书特性图</title>
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
      width:1080px;height:1440px;position:relative;background:var(--ink);overflow:hidden;
      padding:96px 88px;display:flex;flex-direction:column;
    }}
    .content{{
      position:relative;z-index:2;flex:1;display:flex;flex-direction:column;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,.2);margin-bottom:40px;
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
      font-family:var(--sans-zh);font-weight:200;font-size:64px;line-height:1.1;
      margin:0 0 48px;color:var(--paper);
    }}
    .features{{
      display:flex;flex-direction:column;gap:24px;flex:1;
    }}
    .feature{{
      display:grid;grid-template-columns:80px 1fr;gap:24px;
      padding:24px 0;border-bottom:1px solid rgba(255,255,255,.2);
    }}
    .feature:last-child{{border-bottom:0}}
    .feature-num{{
      font-family:var(--mono);font-size:32px;color:var(--accent);
    }}
    .feature-content{{
      display:flex;flex-direction:column;gap:8px;
    }}
    .feature-title{{
      font-family:var(--sans-zh);font-weight:600;font-size:28px;color:var(--paper);
    }}
    .feature-desc{{
      font-family:var(--sans-zh);font-size:20px;color:rgba(255,255,255,.7);
    }}
    .issue-strip{{
      position:absolute;bottom:96px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:rgba(255,255,255,.4);
      border-top:1px solid rgba(255,255,255,.2);padding-top:20px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="content">
      <div class="chrome-min">
        <span class="t-cat">Features · 核心特性</span>
        <span class="t-meta">4 / 5</span>
      </div>
      <h2 class="h-xl">M3 的五大核心特性</h2>
      <div class="features">
        <div class="feature">
          <span class="feature-num">01</span>
          <div class="feature-content">
            <h3 class="feature-title">MSA 稀疏注意力</h3>
            <p class="feature-desc">每 Token 计算量降至前代的 1/20，预填充速度提升 9 倍以上</p>
          </div>
        </div>
        <div class="feature">
          <span class="feature-num">02</span>
          <div class="feature-content">
            <h3 class="feature-title">100 万 Token 上下文</h3>
            <p class="feature-desc">可处理整本技术文档、大型代码仓库、全天会议录音</p>
          </div>
        </div>
        <div class="feature">
          <span class="feature-num">03</span>
          <div class="feature-content">
            <h3 class="feature-title">原生多模态</h3>
            <p class="feature-desc">支持图像和视频输入，可操控桌面计算机</p>
          </div>
        </div>
        <div class="feature">
          <span class="feature-num">04</span>
          <div class="feature-content">
            <h3 class="feature-title">思维模式开关</h3>
            <p class="feature-desc">开启适合复杂任务，关闭适合低延迟场景，价格相同</p>
          </div>
        </div>
        <div class="feature">
          <span class="feature-num">05</span>
          <div class="feature-content">
            <h3 class="feature-title">全面开源</h3>
            <p class="feature-desc">模型权重、技术报告、训练框架全部开源</p>
          </div>
        </div>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>4 / 5</span>
    </div>
  </div>
</body>
</html>'''


def generate_xhs_summary(article_data: dict) -> str:
    """生成小红书总结图"""
    return f'''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>小红书总结图</title>
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
      width:1080px;height:1440px;position:relative;background:var(--paper);overflow:hidden;
      padding:96px 88px;display:flex;flex-direction:column;
    }}
    .dot-mat{{
      position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.08;
      background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);
      background-size:24px 24px;
    }}
    .content{{
      position:relative;z-index:2;flex:1;display:flex;flex-direction:column;
    }}
    .chrome-min{{
      display:flex;justify-content:space-between;align-items:center;
      padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:40px;
    }}
    .t-cat{{
      font-family:var(--mono);font-weight:600;font-size:16px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--accent);margin:0;
    }}
    .t-meta{{
      font-family:var(--mono);font-weight:500;font-size:14px;letter-spacing:.14em;
      text-transform:uppercase;color:var(--grey-3);margin:0;
    }}
    .h-xl{{
      font-family:var(--sans-zh);font-weight:300;font-size:56px;line-height:1.1;
      margin:0 0 48px;color:var(--ink);
    }}
    .conclusions{{
      display:flex;flex-direction:column;gap:32px;flex:1;
    }}
    .conclusion{{
      display:grid;grid-template-columns:80px 1fr;gap:24px;
      padding:24px 0;border-bottom:1px solid var(--grey-2);
    }}
    .conclusion:last-child{{border-bottom:0}}
    .conclusion-num{{
      font-family:var(--sans);font-weight:200;font-size:48px;color:var(--accent);
    }}
    .conclusion-content{{
      display:flex;flex-direction:column;gap:8px;
    }}
    .conclusion-title{{
      font-family:var(--sans-zh);font-weight:600;font-size:28px;color:var(--ink);
    }}
    .conclusion-desc{{
      font-family:var(--sans-zh);font-size:20px;color:var(--grey-3);
    }}
    .cta{{
      margin-top:auto;padding:24px;background:var(--accent);color:var(--accent-on);
      text-align:center;
    }}
    .cta-text{{
      font-family:var(--sans-zh);font-size:20px;margin:0;
    }}
    .issue-strip{{
      position:absolute;bottom:96px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:var(--mono);font-size:14px;color:var(--grey-3);
      border-top:1px solid var(--grey-2);padding-top:20px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="content">
      <div class="chrome-min">
        <span class="t-cat">Summary · 总结</span>
        <span class="t-meta">5 / 5</span>
      </div>
      <h2 class="h-xl">三个关键结论</h2>
      <div class="conclusions">
        <div class="conclusion">
          <span class="conclusion-num">01</span>
          <div class="conclusion-content">
            <h3 class="conclusion-title">开源模型已具备软件工程能力</h3>
            <p class="conclusion-desc">M3 在 SWE-Bench Pro 上的 59.0% 得分证明了这一点</p>
          </div>
        </div>
        <div class="conclusion">
          <span class="conclusion-num">02</span>
          <div class="conclusion-content">
            <h3 class="conclusion-title">价格战加速 AI 基础设施化</h3>
            <p class="conclusion-desc">$0.12/M tokens，AI 正在变得越来越便宜</p>
          </div>
        </div>
        <div class="conclusion">
          <span class="conclusion-num">03</span>
          <div class="conclusion-content">
            <h3 class="conclusion-title">开发者是最大受益者</h3>
            <p class="conclusion-desc">更多选择，更低成本，更强能力</p>
          </div>
        </div>
      </div>
      <div class="cta">
        <p class="cta-text">关注 AI创享派，获取最新 AI 资讯</p>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>5 / 5</span>
    </div>
  </div>
</body>
</html>'''


def render_card_to_png(html_content: str, output_file: Path, width: int = 1080, height: int = 1440) -> bool:
    """将 HTML 渲染为 PNG"""
    from playwright.sync_api import sync_playwright

    # 保存 HTML 到临时文件
    temp_html = Path("temp_card.html")
    temp_html.write_text(html_content, encoding='utf-8')

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=2
            )
            page = context.new_page()

            # 加载 HTML
            page.goto(f"file:///{temp_html.resolve().as_posix()}")
            page.wait_for_timeout(1500)

            # 查找卡片元素
            card = page.query_selector('.card')
            if card:
                card.screenshot(path=str(output_file))
                page.close()
                context.close()
                browser.close()
                temp_html.unlink(missing_ok=True)
                return True
            else:
                print(f"  ⚠️ 未找到卡片元素")
                page.close()
                context.close()
                browser.close()
                temp_html.unlink(missing_ok=True)
                return False
    except Exception as e:
        print(f"  ❌ 渲染失败: {e}")
        temp_html.unlink(missing_ok=True)
        return False


def generate_xhs_cards(article_file: str) -> list:
    """
    生成小红书套图

    Args:
        article_file: 文章文件路径

    Returns:
        生成的图片路径列表
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

    # 提取文章数据
    title_match = re.search(r'^#\s+(.+)$', body_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "未命名文章"

    # 提取标签
    tags = ["AI", "大模型", "开源", "编程"]

    # 提取副标题
    subtitle = "性能接近 Opus 4.7，价格只有 1%"

    article_data = {
        "title": title,
        "subtitle": subtitle,
        "tags": tags,
    }

    # 创建输出目录
    article_name = article_path.stem
    output_dir = OUTPUT_DIR / article_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成 5 张小红书卡片
    cards = [
        ("cover", generate_xhs_cover(article_data)),
        ("data", generate_xhs_data(article_data)),
        ("compare", generate_xhs_compare(article_data)),
        ("features", generate_xhs_features(article_data)),
        ("summary", generate_xhs_summary(article_data)),
    ]

    generated_files = []

    for i, (card_type, html_content) in enumerate(cards, 1):
        print(f"正在生成第 {i} 张卡片: {card_type}...")

        output_file = output_dir / f"xhs-{i:02d}-{card_type}.png"

        if render_card_to_png(html_content, output_file):
            generated_files.append(output_file)
            print(f"  ✅ 已生成: {output_file.name}")
        else:
            print(f"  ❌ 生成失败")

    print(f"\n✨ 小红书套图生成完成！共 {len(generated_files)} 张")
    print(f"📁 保存位置: {output_dir}")

    return generated_files


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_xhs_cards.py <文章文件路径>")
        print("示例: python generate_xhs_cards.py articles/2026-06-02_minimax-m3.md")
        sys.exit(1)

    article_file = sys.argv[1]

    generated_files = generate_xhs_cards(article_file)

    if generated_files:
        print("\n生成的文件:")
        for f in generated_files:
            print(f"  - {f.name}")


if __name__ == "__main__":
    main()
