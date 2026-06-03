#!/usr/bin/env python3
"""
小红书套图生成器 - Editorial 风格 + 靛蓝瓷主题
基于 guizang-social-card-skill 的设计规范
"""

import sys
import io
from pathlib import Path

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 靛蓝瓷主题颜色
INDIGO_PORCELAIN = {
    "paper": "#f2f4f5",
    "paper-2": "#e5ebef",
    "ink": "#0a1f3d",
    "muted": "#5f6d78",
    "line": "rgba(10,31,61,.20)",
    "accent": "#315d93",
    "accent-soft": "#d7e1ec",
}


def generate_m01_cover():
    """M01 杂志封面 - 小红书封面"""
    return f'''<!doctype html>
<html lang="zh-CN" data-theme="indigo-porcelain">
<head>
  <meta charset="utf-8">
  <title>M01 Cover</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,[data-theme="indigo-porcelain"]{{
      --paper:#f2f4f5;--paper-2:#e5ebef;--ink:#0a1f3d;--muted:#5f6d78;
      --line:rgba(10,31,61,.20);--accent:#315d93;--accent-soft:#d7e1ec;
    }}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#1a1a1a;padding:32px}}
    .card{{
      width:1080px;height:1440px;background:var(--paper);position:relative;
      overflow:hidden;padding:96px 88px;display:flex;flex-direction:column;
    }}
    .grain{{
      position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
      background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);
      background-size:3px 3px;
    }}
    .issue-row{{
      display:flex;align-items:center;gap:16px;
      font-family:"IBM Plex Mono",monospace;font-size:18px;
      letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
      margin-bottom:48px;
    }}
    .issue-row .dot{{width:6px;height:6px;border-radius:50%;background:var(--accent)}}
    .h-display{{
      font-family:"Noto Serif SC",serif;font-weight:500;font-size:124px;
      line-height:1.06;letter-spacing:.04em;margin:0 0 32px;color:var(--ink);
    }}
    .h-sub{{
      font-family:"Playfair Display",serif;font-style:italic;font-weight:400;
      font-size:36px;color:var(--muted);margin:0 0 48px;
    }}
    .hero-img{{
      width:100%;aspect-ratio:16/10;background:var(--ink);
      margin-bottom:48px;position:relative;overflow:hidden;
    }}
    .hero-img::after{{
      content:'';position:absolute;inset:0;
      background:linear-gradient(180deg,transparent 60%,rgba(10,31,61,.3));
    }}
    .lead{{
      font-family:"Noto Serif SC",serif;font-weight:400;font-size:28px;
      line-height:1.55;color:rgba(10,31,61,.82);margin:0 0 32px;
    }}
    .points{{
      display:flex;flex-direction:column;gap:16px;margin-top:auto;
    }}
    .point{{
      display:flex;align-items:baseline;gap:16px;
      font-family:"Noto Serif SC",serif;font-size:22px;line-height:1.5;
    }}
    .point-nb{{
      font-family:"IBM Plex Mono",monospace;font-size:18px;
      color:var(--muted);min-width:32px;
    }}
    .issue-strip{{
      position:absolute;bottom:56px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:"IBM Plex Mono",monospace;font-size:16px;
      letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
      border-top:1px solid var(--line);padding-top:18px;
    }}
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


def generate_m04_quote():
    """M04 引文/论点 - 核心观点"""
    return f'''<!doctype html>
<html lang="zh-CN" data-theme="indigo-porcelain">
<head>
  <meta charset="utf-8">
  <title>M04 Pull Quote</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=Playfair+Display:ital,wght@0,400;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,[data-theme="indigo-porcelain"]{{
      --paper:#f2f4f5;--paper-2:#e5ebef;--ink:#0a1f3d;--muted:#5f6d78;
      --line:rgba(10,31,61,.20);--accent:#315d93;--accent-soft:#d7e1ec;
    }}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#1a1a1a;padding:32px}}
    .card{{
      width:1080px;height:1440px;background:var(--paper);position:relative;
      overflow:hidden;padding:96px 88px;display:flex;flex-direction:column;
      justify-content:center;align-items:center;
    }}
    .grain{{
      position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
      background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);
      background-size:3px 3px;
    }}
    .quote-mark{{
      font-family:"Playfair Display",serif;font-size:120px;line-height:1;
      color:var(--muted);opacity:.4;margin-bottom:32px;
    }}
    .quote{{
      font-family:"Noto Serif SC",serif;font-weight:500;font-size:72px;
      line-height:1.3;text-align:center;color:var(--ink);margin:0 0 48px;
    }}
    .source{{
      font-family:"IBM Plex Mono",monospace;font-size:18px;
      letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
      margin:0 0 16px;
    }}
    .context{{
      font-family:"Noto Serif SC",serif;font-size:20px;color:var(--muted);
      text-align:center;max-width:800px;
    }}
    .issue-strip{{
      position:absolute;bottom:56px;left:120px;right:120px;
      display:flex;justify-content:space-between;
      font-family:"IBM Plex Mono",monospace;font-size:14px;
      color:var(--muted);border-top:1px solid var(--line);padding-top:18px;
    }}
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


