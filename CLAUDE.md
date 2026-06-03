# AI 内容创作工作流

## 项目概述
这是一个 AI 内容账号的每日创作工作流，覆盖公众号、小红书、抖音三端，支持自动保存到飞书文档。

## 模型自动切换规则

### 多模态任务自动使用 Sonnet 模型
当检测到以下情况时，**必须使用 `model: "sonnet"` 参数调用 Agent**：
- 用户发送了图片（截图、照片、图表等）
- 用户要求识别/分析/描述图片内容
- 用户说"识别图片"、"看图"、"OCR"、"图片里有什么"等关键词
- 任务涉及图片理解、文字提取、图表分析

**原因**：当前主模型 `mimo-v2.5-pro` 不支持多模态，而 Sonnet 槽位已映射到 `mimo-v2.5`（支持多模态）。

**正确做法**：
```javascript
// 检测到图片任务时，不要用 Read 工具（会用当前模型），而是用 Agent 工具
Agent({
  subagent_type: "claude",
  model: "sonnet",  // ← 自动使用 mimo-v2.5（支持多模态）
  prompt: "请使用 Read 工具读取图片 [图片路径]，然后识别并详细描述图片内容..."
})
```

**关键点**：`Read` 工具会使用当前模型处理图片，如果当前模型不支持多模态就会报错。所以必须通过 `Agent` 工具间接调用 `Read`，让 Agent 用支持多模态的 Sonnet 模型来处理。

**其他任务**（写文章、查热点、生成卡片等）继续使用默认的 `mimo-v2.5-pro` 模型，无需指定 model 参数。

## 每日工作流

### 第一步：获取 AI 热点
当用户说「今日热点」「AI 日报」「看看今天有什么」时：
1. 使用 `aihot` 技能获取最新 AI 热点精选
2. 按「模型发布/产品发布/行业动态/论文研究/技巧与观点」分类展示
3. 等待用户确认要写的选题

### 第二步：确认选题
用户从热点列表中选择 1-3 个感兴趣的选题，可以：
- 直接说编号（「写第 3 条」）
- 说方向（「写那个模型发布的」）
- 组合多条（「把 1 和 5 合在一起写」）

### 第三步：获取原文素材（自动化）
用户确认选题后，**自动截取原文网页**作为文章素材，增强可信度和「活人感」：
1. 从选题中提取原始 URL（推文、博客、GitHub 等）
2. 运行 `python scripts/screenshot_webpage.py <url1> <url2> ...` 截取原文
3. 自动识别平台（Twitter/X、微博、知乎、GitHub 等）并使用对应策略
4. 截图保存到 `images/YYYY-MM-DD_article-name/` 目录
5. 在文章中引用截图（每篇至少 2-3 张），增强可信度和「活人感」

#### 浏览器截图工具（推荐用于 X 平台）
对于 X 平台等有反爬虫机制的网站，使用浏览器截图工具：
```bash
# 打开浏览器手动操作后截图（交互式）
python scripts/browser_screenshot.py "https://x.com/user/status/123456"

# 等待 10 秒后自动截图
python scripts/browser_screenshot.py "https://x.com/user/status/123456" --wait 10

# 指定输出目录
python scripts/browser_screenshot.py "url" -o images/my-article/
```

### 第四步：生成公众号文章
用户确认选题后，使用 `khazix-writer` 技能生成公众号长文：
1. 基于选题素材，以「AI创享派」风格写作
2. 文章 4000-8000 字
3. 跑四层自检体系（L1 硬性规则 → L2 风格一致性 → L3 内容质量 → L4 活人感）
4. 输出质检报告

### 第五步：生成社交卡片并保存到飞书文档
文章生成后，自动生成社交卡片并保存到飞书文档：
1. 保存文章到本地：`articles/YYYY-MM-DD_标题.md`
2. 生成社交卡片：运行 `python scripts/generate_social_cards.py articles/YYYY-MM-DD_标题.md`
   - 自动创建目录：`covers/YYYY-MM-DD_article-name/`
   - 生成 HTML 文件：`social-cards.html`
3. 渲染为 PNG：运行 `python scripts/render_social_cards.py covers/YYYY-MM-DD_article-name/social-cards.html`
   - 自动生成 7 张 PNG 图片到同一目录
4. 获取原文截图作为插图：自动从文章中提取原文链接并截取截图
5. 保存到飞书：运行 `python scripts/save_to_feishu.py articles/YYYY-MM-DD_标题.md`
6. 输出飞书文档链接

