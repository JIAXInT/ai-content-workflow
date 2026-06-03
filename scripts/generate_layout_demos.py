#!/usr/bin/env python3
"""
生成 28 个版式骨架的真正布局示例
"""

import sys
import io
from pathlib import Path

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def generate_m01():
    """M01 Cover — 杂志封面"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M01 Cover</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,[data-theme="ink-classic"]{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22);--accent:#111111}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1080px;height:1440px;background:var(--paper);position:relative;overflow:hidden;padding:96px 88px;display:flex;flex-direction:column}
    .grain{position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);background-size:3px 3px}
    .issue-row{display:flex;align-items:center;gap:16px;font-family:"IBM Plex Mono",monospace;font-size:18px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:48px}
    .issue-row .dot{width:6px;height:6px;border-radius:50%;background:var(--accent)}
    .h-display{font-family:"Noto Serif SC",serif;font-weight:500;font-size:124px;line-height:1.06;letter-spacing:.04em;margin:0 0 32px;color:var(--ink)}
    .h-sub{font-family:"Playfair Display",serif;font-style:italic;font-weight:400;font-size:36px;color:var(--muted);margin:0 0 48px}
    .hero-img{width:100%;aspect-ratio:16/10;background:var(--ink);margin-bottom:48px}
    .lead{font-family:"Noto Serif SC",serif;font-weight:400;font-size:28px;line-height:1.55;color:rgba(10,10,11,.82);margin:0 0 32px}
    .points{display:flex;flex-direction:column;gap:16px;margin-top:auto}
    .point{display:flex;align-items:baseline;gap:16px;font-family:"Noto Serif SC",serif;font-size:22px;line-height:1.5}
    .point-nb{font-family:"IBM Plex Mono",monospace;font-size:18px;color:var(--muted);min-width:32px}
    .issue-strip{position:absolute;bottom:56px;left:88px;right:88px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);border-top:1px solid var(--line);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <div class="issue-row"><span>Vol. 01</span><span class="dot"></span><span>2026.06</span></div>
    <h1 class="h-display">MiMo M3<br>开源了</h1>
    <p class="h-sub">Performance approaching Opus 4.7</p>
    <div class="hero-img"></div>
    <p class="lead">一个开源模型，在编程能力上逼近目前公认的最强闭源模型，这事儿是不是有点离谱了？</p>
    <div class="points">
      <div class="point"><span class="point-nb">01</span><span>SWE-Bench Pro 59.0%，超越 GPT-5.5</span></div>
      <div class="point"><span class="point-nb">02</span><span>100万 token 上下文窗口</span></div>
      <div class="point"><span class="point-nb">03</span><span>价格只有 Opus 的百分之一</span></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M01 · Cover</span></div>
  </div>
</body>
</html>'''


def generate_m02():
    """M02 Field Note Photo — 田野笔记照片"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M02 Field Note</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-columns:1.2fr 1fr}
    .photo{background:var(--ink);position:relative}
    .photo-label{position:absolute;bottom:40px;left:40px;font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.7);letter-spacing:.12em;text-transform:uppercase}
    .content{padding:80px;display:flex;flex-direction:column;justify-content:center}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:56px;line-height:1.1;margin:0 0 32px;color:var(--ink)}
    .body{font-family:"Noto Serif SC",serif;font-size:24px;line-height:1.6;color:var(--ink);margin:0 0 48px}
    .caption{font-family:"IBM Plex Mono",monospace;font-size:18px;color:var(--muted);margin-top:auto;padding-top:32px;border-top:1px solid var(--line)}
  </style>
</head>
<body>
  <div class="card">
    <div class="photo"><span class="photo-label">Field Note · 现场记录</span></div>
    <div class="content">
      <p class="kicker">Observation</p>
      <h1 class="h-xl">在咖啡馆<br>看到有人用<br>Claude Code</h1>
      <p class="body">他一边喝咖啡，一边看着屏幕上自动生成的代码，嘴角微微上扬。那种表情我太熟悉了，是第一次感受到AI编程魔力时的惊喜。</p>
      <p class="caption">M02 · Field Note Photo</p>
    </div>
  </div>
</body>
</html>'''


def generate_m03():
    """M03 Editorial Essay Split — 编辑分栏随笔"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M03 Essay Split</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-columns:1fr 1fr}
    .left{padding:80px;display:flex;flex-direction:column;justify-content:center;border-right:1px solid var(--line)}
    .right{padding:80px;display:flex;flex-direction:column;justify-content:center}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:64px;line-height:1.1;margin:0 0 32px;color:var(--ink)}
    .h-sub{font-family:"Playfair Display",serif;font-style:italic;font-size:28px;color:var(--muted);margin:0 0 48px}
    .para{font-family:"Noto Serif SC",serif;font-size:22px;line-height:1.65;color:var(--ink);margin:0 0 24px}
    .para:last-child{margin-bottom:0}
    .nb{font-family:"IBM Plex Mono",monospace;font-size:28px;color:var(--muted);margin:0 0 16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="left">
      <p class="kicker">Essay</p>
      <h1 class="h-xl">信息差<br>是亘古不变的</h1>
      <p class="h-sub">The eternal information gap</p>
    </div>
    <div class="right">
      <p class="nb">01</p>
      <p class="para">你想想看，1880年代电力普及时，大多数人还在用蜡烛。知道电灯的人，和不知道的人，活在完全不同的世界里。</p>
      <p class="nb">02</p>
      <p class="para">现在AI也是一样。知道怎么用Claude Code的人，效率是不知道的人的十倍。这个差距，比电灯和蜡烛的差距还大。</p>
      <p class="nb">03</p>
      <p class="para">我不是在制造焦虑，我是在说一个事实。信息差从来不会消失，它只会换一种形式存在。</p>
    </div>
  </div>
</body>
</html>'''