def generate_m08_ledger():
    """M08 高账目表 - 核心数据对比"""
    return f'''<!doctype html>
<html lang="zh-CN" data-theme="indigo-porcelain">
<head>
  <meta charset="utf-8">
  <title>M08 Tall Ledger</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,[data-theme="indigo-porcelain"]{{
      --paper:#f2f4f5;--paper-2:#e5ebef;--ink:#0a1f3d;--muted:#5f6d78;
      --line:rgba(10,31,61,.20);--accent:#315d93;--accent-soft:#d7e1ec;
    }}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#1a1a1a;padding:32px}}
    .card{{
      width:1080px;height:1440px;background:var(--paper);position:relative;
      overflow:hidden;padding:96px 88px;display:flex;flex-direction:column;
    }}
    .grain{{
      position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
      background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);
      background-size:3px 3px;
    }}
    .header{{
      display:flex;justify-content:space-between;align-items:baseline;
      margin-bottom:48px;
    }}
    .h-xl{{
      font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;
      margin:0;color:var(--ink);
    }}
    .kicker{{
      font-family:"IBM Plex Mono",monospace;font-size:14px;
      letter-spacing:.2em;text-transform:uppercase;color:var(--muted);
    }}
    .ledger{{
      display:flex;flex-direction:column;flex:1;
    }}
    .ledger-row{{
      display:grid;grid-template-columns:120px 1fr 200px;gap:32px;
      align-items:baseline;padding:28px 0;border-bottom:1px solid var(--line);
    }}
    .ledger-row:last-child{{border-bottom:0}}
    .ledger-idx{{
      font-family:"IBM Plex Mono",monospace;font-size:20px;color:var(--muted);
    }}
    .ledger-title{{
      font-family:"Noto Serif SC",serif;font-weight:500;font-size:32px;
      color:var(--ink);
    }}
    .ledger-note{{
      font-family:"Noto Serif SC",serif;font-weight:400;font-size:20px;
      color:var(--muted);text-align:right;
    }}
    .issue-strip{{
      position:absolute;bottom:56px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:"IBM Plex Mono",monospace;font-size:14px;
      color:var(--muted);border-top:1px solid var(--line);padding-top:18px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <div class="header">
      <h1 class="h-xl">M3 vs 竞品对比</h1>
      <span class="kicker">Comparison</span>
    </div>
    <div class="ledger">
      <div class="ledger-row">
        <span class="ledger-idx">01</span>
        <span class="ledger-title">SWE-Bench Pro</span>
        <span class="ledger-note">59.0% vs 62.1%</span>
      </div>
      <div class="ledger-row">
        <span class="ledger-idx">02</span>
        <span class="ledger-title">Terminal-Bench</span>
        <span class="ledger-note">66.0% vs 68.5%</span>
      </div>
      <div class="ledger-row">
        <span class="ledger-idx">03</span>
        <span class="ledger-title">上下文长度</span>
        <span class="ledger-note">100万 vs 20万</span>
      </div>
      <div class="ledger-row">
        <span class="ledger-idx">04</span>
        <span class="ledger-title">价格</span>
        <span class="ledger-note">$0.12 vs $15</span>
      </div>
      <div class="ledger-row">
        <span class="ledger-idx">05</span>
        <span class="ledger-title">开源程度</span>
        <span class="ledger-note">完全开源 vs 闭源</span>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M08 · Tall Ledger</span></div>
  </div>
</body>
</html>'''


