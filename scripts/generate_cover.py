#!/usr/bin/env python3
"""
动态生成封面图脚本
根据文章标题、标签、日期生成封面图
"""

import sys
from pathlib import Path
from datetime import datetime


# 封面 HTML 模板
COVER_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>公众号封面图</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root {{
    /* 莫兰迪色系 */
    --blue: #6B8FAD;
    --blue-light: #D4E1E9;
    --orange: #C4A882;
    --orange-light: #E8DDD0;
    --bg: #F5F0EB;
    --bg-warm: #EDE8E2;
    --dark: #1A1A1A;
    --gray: #6B6560;
    --light: #E8E3DD;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #D5CEC6;
    font-family: 'Noto Sans SC', 'Inter', sans-serif;
  }}

  .cover {{
    width: 900px;
    height: 383px;
    position: relative;
    overflow: hidden;
    background: var(--bg);
  }}

  /* 背景装饰层 */
  .bg-deco {{
    position: absolute;
    inset: 0;
    pointer-events: none;
  }}

  .circle-1 {{
    position: absolute;
    top: -120px;
    right: -80px;
    width: 350px;
    height: 350px;
    border: 1px solid rgba(107, 143, 173, 0.12);
    border-radius: 50%;
  }}

  .circle-2 {{
    position: absolute;
    top: -60px;
    right: -20px;
    width: 200px;
    height: 200px;
    border: 1px solid rgba(107, 143, 173, 0.08);
    border-radius: 50%;
  }}

  .circle-3 {{
    position: absolute;
    bottom: -100px;
    left: -60px;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(107, 143, 173, 0.06) 0%, transparent 70%);
    border-radius: 50%;
  }}

  .dots {{
    position: absolute;
    top: 30px;
    right: 180px;
    display: grid;
    grid-template-columns: repeat(5, 8px);
    gap: 12px;
  }}

  .dots span {{
    width: 3px;
    height: 3px;
    background: rgba(107, 143, 173, 0.2);
    border-radius: 50%;
  }}

  .crosshair {{
    position: absolute;
    top: 50px;
    right: 100px;
    width: 20px;
    height: 20px;
  }}

  .crosshair::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(107, 143, 173, 0.25);
  }}

  .crosshair::after {{
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 1px;
    background: rgba(107, 143, 173, 0.25);
  }}

  .glow {{
    position: absolute;
    top: 50%;
    right: 15%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(107, 143, 173, 0.08) 0%, transparent 70%);
    border-radius: 50%;
    transform: translateY(-50%);
  }}

  /* 内容容器 */
  .content {{
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-rows: auto 1fr auto;
    padding: 45px 60px 50px;
    z-index: 2;
  }}

  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .header-left {{
    display: flex;
    align-items: center;
    gap: 24px;
  }}

  .brand {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .brand-icon {{
    width: 30px;
    height: 30px;
    background: var(--blue);
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .brand-icon span {{
    font-size: 13px;
    font-weight: 900;
    color: white;
  }}

  .brand-text {{
    font-size: 15px;
    font-weight: 700;
    color: #2D2D2D;
  }}

  .tag {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 14px;
    background: var(--light);
    border-radius: 20px;
  }}

  .tag-dot {{
    width: 5px;
    height: 5px;
    background: var(--blue);
    border-radius: 50%;
  }}

  .tag-text {{
    font-size: 11px;
    font-weight: 600;
    color: var(--blue);
    letter-spacing: 2px;
    text-transform: uppercase;
  }}

  .date {{
    font-size: 12px;
    font-weight: 500;
    color: var(--gray);
  }}

  .main {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 18px;
  }}

  .title {{
    font-size: 48px;
    font-weight: 900;
    color: #1A1A1A;
    line-height: 1.15;
    letter-spacing: -1px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }}

  .title .blue {{
    color: #4A7594;
    font-weight: 900;
  }}

  .title .orange {{
    color: #A88B6A;
  }}

  .subtitle {{
    font-size: 16px;
    font-weight: 500;
    color: #6B6560;
    line-height: 1.7;
    letter-spacing: 0.3px;
  }}

  .subtitle strong {{
    color: #2D2D2D;
    font-weight: 700;
  }}

  .footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .footer-left {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .footer-line {{
    width: 28px;
    height: 2px;
    background: var(--orange);
    border-radius: 1px;
  }}

  .footer-text {{
    font-size: 11px;
    font-weight: 600;
    color: var(--gray);
    letter-spacing: 2px;
  }}

  .bottom-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(to right, var(--blue), var(--orange));
    z-index: 3;
  }}