def generate_m04():
    """M04 Pull Quote / Thesis — 引文/论点"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M04 Pull Quote</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:80px 120px;display:flex;flex-direction:column;justify-content:center;align-items:center}
    .grain{position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);background-size:3px 3px}
    .quote-mark{font-family:"Playfair Display",serif;font-size:120px;line-height:1;color:var(--muted);opacity:.4;margin-bottom:32px}
    .quote{font-family:"Noto Serif SC",serif;font-weight:500;font-size:72px;line-height:1.3;text-align:center;color:var(--ink);margin:0 0 48px}
    .source{font-family:"IBM Plex Mono",monospace;font-size:18px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 16px}
    .context{font-family:"Noto Serif SC",serif;font-size:20px;color:var(--muted);text-align:center;max-width:800px}
    .issue-strip{position:absolute;bottom:56px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <div class="quote-mark">"</div>
    <p class="quote">开源的力量，不在于单个产品的性能，而在于整个生态的活力。</p>
    <p class="source">— AI创享派</p>
    <p class="context">M3 的出现，让开源生态在编程能力这个关键维度上，第一次真正逼近了闭源最强。</p>
    <div class="issue-strip"><span>AI创享派</span><span>M04 · Pull Quote</span></div>
  </div>
</body>
</html>'''


def generate_m05():
    """M05 Checklist / Buying Guide — 清单/选购指南"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M05 Checklist</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22);--accent:#111111}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1080px;height:1440px;background:var(--paper);position:relative;overflow:hidden;padding:96px 88px;display:flex;flex-direction:column}
    .grain{position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);background-size:3px 3px}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:56px;line-height:1.1;margin:0 0 48px;color:var(--ink)}
    .checklist{display:flex;flex-direction:column;gap:0;flex:1}
    .check-row{display:grid;grid-template-columns:60px 1fr auto;gap:24px;align-items:baseline;padding:28px 0;border-bottom:1px solid var(--line)}
    .check-row:last-child{border-bottom:0}
    .check-nb{font-family:"IBM Plex Mono",monospace;font-size:24px;color:var(--accent)}
    .check-item{font-family:"Noto Serif SC",serif;font-weight:500;font-size:28px;color:var(--ink)}
    .check-result{font-family:"IBM Plex Mono",monospace;font-size:16px;color:var(--muted);text-align:right}
    .issue-strip{position:absolute;bottom:56px;left:88px;right:88px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <p class="kicker">Checklist</p>
    <h1 class="h-xl">选模型前<br>先看这5点</h1>
    <div class="checklist">
      <div class="check-row"><span class="check-nb">01</span><span class="check-item">编程能力</span><span class="check-result">SWE-Bench Pro</span></div>
      <div class="check-row"><span class="check-nb">02</span><span class="check-item">上下文长度</span><span class="check-result">Token 窗口</span></div>
      <div class="check-row"><span class="check-nb">03</span><span class="check-item">多模态支持</span><span class="check-result">图像/视频</span></div>
      <div class="check-row"><span class="check-nb">04</span><span class="check-item">价格</span><span class="check-result">每百万 Token</span></div>
      <div class="check-row"><span class="check-nb">05</span><span class="check-item">开源程度</span><span class="check-result">权重/代码/数据</span></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M05 · Checklist</span></div>
  </div>
</body>
</html>'''


def generate_m06():
    """M06 Evidence Wall — 证据墙"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M06 Evidence Wall</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;margin:0;color:var(--ink)}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
    .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;flex:1}
    .evidence{background:var(--ink);position:relative;display:flex;align-items:flex-end;padding:24px}
    .evidence-label{font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.8)}
    .caption{font-family:"Noto Serif SC",serif;font-size:20px;color:var(--muted);margin-top:24px;text-align:center}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">三张图看懂 M3</h1>
      <span class="kicker">Evidence Wall</span>
    </div>
    <div class="grid">
      <div class="evidence"><span class="evidence-label">SWE-Bench Pro 59.0%</span></div>
      <div class="evidence"><span class="evidence-label">100万 Token 上下文</span></div>
      <div class="evidence"><span class="evidence-label">价格 $0.12/M Tokens</span></div>
    </div>
    <p class="caption">数据来源：MiniMax 官方博客</p>
    <div class="issue-strip"><span>AI创享派</span><span>M06 · Evidence Wall</span></div>
  </div>
</body>
</html>'''


def generate_m07():
    """M07 Closing Note — 收尾笔记"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M07 Closing Note</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1080px;height:1440px;background:var(--paper);position:relative;overflow:hidden;padding:96px 88px;display:flex;flex-direction:column}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;line-height:1.2;margin:0 0 48px;color:var(--ink)}
    .ledger{display:flex;flex-direction:column;flex:1}
    .ledger-row{display:grid;grid-template-columns:80px 1fr;gap:24px;align-items:baseline;padding:32px 0;border-bottom:1px solid var(--line)}
    .ledger-row:last-child{border-bottom:0}
    .ledger-nb{font-family:"IBM Plex Mono",monospace;font-size:28px;color:var(--muted)}
    .ledger-title{font-family:"Noto Serif SC",serif;font-weight:500;font-size:32px;color:var(--ink)}
    .closing{margin-top:auto;padding-top:32px;border-top:1px solid var(--line)}
    .closing-text{font-family:"Noto Serif SC",serif;font-style:italic;font-size:24px;color:var(--muted)}
    .issue-strip{position:absolute;bottom:56px;left:88px;right:88px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <h1 class="h-xl">三个关键结论</h1>
    <div class="ledger">
      <div class="ledger-row"><span class="ledger-nb">01</span><span class="ledger-title">开源模型已具备软件工程能力</span></div>
      <div class="ledger-row"><span class="ledger-nb">02</span><span class="ledger-title">价格战加速AI基础设施化</span></div>
      <div class="ledger-row"><span class="ledger-nb">03</span><span class="ledger-title">开发者是最大受益者</span></div>
    </div>
    <div class="closing">
      <p class="closing-text">技术的进步最终会让所有人受益。</p>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M07 · Closing Note</span></div>
  </div>
</body>
</html>'''


def generate_m08():
    """M08 Tall Ledger — 高账目表"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M08 Tall Ledger</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;margin:0;color:var(--ink)}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
    .ledger{display:flex;flex-direction:column;flex:1}
    .ledger-row{display:grid;grid-template-columns:120px 1fr 200px;gap:32px;align-items:baseline;padding:28px 0;border-bottom:1px solid var(--line)}
    .ledger-row:last-child{border-bottom:0}
    .ledger-idx{font-family:"IBM Plex Mono",monospace;font-size:20px;color:var(--muted)}
    .ledger-title{font-family:"Noto Serif SC",serif;font-weight:500;font-size:32px;color:var(--ink)}
    .ledger-note{font-family:"Noto Serif SC",serif;font-size:20px;color:var(--muted);text-align:right}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">M3 vs 竞品对比</h1>
      <span class="kicker">Comparison</span>
    </div>
    <div class="ledger">
      <div class="ledger-row"><span class="ledger-idx">01</span><span class="ledger-title">SWE-Bench Pro</span><span class="ledger-note">59.0% vs 58.2%</span></div>
      <div class="ledger-row"><span class="ledger-idx">02</span><span class="ledger-title">Terminal-Bench</span><span class="ledger-note">66.0% vs 64.5%</span></div>
      <div class="ledger-row"><span class="ledger-idx">03</span><span class="ledger-title">上下文长度</span><span class="ledger-note">100万 vs 20万</span></div>
      <div class="ledger-row"><span class="ledger-idx">04</span><span class="ledger-title">价格</span><span class="ledger-note">$0.12 vs $15</span></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M08 · Tall Ledger</span></div>
  </div>
</body>
</html>'''


def generate_m09():
    """M09 Atmospheric Thesis — 氛围论点"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M09 Atmospheric Thesis</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--ink);position:relative;overflow:hidden;padding:80px 120px;display:flex;flex-direction:column;justify-content:center}
    .grain{position:absolute;inset:0;opacity:.26;mix-blend-mode:screen;background-image:radial-gradient(rgba(255,244,214,.10) 1px,transparent 1px);background-size:3px 3px}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.5);margin:0 0 32px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:500;font-size:72px;line-height:1.2;color:var(--paper);margin:0 0 48px}
    .note{font-family:"Noto Serif SC",serif;font-size:24px;line-height:1.6;color:rgba(255,255,255,.6);max-width:800px}
    .issue-strip{position:absolute;bottom:56px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.4);border-top:1px solid rgba(255,255,255,.2);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <p class="kicker">Thesis</p>
    <h1 class="h-xl">AI正在变得<br>越来越便宜<br>便宜到不需要比较</h1>
    <p class="note">M3 的出现，加速了这个进程。这是好事。</p>
    <div class="issue-strip"><span>AI创享派</span><span>M09 · Atmospheric Thesis</span></div>
  </div>
</body>
</html>'''


def generate_m10():
    """M10 Evidence Feature — 证据专题"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M10 Evidence Feature</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-rows:auto 1fr auto}
    .header{padding:40px 80px;display:flex;justify-content:space-between;align-items:baseline}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;margin:0;color:var(--ink)}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
    .hero{background:var(--ink);min-height:400px}
    .footer{padding:32px 80px;display:flex;gap:48px}
    .point{flex:1;padding:24px 0;border-top:1px solid var(--line)}
    .point-nb{font-family:"IBM Plex Mono",monospace;font-size:20px;color:var(--muted);margin:0 0 12px}
    .point-text{font-family:"Noto Serif SC",serif;font-size:22px;color:var(--ink);margin:0}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">CUDA Kernel 优化过程</h1>
      <span class="kicker">Evidence</span>
    </div>
    <div class="hero"></div>
    <div class="footer">
      <div class="point"><p class="point-nb">147</p><p class="point-text">次基准提交</p></div>
      <div class="point"><p class="point-nb">1,959</p><p class="point-text">次工具调用</p></div>
      <div class="point"><p class="point-nb">9.4×</p><p class="point-text">性能提升</p></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M10 · Evidence Feature</span></div>
  </div>
</body>
</html>'''


def generate_m11():
    """M11 Marginalia Essay — 旁注随笔"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M11 Marginalia</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-columns:1fr 280px}
    .main{padding:80px;display:flex;flex-direction:column;justify-content:center;border-right:1px solid var(--line)}
    .margin{padding:80px 40px;display:flex;flex-direction:column;justify-content:center}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:56px;line-height:1.15;margin:0 0 32px;color:var(--ink)}
    .para{font-family:"Noto Serif SC",serif;font-size:24px;line-height:1.65;color:var(--ink);margin:0 0 24px}
    .margin-note{font-family:"IBM Plex Mono",monospace;font-size:16px;line-height:1.6;color:var(--muted);margin:0 0 24px;padding-left:16px;border-left:2px solid var(--line)}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="main">
      <p class="kicker">Essay</p>
      <h1 class="h-xl">MSA架构<br>为什么重要</h1>
      <p class="para">传统的注意力机制，计算量会随着文本长度的平方增长。100万token的上下文窗口，如果用传统方法，计算量会大到根本跑不动。</p>
      <p class="para">MSA的解决方案是稀疏注意力。它不是让模型看每一个token对其他所有token的关系，而是只看最相关的那些。</p>
    </div>
    <div class="margin">
      <p class="margin-note">每token计算量降至前代的1/20</p>
      <p class="margin-note">预填充速度提升9倍以上</p>
      <p class="margin-note">解码速度提升15倍以上</p>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M11 · Marginalia</span></div>
  </div>