#### 社交卡片输出
- **公众号封面**：21:9 主封面 + 1:1 方封面
- **小红书轮播图**：3:4 比例，5-9 页（封面、数据、对比、要点、总结）
- 支持 Swiss 和 Editorial 两种风格
- 支持 4 种强调色：ikb（克莱因蓝）、lemon-yellow、lemon-green、safety-orange
- **目录结构**：以日期和文章主题命名的文件夹，便于管理

### 第六步：多端适配（可选）
- 公众号：完整长文
- 小红书：提炼 3-5 个核心观点，配图文案
- 抖音：口播脚本或短视频文案

## 快捷命令
- `今日热点` / `AI 日报` → 拉取最新热点
- `截图素材` / `截取原文` → 截取选题的原文网页作为素材
- `写文章` → 基于已选热点生成公众号文章
- `质检` → 对已写文章跑四层自检
- `生成卡片` → 基于文章生成社交卡片（公众号封面 + 小红书轮播图）
  - 自动创建目录：`covers/YYYY-MM-DD_article-name/`
  - 生成 HTML 和 PNG 文件
- `保存到飞书` → 将文章保存到飞书文档（包含社交卡片）

## 社交卡片生成

### 功能概述
基于 guizang-social-card-skill 的模板系统，自动生成符合中文社交平台规范的视觉卡片。

### 输出格式
- **公众号封面**：
  - 21:9 主封面（2100×900 像素）
  - 1:1 方封面（1080×1080 像素）
- **小红书轮播图**：
  - 3:4 比例（1080×1440 像素）
  - 5-9 页（封面、核心数据、对比分析、要点列表、总结）

### 目录结构
生成的文件会自动保存到以日期和文章主题命名的文件夹中：
```
covers/
  YYYY-MM-DD_article-name/
    social-cards.html          # HTML 源文件
    cover-21x9-wechat-21x9.png # 公众号 21:9 主封面
    cover-1x1-wechat-1x1.png   # 公众号 1:1 方封面
    xhs-xhs-01.png             # 小红书第 1 页：封面
    xhs-xhs-02.png             # 小红书第 2 页：核心数据
    xhs-xhs-03.png             # 小红书第 3 页：对比分析
    xhs-xhs-04.png             # 小红书第 4 页：要点列表
    xhs-xhs-05.png             # 小红书第 5 页：总结
```

### 使用方法
```bash
# 基本用法：从文章生成社交卡片（自动创建以文章名命名的文件夹）
python scripts/generate_social_cards.py articles/YYYY-MM-DD_标题.md

# 指定样式（swiss 或 editorial）
python scripts/generate_social_cards.py articles/YYYY-MM-DD_标题.md --style swiss

# 指定强调色（ikb、lemon-yellow、lemon-green、safety-orange）
python scripts/generate_social_cards.py articles/YYYY-MM-DD_标题.md --accent ikb

# 指定输出文件（不使用自动目录结构）
python scripts/generate_social_cards.py articles/YYYY-MM-DD_标题.md -o covers/custom-cards.html

# 只输出 JSON 数据（不生成 HTML）
python scripts/generate_social_cards.py articles/YYYY-MM-DD_标题.md --json

# 渲染 HTML 为 PNG 图片（自动保存到同一目录）
python scripts/render_social_cards.py covers/YYYY-MM-DD_article-name/social-cards.html

# 渲染时自动检测卡片元素（默认开启）
python scripts/render_social_cards.py covers/YYYY-MM-DD_article-name/social-cards.html --auto-detect

# 使用默认配置渲染（不自动检测）
python scripts/render_social_cards.py covers/YYYY-MM-DD_article-name/social-cards.html --no-auto-detect
```

### 样式说明
- **Swiss 风格**：国际主义设计，网格布局、单色强调、极端字号对比，适合产品评测、数据、教程内容
- **Editorial 风格**：杂志风格，衬线字体、墨水纹理、杂志排版，适合叙事、生活方式、旅行内容

### 强调色预设
- **ikb**（克莱因蓝）：经典蓝色，专业感强
- **lemon-yellow**：柠檬黄，活泼醒目
- **lemon-green**：柠檬绿，清新自然
- **safety-orange**：安全橙，警示感强

### 自动提取内容
脚本会自动从 Markdown 文章中提取：
- 标题和副标题
- 关键数据点（百分比、倍数、金额）
- 要点列表
- 结论和总结
- 标签和分类

### 自定义模板
模板文件位于 `templates/` 目录：
- `templates/social-card-swiss.html`：Swiss 风格模板
- `templates/social-card-editorial.html`：Editorial 风格模板（待创建）