def generate_m05_checklist():
    """M05 清单 - 核心特性"""
    return f'''<!doctype html>
<html lang="zh-CN" data-theme="indigo-porcelain">
<head>
  <meta charset="utf-8">
  <title>M05 Checklist</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,[data-theme="indigo-porcelain"]{{
      --paper:#f2f4f5;--paper-2:#e5ebef;--ink:#0a1f3d;--muted:#5f6d78;
      --line:rgba(10,31,61,.20);--accent:#315d93;--accent-soft:#d7e1ec;
    }}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#1a1a1a;padding:32px}}
    .card{{
      width:1080px;height:1440px;background:var(--paper);position:relative;
      overflow:hidden;padding:96px 88px;display:flex;flex-direction:column;
    }}
    .grain{{
      position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
      background-image:radial-gradient(rgba(0,0,0,.045) 1px,transparent 1px);
      background-size:3px 3px;
    }}
    .kicker{{
      font-family:"IBM Plex Mono",monospace;font-size:16px;
      letter-spacing:.2em;text-transform:uppercase;color:var(--muted);
      margin:0 0 24px;
    }}
    .h-xl{{
      font-family:"Noto Serif SC",serif;font-weight:700;font-size:56px;
      line-height:1.1;margin:0 0 48px;color:var(--ink);
    }}
    .checklist{{
      display:flex;flex-direction:column;gap:0;flex:1;
    }}
    .check-row{{
      display:grid;grid-template-columns:60px 1fr auto;gap:24px;
      align-items:baseline;padding:28px 0;border-bottom:1px solid var(--line);
    }}
    .check-row:last-child{{border-bottom:0}}
    .check-nb{{
      font-family:"IBM Plex Mono",monospace;font-size:24px;color:var(--accent);
    }}
    .check-item{{
      font-family:"Noto Serif SC",serif;font-weight:500;font-size:28px;
      color:var(--ink);
    }}
    .check-desc{{
      font-family:"Noto Serif SC",serif;font-size:18px;color:var(--muted);
      margin-top:8px;
    }}
    .issue-strip{{
      position:absolute;bottom:56px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:"IBM Plex Mono",monospace;font-size:14px;
      color:var(--muted);border-top:1px solid var(--line);padding-top:18px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="grain"></div>
    <p class="kicker">Features</p>
    <h1 class="h-xl">M3 的五大核心特性</h1>
    <div class="checklist">
      <div class="check-row">
        <span class="check-nb">01</span>
        <div>
          <span class="check-item">MSA 稀疏注意力</span>
          <p class="check-desc">每 Token 计算量降至前代的 1/20</p>
        </div>
      </div>
      <div class="check-row">
        <span class="check-nb">02</span>
        <div>
          <span class="check-item">100 万 Token 上下文</span>
          <p class="check-desc">可处理整本技术文档、大型代码仓库</p>
        </div>
      </div>
      <div class="check-row">
        <span class="check-nb">03</span>
        <div>
          <span class="check-item">原生多模态</span>
          <p class="check-desc">支持图像和视频输入，可操控桌面</p>
        </div>
      </div>
      <div class="check-row">
        <span class="check-nb">04</span>
        <div>
          <span class="check-item">思维模式开关</span>
          <p class="check-desc">复杂任务开启，低延迟场景关闭</p>
        </div>
      </div>
      <div class="check-row">
        <span class="check-nb">05</span>
        <div>
          <span class="check-item">全面开源</span>
          <p class="check-desc">模型权重、技术报告、训练框架全部开源</p>
        </div>
      </div>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M05 · Checklist</span></div>
  </div>
</body>
</html>'''