</body>
</html>'''


def generate_m12():
    """M12 Section Divider — 章节分隔页"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M12 Section Divider</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--ink);position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center;align-items:center}
    .grain{position:absolute;inset:0;opacity:.26;mix-blend-mode:screen;background-image:radial-gradient(rgba(255,244,214,.10) 1px,transparent 1px);background-size:3px 3px}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:18px;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,255,255,.5);margin:0 0 48px}
    .h-display{font-family:"Noto Serif SC",serif;font-weight:500;font-size:96px;line-height:1.1;color:var(--paper);margin:0 0 24px;text-align:center}
    .h-sub{font-family:"Playfair Display",serif;font-style:italic;font-size:28px;color:rgba(255,255,255,.5);margin:0}
    .issue-strip{position:absolute;bottom:56px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.4);border-top:1px solid rgba(255,255,255,.2);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <p class="kicker">Act II</p>
    <h1 class="h-display">技术细节</h1>
    <p class="h-sub">The technical deep dive</p>
    <div class="issue-strip"><span>AI创享派</span><span>M12 · Section Divider</span></div>
  </div>
</body>
</html>'''


def generate_m13():
    """M13 Hero Question — 核心问题"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M13 Hero Question</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--ink);position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center;align-items:center}
    .grain{position:absolute;inset:0;opacity:.26;mix-blend-mode:screen;background-image:radial-gradient(rgba(255,244,214,.10) 1px,transparent 1px);background-size:3px 3px}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.5);margin:0 0 48px}
    .question{font-family:"Noto Serif SC",serif;font-weight:500;font-size:72px;line-height:1.3;color:var(--paper);text-align:center;max-width:1000px;margin:0 0 64px}
    .prompt{font-family:"Noto Serif SC",serif;font-size:22px;color:rgba(255,255,255,.6);text-align:center}
    .issue-strip{position:absolute;bottom:56px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.4);border-top:1px solid rgba(255,255,255,.2);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <p class="kicker">Question</p>
    <h1 class="question">当价格不再是门槛<br>真正决定胜负的是什么？</h1>
    <p class="prompt">欢迎在评论区分享你的看法</p>
    <div class="issue-strip"><span>AI创享派</span><span>M13 · Hero Question</span></div>
  </div>
</body>
</html>'''


def generate_m14():
    """M14 Vertical Pipeline — 竖向流水线"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M14 Pipeline</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1080px;height:1440px;background:var(--paper);position:relative;overflow:hidden;padding:96px 88px;display:flex;flex-direction:column}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;line-height:1.15;margin:0 0 48px;color:var(--ink)}
    .pipeline{display:flex;flex-direction:column;gap:0;flex:1}
    .step{display:grid;grid-template-columns:80px 1fr;gap:24px;align-items:baseline;padding:32px 0;border-bottom:1px solid var(--line)}
    .step:last-child{border-bottom:0}
    .step-nb{font-family:"IBM Plex Mono",monospace;font-size:32px;color:var(--muted)}
    .step-title{font-family:"Noto Serif SC",serif;font-weight:500;font-size:36px;color:var(--ink);margin:0 0 8px}
    .step-desc{font-family:"Noto Serif SC",serif;font-size:20px;color:var(--muted);margin:0}
    .issue-strip{position:absolute;bottom:56px;left:88px;right:88px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px}
  </style>
