#!/usr/bin/env python3
"""
生成 28 个版式骨架的参考图
"""

import sys
import io
from pathlib import Path

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 版式骨架定义
LAYOUT_RECIPES = [
    # Editorial Magazine × E-ink 系列（M系列）
    {
        "id": "M01",
        "name": "Cover — 杂志封面",
        "type": "Editorial",
        "scene": "小红书首页、竖版社交卡片、文章封面",
        "structure": "顶部期号栏 → 大号衬线标题 → 占页面35%-55%的大图 → 底部3-5个要点条带"
    },
    {
        "id": "M02",
        "name": "Field Note Photo — 田野笔记照片",
        "type": "Editorial",
        "scene": "户外、实物、硬件、真实世界观察记录",
        "structure": "大幅纪实照片 → 窄幅说明列或底部说明带 → 大字短要点"
    },
    {
        "id": "M03",
        "name": "Editorial Essay Split — 编辑分栏随笔",
        "type": "Editorial",
        "scene": "用细节阐释单一观点",
        "structure": "左侧大标题或引文 → 右侧2-3短段或编号片段 → 栏间细线分隔"
    },
    {
        "id": "M04",
        "name": "Pull Quote / Thesis — 引文/论点",
        "type": "Editorial",
        "scene": "核心句子或结论展示",
        "structure": "跨页大引文 → 小字来源/上下文行 → 可选小注释或期号标记"
    },
    {
        "id": "M05",
        "name": "Checklist / Buying Guide — 清单/选购指南",
        "type": "Editorial",
        "scene": "小红书实用内容",
        "structure": "标题头 → 4-6行（每行含编号、条目、结果说明）→ 可选小图或材质色块"
    },
    {
        "id": "M06",
        "name": "Evidence Wall — 证据墙",
        "type": "Editorial",
        "scene": "多张截图、参考文献或小图",
        "structure": "2×2或3列图片网格 → 每图配短说明 → 一个较大标题锚定解读"
    },
    {
        "id": "M07",
        "name": "Closing Note — 收尾笔记",
        "type": "Editorial",
        "scene": "末页",
        "structure": "大标题 → 4-6条账目项 → 收尾块（引文/签名/价格/CTA/旁注任选一）→ 小字页脚标签"
    },
    {
        "id": "M08",
        "name": "Tall Ledger — 高账目表",
        "type": "Editorial",
        "scene": "列表、角色、优劣对比、装备项、产品能力",
        "structure": "标题头 → 4-6全宽行 → 左侧索引/旁注列，右侧标题+结果说明"
    },
    {
        "id": "M09",
        "name": "Atmospheric Thesis — 氛围论点",
        "type": "Editorial",
        "scene": "稀疏但重要的观点",
        "structure": "WebGL/墨流背景 → 大号论点或引文 → 1-2条支撑注释 → 小字期号元数据"
    },
    {
        "id": "M10",
        "name": "Evidence Feature — 证据专题",
        "type": "Editorial",
        "scene": "提供的截图/照片",
        "structure": "占垂直画布45%-65%的大图 → 标题和导语在上方或旁边 → 底部说明带含2-3个要点"
    },
    {
        "id": "M11",
        "name": "Marginalia Essay — 旁注随笔",
        "type": "Editorial",
        "scene": "中等文字量的细致解释",
        "structure": "宽编辑标题 → 主栏2-3段 → 窄旁注栏（关键词/引文片段/小图裁剪）→ 栏间竖向细线"
    },
    {
        "id": "M12",
        "name": "Section Divider — 章节分隔页",
        "type": "Editorial",
        "scene": "多页集中密集页面间的呼吸",
        "structure": "WebGL墨流背景 → 单行mono踢脚线 → 大号衬线章节标题 → 短副标题"
    },
    {
        "id": "M13",
        "name": "Hero Question — 核心问题",
        "type": "Editorial",
        "scene": "小红书多页集的最后一页",
        "structure": "WebGL墨流背景 → 安静踢脚线 → 大号衬线问题 → 单句提示引导评论"
    },
    {
        "id": "M14",
        "name": "Vertical Pipeline — 竖向流水线",
        "type": "Editorial",
        "scene": "3-5步工作流、决策树、配方",
        "structure": "踢脚线+大标题 → 3-5个步骤行 → 步骤间细线"
    },
    {
        "id": "M15",
        "name": "Before / After — 前后对比",
        "type": "Editorial",
        "scene": "旧方式vs新方式、AI前vs AI后",
        "structure": "踢脚线+大标题 → 两个对比块（Before块淡化，After块正常）→ 每块含独立要点"
    },
    {
        "id": "M16",
        "name": "Image-Led Cover — 图片主导封面",
        "type": "Editorial",
        "scene": "生活方式、图片密集内容",
        "structure": "照片铺满画布 → 标题以克制方式覆盖其上"
    },
    # Swiss International 系列（S系列）
    {
        "id": "S01",
        "name": "Accent Cover — 强调色封面",
        "type": "Swiss",
        "scene": "小红书封面",
        "structure": "全强调色或米白背景 → 大号轻量标题 → 简洁抽象系统块 → 底部元数据条带"
    },
    {
        "id": "S02",
        "name": "Two Signals / Comparison — 双信号/对比",
        "type": "Swiss",
        "scene": "两个来源、两个选项或两个产品方向的对比",
        "structure": "页面标题 → 两个大矩形模块 → 各自下方短注"
    },
    {
        "id": "S03",
        "name": "Data Layer / File Card — 数据层/文件卡片",
        "type": "Swiss",
        "scene": "Markdown、内存、数据源、数据库或状态展示",
        "structure": "大型文件类型或对象块 → 3-4属性列表 → 粗mono标签"
    },
    {
        "id": "S04",
        "name": "Interface / Browser Mock — 界面/浏览器模型",
        "type": "Swiss",
        "scene": "HTML、UI、演示、交互或输出层",
        "structure": "直边浏览器窗口框架 → 内含一个主内容块+2-3功能模块"
    },
    {
        "id": "S05",
        "name": "Trap / Warning Rows — 陷阱/警告行",
        "type": "Swiss",
        "scene": "问题、反模式和不要这样做的页面",
        "structure": "大警告标题 → 三横行 → 左mono标签，右结果说明"
    },
    {
        "id": "S06",
        "name": "Pipeline / Architecture — 流水线/架构",
        "type": "Swiss",
        "scene": "工作流和分层系统",
        "structure": "三行或三列 → 每个含编号、标签、动作和结果 → 细线框和中性灰填充"
    },
    {
        "id": "S07",
        "name": "Takeaway Ledger — 收获账目",
        "type": "Swiss",
        "scene": "末页",
        "structure": "大论点标题 → 三行账目 → 深色/墨色背景可创造收束感"
    },
    {
        "id": "S08",
        "name": "Image Hero — 图片主视觉",
        "type": "Swiss",
        "scene": "微信21:9主封面及小红书封面",
        "structure": "顶部单行分类+日期 → 图片网格 → 底部3个统计块"
    },
    {
        "id": "S09",
        "name": "KPI Tower — KPI塔",
        "type": "Swiss",
        "scene": "产品更新、发布说明、流量仪表盘",
        "structure": "踢脚线+大标题 → 4个塔列 → 一列可带muted修饰作为基线对比"
    },
    {
        "id": "S10",
        "name": "H-Bar Chart — 水平条形图",
        "type": "Swiss",
        "scene": "排名、5-10项对比、Top N列表",
        "structure": "踢脚线+大标题 → 5-10条水平条形行"
    },
    {
        "id": "S11",
        "name": "Stacked Ledger — 堆叠账目",
        "type": "Swiss",
        "scene": "购物清单、支出汇总、Agent能力清单",
        "structure": "踢脚线+大标题 → 4-6条账目行"
    },
    {
        "id": "S12",
        "name": "Matrix + Hero Stat — 矩阵+主数据",
        "type": "Swiss",
        "scene": "能力矩阵、Agent清单",
        "structure": "踢脚线+大标题 → 8-12格矩阵 → 底部统计区"
    }
]