</style>
</head>
<body>

<div class="cover">
  <div class="bg-deco">
    <div class="circle-1"></div>
    <div class="circle-2"></div>
    <div class="circle-3"></div>
    <div class="glow"></div>
    <div class="dots">
      <span></span><span></span><span></span><span></span><span></span>
      <span></span><span></span><span></span><span></span><span></span>
      <span></span><span></span><span></span><span></span><span></span>
      <span></span><span></span><span></span><span></span><span></span>
      <span></span><span></span><span></span><span></span><span></span>
    </div>
    <div class="crosshair"></div>
  </div>

  <div class="content">
    <div class="header">
      <div class="header-left">
        <div class="brand">
          <div class="brand-icon"><span>AI</span></div>
          <div class="brand-text">AI创享派</div>
        </div>
        <div class="tag">
          <div class="tag-dot"></div>
          <div class="tag-text">{tag}</div>
        </div>
      </div>
      <div class="date">{date}</div>
    </div>

    <div class="main">
      <h1 class="title">
        {title_line1}<br>
        {title_line2}
      </h1>
      <p class="subtitle">
        {subtitle}
      </p>
    </div>

    <div class="footer">
      <div class="footer-left">
        <div class="footer-line"></div>
        <div class="footer-text">{year}</div>
      </div>
    </div>
  </div>

  <div class="bottom-bar"></div>
</div>

</body>
</html>'''


def generate_cover(title, tag, date, subtitle, output_path):
    """生成封面图 HTML"""
    # 解析标题，分成两行
    # 如果标题包含逗号、冒号等，尝试在这些位置断行
    title_lines = split_title(title)

    # 格式化日期
    if isinstance(date, str):
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%Y.%m.%d")
            year = date_obj.strftime("%Y")
        except ValueError:
            formatted_date = date
            year = date[:4]
    else:
        formatted_date = str(date)
        year = str(date)[:4]

    # 生成 HTML
    html = COVER_TEMPLATE.format(
        tag=tag,
        date=formatted_date,
        title_line1=title_lines[0],
        title_line2=title_lines[1] if len(title_lines) > 1 else "",
        subtitle=subtitle,
        year=year
    )

    # 写入文件
    output_file = Path(output_path)
    output_file.write_text(html, encoding="utf-8")

    return output_file


def split_title(title):
    """将标题分成两行"""
    # 优先在这些位置断行
    breakpoints = ["，", "：", "，", "、", " ", "—", "-"]

    for bp in breakpoints:
        if bp in title:
            parts = title.split(bp, 1)
            if len(parts[0]) >= 4 and len(parts[1]) >= 4:
                return [parts[0], parts[1]]

    # 如果标题较短，直接返回
    if len(title) <= 15:
        return [title]

    # 否则在中间位置断行
    mid = len(title) // 2
    # 尝试在标点符号附近断行
    for i in range(mid - 3, mid + 4):
        if i < len(title) and title[i] in "，。、：；！？":
            return [title[:i + 1], title[i + 1:]]

    # 强制断行
    return [title[:mid], title[mid:]]


def main():
    if len(sys.argv) < 5:
        print("用法: python generate_cover.py <标题> <标签> <日期> <副标题> <输出路径>")
        print("示例: python generate_cover.py 'MiMo降价' '产品发布' '2025-05-27' '最高降幅99%' covers/cover.html")
        sys.exit(1)

    title = sys.argv[1]
    tag = sys.argv[2]
    date = sys.argv[3]
    subtitle = sys.argv[4]
    output_path = sys.argv[5]

    generate_cover(title, tag, date, subtitle, output_path)
    print(f"封面 HTML 已生成: {output_path}")


if __name__ == "__main__":
    main()