</head>
<body>
  <div class="card">
    <p class="kicker">Pipeline</p>
    <h1 class="h-xl">M3的<br>工作流程</h1>
    <div class="pipeline">
      <div class="step"><span class="step-nb">01</span><div><h3 class="step-title">理解需求</h3><p class="step-desc">分析代码库结构和issue描述</p></div></div>
      <div class="step"><span class="step-nb">02</span><div><h3 class="step-title">定位问题</h3><p class="step-desc">在复杂代码中找到关键位置</p></div></div>
      <div class="step"><span class="step-nb">03</span><div><h3 class="step-title">生成方案</h3><p class="step-desc">编写修复代码和测试用例</p></div></div>
      <div class="step"><span class="step-nb">04</span><div><h3 class="step-title">验证结果</h3><p class="step-desc">运行测试确保修改正确</p></div></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M14 · Pipeline</span></div>
  </div>
</body>
</html>'''


def generate_m15():
    """M15 Before / After — 前后对比"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M15 Before/After</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-rows:auto 1fr 1fr}
    .header{padding:40px 80px;display:flex;justify-content:space-between;align-items:baseline}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;margin:0;color:var(--ink)}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:14px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
    .before{padding:40px 80px;background:var(--ink);opacity:.68;display:flex;flex-direction:column;justify-content:center}
    .after{padding:40px 80px;display:flex;flex-direction:column;justify-content:center}
    .block-label{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 20px}
    .before .block-label{color:rgba(255,255,255,.7)}
    .after .block-label{color:var(--muted)}
    .block-title{font-family:"Noto Serif SC",serif;font-weight:500;font-size:36px;margin:0 0 16px}
    .before .block-title{color:var(--paper)}
    .after .block-title{color:var(--ink)}
    .block-points{display:flex;gap:32px}
    .point{font-family:"Noto Serif SC",serif;font-size:20px}
    .before .point{color:rgba(255,255,255,.8)}
    .after .point{color:var(--ink)}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">以前 vs 现在</h1>
      <span class="kicker">Before / After</span>
    </div>
    <div class="before">
      <p class="block-label">Before</p>
      <h3 class="block-title">用传统方法优化CUDA</h3>
      <div class="block-points">
        <span class="point">需要数周时间</span>
        <span class="point">需要资深工程师</span>
        <span class="point">效果不稳定</span>
      </div>
    </div>
    <div class="after">
      <p class="block-label">After</p>
      <h3 class="block-title">用M3自动优化</h3>
      <div class="block-points">
        <span class="point">24小时完成</span>
        <span class="point">无需人工干预</span>
        <span class="point">性能提升9.4倍</span>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M15 · Before/After</span></div>
  </div>
</body>
</html>'''


def generate_m16():
    """M16 Image-Led Cover — 图片主导封面"""
    return '''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>M16 Image-Led</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root{--paper:#f3f0e8;--ink:#0a0a0b;--muted:#68625a;--line:rgba(10,10,11,.22)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--ink);position:relative;overflow:hidden}
    .overlay{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.8),transparent 60%)}
    .content{position:absolute;bottom:80px;left:80px;right:80px}
    .kicker{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.6);margin:0 0 20px}
    .h-xl{font-family:"Noto Serif SC",serif;font-weight:700;font-size:64px;line-height:1.15;color:var(--paper);margin:0 0 16px}
    .desc{font-family:"Noto Serif SC",serif;font-size:22px;color:rgba(255,255,255,.7);margin:0}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.4);border-top:1px solid rgba(255,255,255,.2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="overlay"></div>
    <div class="content">
      <p class="kicker">Cover</p>
      <h1 class="h-xl">MiMo M3<br>开源新纪元</h1>
      <p class="desc">一个接近Opus 4.7性能的开源模型，价格只有百分之一</p>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M16 · Image-Led</span></div>
  </div>
</body>
</html>'''