def generate_m07_closing():
    """M07 收尾笔记 - 总结"""
    return f'''<!doctype html>
<html lang="zh-CN" data-theme="indigo-porcelain">
<head>
  <meta charset="utf-8">
  <title>M07 Closing Note</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,[data-theme="indigo-porcelain"]{{
      --paper:#f2f4f5;--paper-2:#e5ebef;--ink:#0a1f3d;--muted:#5f6d78;
      --line:rgba(10,31,61,.20);--accent:#315d93;--accent-soft:#d7e1ec;
    }}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#1a1a1a;padding:32px}}
    .card{{
      width:1080px;height:1440px;background:var(--ink);position:relative;
      overflow:hidden;padding:96px 88px;display:flex;flex-direction:column;
    }}
    .h-xl{{
      font-family:"Noto Serif SC",serif;font-weight:700;font-size:48px;
      line-height:1.2;margin:0 0 48px;color:var(--paper);
    }}
    .ledger{{
      display:flex;flex-direction:column;flex:1;
    }}
    .ledger-row{{
      display:grid;grid-template-columns:80px 1fr;gap:24px;
      align-items:baseline;padding:32px 0;
      border-bottom:1px solid rgba(242,244,245,.2);
    }}
    .ledger-row:last-child{{border-bottom:0}}
    .ledger-nb{{
      font-family:"IBM Plex Mono",monospace;font-size:28px;color:var(--accent);
    }}
    .ledger-title{{
      font-family:"Noto Serif SC",serif;font-weight:500;font-size:32px;
      color:var(--paper);
    }}
    .ledger-desc{{
      font-family:"Noto Serif SC",serif;font-size:20px;
      color:rgba(242,244,245,.7);margin-top:8px;
    }}
    .closing{{
      margin-top:auto;padding-top:32px;
      border-top:1px solid rgba(242,244,245,.2);
    }}
    .closing-text{{
      font-family:"Noto Serif SC",serif;font-style:italic;font-size:24px;
      color:rgba(242,244,245,.6);
    }}
    .issue-strip{{
      position:absolute;bottom:56px;left:88px;right:88px;
      display:flex;justify-content:space-between;
      font-family:"IBM Plex Mono",monospace;font-size:14px;
      color:rgba(242,244,245,.4);
      border-top:1px solid rgba(242,244,245,.2);padding-top:18px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1 class="h-xl">三个关键结论</h1>
    <div class="ledger">
      <div class="ledger-row">
        <span class="ledger-nb">01</span>
        <div>
          <span class="ledger-title">开源模型已具备软件工程能力</span>
          <p class="ledger-desc">M3 在 SWE-Bench Pro 上的 59.0% 得分证明了这一点</p>
        </div>
      </div>
      <div class="ledger-row">
        <span class="ledger-nb">02</span>
        <div>
          <span class="ledger-title">价格战加速 AI 基础设施化</span>
          <p class="ledger-desc">$0.12/M tokens，AI 正在变得越来越便宜</p>
        </div>
      </div>
      <div class="ledger-row">
        <span class="ledger-nb">03</span>
        <div>
          <span class="ledger-title">开发者是最大受益者</span>
          <p class="ledger-desc">更多选择，更低成本，更强能力</p>
        </div>
      </div>
    </div>
    <div class="closing">
      <p class="closing-text">技术的进步最终会让所有人受益。</p>
    </div>
    <div class="issue-strip"><span>AI创享派</span><span>M07 · Closing Note</span></div>
  </div>
</body>
</html>'''


def render_card_to_png(html_content: str, output_file: Path) -> bool:
    """将 HTML 渲染为 PNG"""
    from playwright.sync_api import sync_playwright

    temp_html = Path("temp_card.html")
    temp_html.write_text(html_content, encoding='utf-8')

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={"width": 1080, "height": 1440},
                device_scale_factor=2
            )
            page = context.new_page()
            page.goto(f"file:///{temp_html.resolve().as_posix()}")
            page.wait_for_timeout(2000)

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


def main():
    """生成小红书套图"""
    output_dir = Path("covers/2026-06-02_minimax-m3/editorial")
    output_dir.mkdir(parents=True, exist_ok=True)

    cards = [
        ("01-cover", generate_m01_cover()),
        ("04-quote", generate_m04_quote()),
        ("08-ledger", generate_m08_ledger()),
        ("05-checklist", generate_m05_checklist()),
        ("07-closing", generate_m07_closing()),
    ]

    print("正在生成靛蓝瓷 Editorial 风格小红书套图...")
    print()

    for i, (name, html_content) in enumerate(cards, 1):
        print(f"[{i}/5] 正在生成 {name}...")
        output_file = output_dir / f"xhs-{name}.png"

        if render_card_to_png(html_content, output_file):
            print(f"  ✅ 已生成: {output_file.name}")
        else:
            print(f"  ❌ 生成失败")

    print()
    print("✨ 小红书套图生成完成！")
    print(f"📁 保存位置: {output_dir}")


if __name__ == "__main__":
    main()