## 网页截图

### 功能概述
使用 Playwright 截取网页内容，支持 Twitter/X、微博、知乎、GitHub 等平台的特殊处理。用于在文章创作中获取原文素材，增强文章可信度和「活人感」。

### 使用方法
```bash
# 截取单个网页
python scripts/screenshot_webpage.py "https://twitter.com/user/status/123456"

# 截取多个网页
python scripts/screenshot_webpage.py "url1" "url2" "url3"

# 指定输出目录
python scripts/screenshot_webpage.py "url" -o images/YYYY-MM-DD_article-name/

# 截取全文（默认截取关键元素）
python scripts/screenshot_webpage.py "url" --type full

# 截取视口
python scripts/screenshot_webpage.py "url" --type viewport
```

### 支持的平台
| 平台 | 截图目标 | 说明 |
|------|----------|------|
| Twitter/X | 推文卡片 | 自动等待动态加载，截取完整推文 |
| 微博 | 微博内容 | 截取微博文本和配图 |
| 知乎 | 回答/文章 | 截取富文本内容 |
| GitHub | README/Issue | 截取代码和讨论 |
| 通用网页 | 文章主体 | 智能识别内容区域 |

### 输出格式
- 文件名：`screenshot_{platform}_{date}_{id}.png`
- 分辨率：2x 高清截图
- 保存位置：`images/YYYY-MM-DD_article-name/` 或指定目录

### 截图类型
- `element`（默认）：截取关键元素（推文卡片、文章主体等）
- `viewport`：截取当前视口
- `full`：截取整个页面（包括滚动区域）

### 在文章中引用
```markdown
![推文截图](../images/YYYY-MM-DD_article-name/screenshot_twitter_20260603_123456.png)
```

## 飞书集成

### 前置条件
1. 安装飞书 CLI：`npm install -g @larksuite/cli`
2. 添加 skills：`npx skills add larksuite/cli -g -y`
3. 配置认证：`npx @larksuite/cli config init --new`
4. 登录授权：`npx @larksuite/cli auth login --recommend`
5. 启用权限：在飞书开发者后台启用 `docs:document.media:upload` 权限
6. 配置图片搜索 API key（可选）：在 `config/image_api_keys.json` 中配置

### 使用方法
```bash
# 保存文章到飞书（自动使用原文截图作为插图）
python scripts/save_to_feishu.py articles/YYYY-MM-DD_标题.md

# 不生成封面图
python scripts/save_to_feishu.py articles/YYYY-MM-DD_标题.md --no-cover

# 不添加配图
python scripts/save_to_feishu.py articles/YYYY-MM-DD_标题.md --no-images

# 指定截图数量（默认 3 张）
python scripts/save_to_feishu.py articles/YYYY-MM-DD_标题.md --count 5

# 测试飞书功能
python scripts/test_feishu_save.py
```

### 原文截图说明
插图使用原文链接的截图，从文章中自动提取原文链接并截取：
- 自动从文章内容中提取原文链接（Twitter/X、GitHub、知乎、微博等）
- 使用 Playwright 截取原文网页内容（推荐使用 `--type viewport` 参数）
- 支持多种平台的特殊处理（推文卡片、Issue、回答等）
- 截图保存到 `images/YYYY-MM-DD_article-name/` 目录
- **分段插入位置**（根据小标题自动分割）：
  - 将文章按小标题分成多个部分
  - 每个截图插入到对应内容之后
  - 自动交替追加内容和插入截图

#### 截图参数推荐
```bash
# 推荐：截取视口（包含标题和正文开头）
python scripts/screenshot_webpage.py "url" -o "output_dir" --type viewport

# 备选：截取整个页面（页面内容较短时）
python scripts/screenshot_webpage.py "url" -o "output_dir" --type full

# ❌ 不推荐：只截取导航栏
python scripts/screenshot_webpage.py "url" -o "output_dir" --clip top
```

### 常见问题
- **认证过期**：运行 `npx @larksuite/cli auth login --recommend` 重新登录
- **权限不足**：在飞书开发者后台启用相应权限
- **编码问题**：确保脚本使用 `encoding='utf-8'` 参数
- **截图失败**：检查 Playwright 是否正确安装，运行 `playwright install chromium`
- **截图只有导航栏**：使用 `--type viewport` 参数，不要使用 `--clip top`
- **作者名称错误**：确保文章中使用"AI创享派"，不是"数字生命卡兹克"
- **封面图缺失**：默认生成封面图，只在用户明确要求时才使用 `--no-cover`