def generate_s01():
    """S01 Accent Cover — 强调色封面"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S01 Accent Cover</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1080px;height:1440px;background:var(--paper);position:relative;overflow:hidden;padding:96px 88px;display:flex;flex-direction:column;justify-content:center}
    .dot-mat{position:absolute;inset:0;opacity:.08;background-image:radial-gradient(var(--ink) 1.5px,transparent 1.5px);background-size:24px 24px}
    .chrome-min{display:flex;justify-content:space-between;align-items:center;padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:48px}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .h-statement{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:200;font-size:124px;line-height:1.05;letter-spacing:-.015em;margin:0 0 48px;color:var(--ink)}
    .accent-block{background:var(--accent);color:var(--accent-on);padding:40px;margin-bottom:48px}
    .accent-text{font-family:"IBM Plex Mono",monospace;font-size:18px;margin:0}
    .tags{display:flex;flex-wrap:wrap;gap:12px;margin-top:auto}
    .tag{font-family:"IBM Plex Mono",monospace;font-size:14px;padding:8px 16px;border:1px solid var(--ink);color:var(--ink)}
    .issue-strip{position:absolute;bottom:96px;left:88px;right:88px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:20px}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="chrome-min">
      <span class="t-cat">S01 · Accent Cover</span>
      <span class="t-meta">2026.06</span>
    </div>
    <h1 class="h-statement">MiMo M3<br>开源了</h1>
    <div class="accent-block">
      <p class="accent-text">SWE-Bench Pro 59.0% · 接近 Opus 4.7</p>
    </div>
    <div class="tags">
      <span class="tag">开源</span>
      <span class="tag">编程</span>
      <span class="tag">AI</span>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S01 · Accent Cover</span></div>
  </div>
</body>
</html>'''


def generate_s02():
    """S02 Two Signals / Comparison — 双信号/对比"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S02 Comparison</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:56px;margin:0;color:var(--ink)}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    .compare{display:grid;grid-template-columns:1fr 1fr;gap:40px;flex:1}
    .signal{padding:40px;display:flex;flex-direction:column}
    .signal-a{background:var(--ink);color:var(--paper)}
    .signal-b{background:var(--grey-1);border:2px solid var(--ink)}
    .signal-label{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 24px}
    .signal-a .signal-label{color:var(--accent)}
    .signal-b .signal-label{color:var(--grey-3)}
    .signal-title{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:600;font-size:48px;margin:0 0 24px}
    .signal-points{display:flex;flex-direction:column;gap:16px;margin-top:auto}
    .point{font-family:"Inter","Noto Sans SC",sans-serif;font-size:20px}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">M3 vs Opus 4.7</h1>
      <span class="t-cat">Comparison</span>
    </div>
    <div class="compare">
      <div class="signal signal-a">
        <p class="signal-label">MiMo M3</p>
        <h3 class="signal-title">开源</h3>
        <div class="signal-points">
          <span class="point">✓ SWE-Bench 59.0%</span>
          <span class="point">✓ 100万 Token</span>
          <span class="point">✓ $0.12/M Tokens</span>
        </div>
      </div>
      <div class="signal signal-b">
        <p class="signal-label">Opus 4.7</p>
        <h3 class="signal-title">闭源</h3>
        <div class="signal-points">
          <span class="point">✓ SWE-Bench 62.1%</span>
          <span class="point">✓ 20万 Token</span>
          <span class="point">✓ $15/M Tokens</span>
        </div>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S02 · Comparison</span></div>
  </div>
</body>
</html>'''


def generate_s03():
    """S03 Data Layer / File Card — 数据层/文件卡片"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S03 Data Layer</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-columns:1fr 1fr}
    .left{padding:80px;display:flex;flex-direction:column;justify-content:center;border-right:1px solid var(--grey-2)}
    .right{padding:80px;display:flex;flex-direction:column;justify-content:center}
    .chrome-min{display:flex;justify-content:space-between;align-items:center;padding-bottom:16px;border-bottom:1px solid var(--grey-2);margin-bottom:32px}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .file-card{background:var(--grey-1);padding:40px}
    .file-type{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:48px;color:var(--accent);margin:0 0 24px}
    .file-name{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:600;font-size:28px;color:var(--ink);margin:0 0 32px}
    .file-props{display:flex;flex-direction:column;gap:16px}
    .prop{display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:16px}
    .prop-key{color:var(--grey-3)}
    .prop-val{color:var(--ink)}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="left">
      <div class="chrome-min">
        <span class="t-cat">S03 · Data Layer</span>
        <span class="t-meta">Model Card</span>
      </div>
      <div class="file-card">
        <p class="file-type">.model</p>
        <p class="file-name">MiniMax-M3</p>
        <div class="file-props">
          <div class="prop"><span class="prop-key">Parameters</span><span class="prop-val">12B MoE</span></div>
          <div class="prop"><span class="prop-key">Context</span><span class="prop-val">1,000,000</span></div>
          <div class="prop"><span class="prop-key">License</span><span class="prop-val">Apache 2.0</span></div>
          <div class="prop"><span class="prop-key">Modalities</span><span class="prop-val">Text, Image, Video</span></div>
        </div>
      </div>
    </div>
    <div class="right">
      <p class="t-cat">Capabilities</p>
      <div style="margin-top:32px;display:flex;flex-direction:column;gap:24px">
        <div style="font-family:'Inter',sans-serif;font-size:24px">Coding: <strong>59.0%</strong></div>
        <div style="font-family:'Inter',sans-serif;font-size:24px">Terminal: <strong>66.0%</strong></div>
        <div style="font-family:'Inter',sans-serif;font-size:24px">Multimodal: <strong>Yes</strong></div>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S03 · Data Layer</span></div>
  </div>
</body>
</html>'''


def generate_s04():
    """S04 Interface / Browser Mock — 界面/浏览器模型"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S04 Interface</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .browser{background:var(--paper);border:1px solid var(--grey-2);border-radius:8px;overflow:hidden;flex:1}
    .browser-bar{height:40px;background:var(--grey-1);border-bottom:1px solid var(--grey-2);display:flex;align-items:center;padding:0 16px;gap:8px}
    .dot{width:12px;height:12px;border-radius:50%}
    .dot-r{background:#f08080}
    .dot-y{background:#f5c450}
    .dot-g{background:#7ec98f}
    .browser-url{margin-left:16px;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3)}
    .browser-content{padding:40px;display:flex;flex-direction:column;gap:24px}
    .code-line{font-family:"IBM Plex Mono",monospace;font-size:18px;color:var(--ink);background:var(--grey-1);padding:12px 16px}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="browser">
      <div class="browser-bar">
        <span class="dot dot-r"></span>
        <span class="dot dot-y"></span>
        <span class="dot dot-g"></span>
        <span class="browser-url">minimax.io/blog/m3</span>
      </div>
      <div class="browser-content">
        <div class="code-line"># Install MiniMax M3</div>
        <div class="code-line">pip install minimax-m3</div>
        <div class="code-line"></div>
        <div class="code-line"># Generate code</div>
        <div class="code-line">from minimax import M3</div>
        <div class="code-line">model = M3.from_pretrained("m3-base")</div>
        <div class="code-line">result = model.generate("Write a Python function...")</div>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S04 · Interface</span></div>
  </div>
</body>
</html>'''


def generate_s05():
    """S05 Trap / Warning Rows — 陷阱/警告行"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="safety-orange">