def generate_layout_html(recipe: dict) -> str:
    """为每个版式生成参考 HTML"""
    layout_id = recipe["id"]
    name = recipe["name"]
    scene = recipe["scene"]
    structure = recipe["structure"]
    layout_type = recipe["type"]

    if layout_type == "Editorial":
        return generate_editorial_html(recipe)
    else:
        return generate_swiss_html(recipe)


def generate_editorial_html(recipe: dict) -> str:
    """生成 Editorial 风格参考图"""
    layout_id = recipe["id"]
    name = recipe["name"]
    scene = recipe["scene"]
    structure = recipe["structure"]

    return f'''<!doctype html>
<html lang="zh-CN" data-theme="ink-classic">
<head>
  <meta charset="utf-8">
  <title>{layout_id} - {name}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
  <style>
    :root,
    [data-theme="ink-classic"] {{
      --paper: #f3f0e8;
      --paper-2: #ebe6da;
      --ink: #0a0a0b;
      --muted: #68625a;
      --line: rgba(10,10,11,.22);
      --accent: #111111;
      --accent-soft: #d8d2c6;
    }}
    :root {{
      --serif-zh: "Noto Serif SC", "Songti SC", serif;
      --serif-en: "Playfair Display", serif;
      --sans-zh: "Noto Sans SC", sans-serif;
      --sans-en: "Inter", sans-serif;
      --mono: "IBM Plex Mono", monospace;
    }}
    *,*::before,*::after {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      background: #1a1a1a;
      font-family: var(--sans-zh);
      color: var(--ink);
      padding: 32px;
    }}
    .card {{
      width: 1920px;
      height: 1080px;
      position: relative;
      background: var(--paper);
      overflow: hidden;
      padding: 80px 120px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
    }}
    .dot-mat {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 1;
      opacity: .35;
      mix-blend-mode: multiply;
      background-image: radial-gradient(rgba(0,0,0,.045) 1px, transparent 1px);
      background-size: 3px 3px;
    }}
    .left {{
      position: relative;
      z-index: 2;
      padding: 40px 60px 40px 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      border-right: 1px solid var(--line);
    }}
    .right {{
      position: relative;
      z-index: 2;
      padding: 40px 0 40px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .issue-row {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: var(--mono);
      font-size: 18px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 32px;
    }}
    .issue-row .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
    }}
    .h-display {{
      font-family: var(--serif-zh);
      font-weight: 500;
      font-size: 72px;
      line-height: 1.06;
      letter-spacing: .04em;
      margin: 0 0 24px;
      color: var(--ink);
    }}
    .h-sub {{
      font-family: var(--serif-en);
      font-style: italic;
      font-weight: 400;
      font-size: 28px;
      color: var(--muted);
      margin: 0 0 32px;
    }}
    .lead {{
      font-family: var(--serif-zh);
      font-weight: 400;
      font-size: 22px;
      line-height: 1.55;
      color: rgba(10,10,11,.82);
      margin: 0;
    }}
    .meta {{
      font-family: var(--mono);
      font-size: 16px;
      letter-spacing: .20em;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: auto;
    }}
    .info-block {{
      background: var(--paper-2);
      padding: 32px;
      margin-bottom: 24px;
    }}
    .info-title {{
      font-family: var(--mono);
      font-weight: 600;
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 0 0 16px;
    }}
    .info-text {{
      font-family: var(--sans-zh);
      font-weight: 400;
      font-size: 18px;
      line-height: 1.6;
      color: var(--ink);
      margin: 0;
    }}
    .issue-strip {{
      position: absolute;
      bottom: 40px;
      left: 120px;
      right: 120px;
      display: flex;
      justify-content: space-between;
      font-family: var(--mono);
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--muted);
      border-top: 1px solid var(--line);
      padding-top: 16px;
      z-index: 3;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="dot-mat"></div>
    <div class="left">
      <div class="issue-row">
        <span>{layout_id}</span>
        <span class="dot"></span>
        <span>Editorial</span>
      </div>
      <h1 class="h-display">{name.split("—")[0].strip()}</h1>
      <p class="h-sub">{name.split("—")[1].strip() if "—" in name else ""}</p>
      <p class="lead">{scene}</p>
      <p class="meta">Layout Recipe</p>
    </div>
    <div class="right">
      <div class="info-block">
        <p class="info-title">结构</p>
        <p class="info-text">{structure}</p>
      </div>
      <div class="info-block">
        <p class="info-title">适用场景</p>
        <p class="info-text">{scene}</p>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{layout_id} · Editorial</span>
    </div>
  </div>
</body>
</html>'''