<head>
  <meta charset="utf-8">
  <title>S05 Trap</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="safety-orange"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#FF6B35;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:80px 120px;display:flex;flex-direction:column}
    .chrome-min{display:flex;justify-content:space-between;align-items:center;padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:48px}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:72px;line-height:1.1;margin:0 0 48px;color:var(--ink)}
    .trap-list{display:flex;flex-direction:column;gap:0;flex:1}
    .trap-row{display:grid;grid-template-columns:200px 1fr;gap:32px;align-items:baseline;padding:28px 0;border-bottom:1px solid var(--grey-2)}
    .trap-row:last-child{border-bottom:0}
    .trap-label{font-family:"IBM Plex Mono",monospace;font-size:18px;color:var(--accent);font-weight:600}
    .trap-text{font-family:"Inter","Noto Sans SC",sans-serif;font-size:24px;color:var(--ink)}
    .issue-strip{position:absolute;bottom:80px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:20px}
  </style>
</head>
<body>
  <div class="card">
    <div class="chrome-min">
      <span class="t-cat">S05 · Trap</span>
      <span class="t-meta">Warning</span>
    </div>
    <h1 class="h-xl">使用M3的<br>常见陷阱</h1>
    <div class="trap-list">
      <div class="trap-row"><span class="trap-label">Trap 01</span><span class="trap-text">不要在没有测试的情况下直接部署</span></div>
      <div class="trap-row"><span class="trap-label">Trap 02</span><span class="trap-text">不要忽略长上下文的成本</span></div>
      <div class="trap-row"><span class="trap-label">Trap 03</span><span class="trap-text">不要期望所有任务都超越Opus</span></div>
      <div class="trap-row"><span class="trap-label">Trap 04</span><span class="trap-text">不要忘记开源模型需要更多调优</span></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S05 · Trap</span></div>
  </div>
</body>
</html>'''


def generate_s06():
    """S06 Pipeline / Architecture — 流水线/架构"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S06 Pipeline</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:56px;margin:0;color:var(--ink)}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    .pipeline{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;flex:1}
    .stage{background:var(--grey-1);padding:32px;display:flex;flex-direction:column}
    .stage-nb{font-family:"IBM Plex Mono",monospace;font-size:24px;color:var(--accent);margin:0 0 16px}
    .stage-title{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:600;font-size:28px;color:var(--ink);margin:0 0 12px}
    .stage-desc{font-family:"Inter","Noto Sans SC",sans-serif;font-size:18px;color:var(--grey-3);margin:0 0 24px}
    .stage-action{font-family:"IBM Plex Mono",monospace;font-size:16px;color:var(--accent);margin-top:auto;padding-top:16px;border-top:1px solid var(--grey-2)}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">M3 架构</h1>
      <span class="t-cat">Architecture</span>
    </div>
    <div class="pipeline">
      <div class="stage">
        <p class="stage-nb">01</p>
        <h3 class="stage-title">输入层</h3>
        <p class="stage-desc">文本、图像、视频多模态输入</p>
        <p class="stage-action">MSA 稀疏注意力</p>
      </div>
      <div class="stage">
        <p class="stage-nb">02</p>
        <h3 class="stage-title">处理层</h3>
        <p class="stage-desc">100万 Token 上下文处理</p>
        <p class="stage-action">MoE 混合专家</p>
      </div>
      <div class="stage">
        <p class="stage-nb">03</p>
        <h3 class="stage-title">输出层</h3>
        <p class="stage-desc">代码生成、推理、Agent</p>
        <p class="stage-action">思维模式切换</p>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S06 · Pipeline</span></div>
  </div>
</body>
</html>'''


def generate_s07():
    """S07 Takeaway Ledger — 收获账目"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S07 Takeaway</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--ink);position:relative;overflow:hidden;padding:80px 120px;display:flex;flex-direction:column}
    .chrome-min{display:flex;justify-content:space-between;align-items:center;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,.2);margin-bottom:48px}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.5);margin:0}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:200;font-size:72px;line-height:1.1;margin:0 0 48px;color:var(--paper)}
    .ledger{display:flex;flex-direction:column;gap:0;flex:1}
    .ledger-row{display:grid;grid-template-columns:120px 1fr;gap:32px;align-items:baseline;padding:28px 0;border-bottom:1px solid rgba(255,255,255,.2)}
    .ledger-row:last-child{border-bottom:0}
    .ledger-nb{font-family:"IBM Plex Mono",monospace;font-size:28px;color:var(--accent)}
    .ledger-text{font-family:"Inter","Noto Sans SC",sans-serif;font-size:28px;color:var(--paper)}
    .issue-strip{position:absolute;bottom:80px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:rgba(255,255,255,.4);border-top:1px solid rgba(255,255,255,.2);padding-top:20px}
  </style>
</head>
<body>
  <div class="card">
    <div class="chrome-min">
      <span class="t-cat">S07 · Takeaway</span>
      <span class="t-meta">Summary</span>
    </div>
    <h1 class="h-xl">三个关键收获</h1>
    <div class="ledger">
      <div class="ledger-row"><span class="ledger-nb">01</span><span class="ledger-text">开源模型已具备软件工程能力</span></div>
      <div class="ledger-row"><span class="ledger-nb">02</span><span class="ledger-text">价格战加速AI基础设施化</span></div>
      <div class="ledger-row"><span class="ledger-nb">03</span><span class="ledger-text">开发者是最大受益者</span></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S07 · Takeaway</span></div>
  </div>
</body>
</html>'''


def generate_s08():
    """S08 Image Hero — 图片主视觉"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S08 Image Hero</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;display:grid;grid-template-rows:auto 1fr auto}
    .chrome-min{padding:40px 80px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--grey-2)}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .hero{background:var(--ink);position:relative;min-height:400px}
    .hero-overlay{position:absolute;top:40px;left:40px;background:var(--paper);padding:32px;max-width:50%}
    .hero-title{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:600;font-size:36px;color:var(--ink);margin:0 0 8px}
    .hero-desc{font-family:"Inter","Noto Sans SC",sans-serif;font-size:18px;color:var(--grey-3);margin:0}
    .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
    .stat{padding:32px 80px;border-top:1px solid var(--grey-2);border-right:1px solid var(--grey-2)}
    .stat:last-child{border-right:0}
    .stat-num{font-family:"Inter",sans-serif;font-weight:200;font-size:72px;line-height:1;color:var(--ink);margin:0 0 8px}
    .stat-label{font-family:"IBM Plex Mono",monospace;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="chrome-min">
      <span class="t-cat">S08 · Image Hero</span>
      <span class="t-meta">2026.06</span>
    </div>
    <div class="hero">
      <div class="hero-overlay">
        <h3 class="hero-title">MiMo M3 开源发布</h3>
        <p class="hero-desc">性能接近 Opus 4.7，价格只有百分之一</p>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><p class="stat-num">59.0%</p><p class="stat-label">SWE-Bench</p></div>
      <div class="stat"><p class="stat-num">100万</p><p class="stat-label">Token</p></div>
      <div class="stat"><p class="stat-num">$0.12</p><p class="stat-label">Per M</p></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S08 · Image Hero</span></div>
  </div>
</body>
</html>'''


def generate_s09():
    """S09 KPI Tower — KPI塔"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S09 KPI Tower</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:80px 120px;display:flex;flex-direction:column}
    .chrome-min{display:flex;justify-content:space-between;align-items:center;padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:48px}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:64px;line-height:1.1;margin:0 0 48px;color:var(--ink)}
    .kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:48px;align-items:end;flex:1}
    .tower{display:flex;flex-direction:column;gap:16px;align-items:flex-start}
    .tower-num{font-family:"Inter",sans-serif;font-weight:200;font-size:88px;line-height:1;letter-spacing:-.02em;margin:0;color:var(--ink)}
    .tower-label{font-family:"IBM Plex Mono",monospace;font-size:18px;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .tower-bar{width:100%;background:var(--accent)}
    .tower.muted .tower-bar{background:var(--grey-2)}
    .tower.muted .tower-num{color:var(--grey-3)}
    .issue-strip{position:absolute;bottom:80px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:20px}
  </style>
</head>
<body>
  <div class="card">
    <div class="chrome-min">
      <span class="t-cat">S09 · KPI Tower</span>
      <span class="t-meta">Data</span>
    </div>
    <h1 class="h-xl">一组数字看懂 M3</h1>
    <div class="kpi-row">
      <div class="tower"><p class="tower-num">59.0%</p><p class="tower-label">SWE-Bench</p><div class="tower-bar" style="height:240px"></div></div>
      <div class="tower"><p class="tower-num">100万</p><p class="tower-label">Token</p><div class="tower-bar" style="height:200px"></div></div>
      <div class="tower"><p class="tower-num">9.4×</p><p class="tower-label">加速</p><div class="tower-bar" style="height:180px"></div></div>
      <div class="tower muted"><p class="tower-num">$0.12</p><p class="tower-label">价格</p><div class="tower-bar" style="height:160px"></div></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S09 · KPI Tower</span></div>
  </div>
</body>
</html>'''


def generate_s10():
    """S10 H-Bar Chart — 水平条形图"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S10 H-Bar</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:56px;margin:0;color:var(--ink)}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    .chart{display:flex;flex-direction:column;gap:24px;flex:1}
    .bar-row{display:grid;grid-template-columns:200px 1fr 100px;gap:24px;align-items:center}
    .bar-label{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:500;font-size:22px;color:var(--ink)}
    .bar-track{height:32px;background:var(--grey-1);position:relative}
    .bar-fill{position:absolute;left:0;top:0;bottom:0;background:var(--accent)}
    .bar-val{font-family:"IBM Plex Mono",monospace;font-size:22px;text-align:right;color:var(--ink)}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">模型能力排名</h1>
      <span class="t-cat">Ranking</span>
    </div>
    <div class="chart">
      <div class="bar-row"><span class="bar-label">Opus 4.7</span><div class="bar-track"><div class="bar-fill" style="width:100%"></div></div><span class="bar-val">62.1%</span></div>
      <div class="bar-row"><span class="bar-label">MiMo M3</span><div class="bar-track"><div class="bar-fill" style="width:95%"></div></div><span class="bar-val">59.0%</span></div>
      <div class="bar-row"><span class="bar-label">GPT-5.5</span><div class="bar-track"><div class="bar-fill" style="width:93%"></div></div><span class="bar-val">58.2%</span></div>
      <div class="bar-row"><span class="bar-label">Gemini 3.1</span><div class="bar-track"><div class="bar-fill" style="width:90%"></div></div><span class="bar-val">56.8%</span></div>
      <div class="bar-row"><span class="bar-label">DeepSeek V4</span><div class="bar-track"><div class="bar-fill" style="width:85%"></div></div><span class="bar-val">53.4%</span></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S10 · H-Bar</span></div>
  </div>
</body>
</html>'''


def generate_s11():
    """S11 Stacked Ledger — 堆叠账目"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S11 Stacked Ledger</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:80px 120px;display:flex;flex-direction:column}
    .chrome-min{display:flex;justify-content:space-between;align-items:center;padding-bottom:20px;border-bottom:1px solid var(--grey-2);margin-bottom:48px}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
    .t-meta{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey-3);margin:0}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:64px;line-height:1.1;margin:0 0 48px;color:var(--ink)}
    .ledger{display:flex;flex-direction:column;gap:0;flex:1}
    .ledger-row{display:grid;grid-template-columns:120px 1fr 80px;gap:32px;align-items:center;padding:28px 0;border-bottom:1px solid var(--grey-2)}
    .ledger-row:last-child{border-bottom:0}
    .ledger-num{font-family:"Inter",sans-serif;font-weight:200;font-size:72px;line-height:1;color:var(--ink)}
    .ledger-text{font-family:"Inter","Noto Sans SC",sans-serif;font-size:28px;color:var(--ink)}
    .ledger-icon{width:56px;height:56px;color:var(--accent)}
    .issue-strip{position:absolute;bottom:80px;left:120px;right:120px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:20px}
  </style>