def generate_swiss_html(recipe: dict) -> str:
    """生成 Swiss 风格参考图"""
    layout_id = recipe["id"]
    name = recipe["name"]
    scene = recipe["scene"]
    structure = recipe["structure"]

    return f'''<!doctype html>
<html lang="zh-CN" data-accent="ikb">
<head>
  <meta charset="utf-8">
  <title>{layout_id} - {name}</title>
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
    .h-statement {{
      font-family: var(--sans);
      font-weight: 200;
      font-size: 72px;
      line-height: 1.05;
      letter-spacing: -.015em;
      margin: 0 0 24px;
      color: var(--ink);
    }}
    .lead {{
      font-family: var(--sans);
      font-weight: 400;
      font-size: 20px;
      line-height: 1.6;
      color: var(--ink);
      margin: 0;
    }}
    .info-block {{
      background: var(--grey-1);
      padding: 32px;
      margin-bottom: 24px;
    }}
    .info-title {{
      font-family: var(--mono);
      font-weight: 600;
      font-size: 14px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 0 0 16px;
    }}
    .info-text {{
      font-family: var(--sans);
      font-weight: 400;
      font-size: 18px;
      line-height: 1.6;
      color: var(--ink);
      margin: 0;
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
        <span class="t-cat">{layout_id} · Swiss</span>
        <span class="t-meta">Layout Recipe</span>
      </div>
      <h1 class="h-statement">{name.split("—")[0].strip()}</h1>
      <p class="lead">{scene}</p>
    </div>
    <div class="right">
      <div class="info-block">
        <p class="info-title">结构</p>
        <p class="info-text">{structure}</p>
      </div>
      <div class="info-block">
        <p class="info-title">适用场景</p>
        <p class="info-text">{scene}</p>
      </div>
    </div>
    <div class="issue-strip">
      <span>AI创享派</span>
      <span>{layout_id} · Swiss</span>
    </div>
  </div>
</body>
</html>'''


def main():
    """生成所有 28 个版式骨架的参考图"""
    output_dir = Path("layout_samples")
    output_dir.mkdir(exist_ok=True)

    print("正在生成 28 个版式骨架的参考图...")
    print()

    for i, recipe in enumerate(LAYOUT_RECIPES, 1):
        layout_id = recipe["id"]
        name = recipe["name"]

        print(f"[{i:02d}/28] 生成 {layout_id} - {name}...")

        # 生成 HTML
        html_content = generate_layout_html(recipe)
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

        for i, recipe in enumerate(LAYOUT_RECIPES, 1):
            layout_id = recipe["id"]
            name = recipe["name"]
            html_file = output_dir / f"{layout_id}.html"
            png_file = output_dir / f"{layout_id}.png"

            print(f"[{i:02d}/28] 渲染 {layout_id} - {name}...")

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
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
    print("✨ 参考图生成完成！")
    print(f"📁 保存位置: {output_dir}")
    print()
    print("生成的文件:")
    for f in sorted(output_dir.glob("*.png")):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