</head>
<body>
  <div class="card">
    <div class="chrome-min">
      <span class="t-cat">S11 · Stacked Ledger</span>
      <span class="t-meta">Capabilities</span>
    </div>
    <h1 class="h-xl">M3 核心能力</h1>
    <div class="ledger">
      <div class="ledger-row"><span class="ledger-num">59%</span><span class="ledger-text">SWE-Bench Pro 编程能力</span><svg class="ledger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 18l6-6-6-6"/><path d="M8 6l-6 6 6 6"/></svg></div>
      <div class="ledger-row"><span class="ledger-num">100万</span><span class="ledger-text">Token 上下文窗口</span><svg class="ledger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg></div>
      <div class="ledger-row"><span class="ledger-num">9.4×</span><span class="ledger-text">CUDA 优化加速</span><svg class="ledger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
      <div class="ledger-row"><span class="ledger-num">$0.12</span><span class="ledger-text">每百万 Token 价格</span><svg class="ledger-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M8 10h8"/></svg></div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S11 · Stacked Ledger</span></div>
  </div>
</body>
</html>'''


def generate_s12():
    """S12 Matrix + Hero Stat — 矩阵+主数据"""
    return '''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>S12 Matrix</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Noto+Sans+SC:wght@200;300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
  <style>
    :root,[data-accent="ikb"]{--paper:#fafaf8;--ink:#0a0a0a;--grey-1:#f0f0ee;--grey-2:#d4d4d2;--grey-3:#737373;--accent:#002FA7;--accent-on:#ffffff}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#1a1a1a;padding:32px}
    .card{width:1920px;height:1080px;background:var(--paper);position:relative;overflow:hidden;padding:60px 80px;display:flex;flex-direction:column}
    .header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:32px}
    .h-xl{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:300;font-size:48px;margin:0;color:var(--ink)}
    .t-cat{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    .matrix{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;flex:1;margin-bottom:32px}
    .cell{background:var(--grey-1);padding:24px;display:flex;flex-direction:column;gap:8px}
    .cell-nb{font-family:"IBM Plex Mono",monospace;font-size:16px;color:var(--grey-3)}
    .cell-title{font-family:"Inter","Noto Sans SC",sans-serif;font-weight:500;font-size:22px;color:var(--ink)}
    .cell.is-accent{background:var(--accent);color:var(--accent-on)}
    .cell.is-accent .cell-nb,.cell.is-accent .cell-title{color:var(--accent-on)}
    .hero-stat{display:flex;justify-content:space-between;align-items:end;padding-top:32px;border-top:1px solid var(--grey-2)}
    .hero-kick{font-family:"IBM Plex Mono",monospace;font-size:16px;color:var(--grey-3);margin:0 0 8px}
    .hero-text{font-family:"Inter","Noto Sans SC",sans-serif;font-size:24px;color:var(--ink);margin:0}
    .hero-num{font-family:"Inter",sans-serif;font-weight:200;font-size:168px;line-height:1;color:var(--accent)}
    .issue-strip{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--grey-3);border-top:1px solid var(--grey-2);padding-top:16px}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1 class="h-xl">M3 能力矩阵</h1>
      <span class="t-cat">Matrix</span>
    </div>
    <div class="matrix">
      <div class="cell"><span class="cell-nb">01</span><span class="cell-title">编程</span></div>
      <div class="cell is-accent"><span class="cell-nb">02</span><span class="cell-title">推理</span></div>
      <div class="cell"><span class="cell-nb">03</span><span class="cell-title">多模态</span></div>
      <div class="cell"><span class="cell-nb">04</span><span class="cell-title">Agent</span></div>
      <div class="cell"><span class="cell-nb">05</span><span class="cell-title">长上下文</span></div>
      <div class="cell"><span class="cell-nb">06</span><span class="cell-title">工具使用</span></div>
      <div class="cell"><span class="cell-nb">07</span><span class="cell-title">代码理解</span></div>
      <div class="cell"><span class="cell-nb">08</span><span class="cell-title">CUDA优化</span></div>
    </div>
    <div class="hero-stat">
      <div>
        <p class="hero-kick">Total Coverage</p>
        <p class="hero-text">覆盖 8 大核心能力领域</p>
      </div>
      <span class="hero-num">8</span>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>S12 · Matrix</span></div>
  </div>
</body>
</html>'''


# 版式映射
LAYOUT_MAP = {
    "M01": generate_m01,
    "M02": generate_m02,
    "M03": generate_m03,
    "M04": generate_m04,
    "M05": generate_m05,
    "M06": generate_m06,
    "M07": generate_m07,
    "M08": generate_m08,
    "M09": generate_m09,
    "M10": generate_m10,
    "M11": generate_m11,
    "M12": generate_m12,
    "M13": generate_m13,
    "M14": generate_m14,
    "M15": generate_m15,
    "M16": generate_m16,
    "S01": generate_s01,
    "S02": generate_s02,
    "S03": generate_s03,
    "S04": generate_s04,
    "S05": generate_s05,
    "S06": generate_s06,
    "S07": generate_s07,
    "S08": generate_s08,
    "S09": generate_s09,
    "S10": generate_s10,
    "S11": generate_s11,
    "S12": generate_s12,
}


def main():
    """生成所有 28 个版式骨架的布局示例"""
    output_dir = Path("layout_samples")
    output_dir.mkdir(exist_ok=True)

    print("正在生成 28 个版式骨架的布局示例...")
    print()

    for i, (layout_id, generator) in enumerate(LAYOUT_MAP.items(), 1):
        print(f"[{i:02d}/28] 生成 {layout_id}...")

        # 生成 HTML
        html_content = generator()
        html_file = output_dir / f"{layout_id}.html"
        html_file.write_text(html_content, encoding='utf-8')

    print()
    print("✨ HTML 文件生成完成！")
    print(f"📁 保存位置: {output_dir}")
    print()
    print("正在渲染为 PNG...")

    # 渲染为 PNG
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, (layout_id, generator) in enumerate(LAYOUT_MAP.items(), 1):
            html_file = output_dir / f"{layout_id}.html"
            png_file = output_dir / f"{layout_id}.png"

            print(f"[{i:02d}/28] 渲染 {layout_id}...")

            # 读取 HTML 获取尺寸
            html_content = html_file.read_text(encoding='utf-8')
            if 'width: 1920px' in html_content:
                width, height = 1920, 1080
            else:
                width, height = 1080, 1440

            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=2
            )
            page = context.new_page()
            page.goto(f"file:///{html_file.resolve().as_posix()}")
            page.wait_for_timeout(1500)

            card = page.query_selector('.card')
            if card:
                card.screenshot(path=str(png_file))

            page.close()
            context.close()

        browser.close()

    print()
    print("✨ 布局示例生成完成！")
    print(f"📁 保存位置: {output_dir}")
    print()
    print("生成的文件:")
    for f in sorted(output_dir.glob("*.png")):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
