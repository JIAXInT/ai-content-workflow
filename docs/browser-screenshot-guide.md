# 浏览器截图工具使用指南

## 概述

浏览器截图工具是一个用于获取 X 平台（Twitter）等有反爬虫机制网站截图的工具。它通过打开真实的浏览器窗口，让用户手动操作后再截取屏幕，从而绕过反爬虫机制，获取真实的页面内容。

## 为什么需要这个工具？

X 平台（Twitter）有严格的反爬虫机制，自动化截图工具（如 Playwright、Selenium）难以获取完整的推文内容。浏览器截图工具通过以下方式解决这个问题：

1. **打开真实浏览器**：不是无头模式，而是显示真实的浏览器窗口
2. **用户手动操作**：可以登录、滚动、点击等操作
3. **截取真实内容**：截取用户实际看到的页面内容

## 使用方法

### 基本用法

```bash
# 打开浏览器，手动操作后按 Enter 截图
python scripts/browser_screenshot.py "https://x.com/user/status/123456"
```

### 自动截图

```bash
# 等待 10 秒后自动截图（适合页面加载较慢的情况）
python scripts/browser_screenshot.py "https://x.com/user/status/123456" --wait 10
```

### 指定输出目录

```bash
# 截图保存到指定目录
python scripts/browser_screenshot.py "https://x.com/user/status/123456" -o images/my-article/
```

## 操作流程

1. **运行命令**：执行上述命令后，浏览器会自动打开并访问指定 URL
2. **手动操作**：
   - 如果需要登录，请在浏览器中登录
   - 滚动页面找到要截取的内容
   - 点击展开需要显示的内容
3. **截图**：
   - 按 Enter 键截取当前屏幕
   - 或输入等待秒数（如 '5'）等待后自动截图
   - 或输入 'q' 退出不截图
4. **完成**：截图会自动保存到指定目录

## 支持的平台

| 平台 | 推荐方式 | 说明 |
|------|----------|------|
| X/Twitter | 浏览器截图工具 | 有反爬虫机制，需要手动操作 |
| GitHub | 自动截图工具 | 直接使用 `screenshot_webpage.py` |
| 微博 | 自动截图工具 | 直接使用 `screenshot_webpage.py` |
| 知乎 | 自动截图工具 | 直用 `screenshot_webpage.py` |

## 在文章中引用截图

截图保存后，可以在文章中使用 Markdown 图片语法引用：

```markdown
![推文截图](../images/manual/twitter_20260603_102514_1234567890.png)
```

## 示例

### 示例 1：截取 X 平台推文

```bash
# 打开浏览器，手动登录后截取推文
python scripts/browser_screenshot.py "https://x.com/AnthropicAI/status/1929213162397413582"
```

### 示例 2：截取需要登录的页面

```bash
# 打开浏览器，手动登录后截取首页
python scripts/browser_screenshot.py "https://twitter.com/home"
```

### 示例 3：批量截图

```bash
# 截取多个推文
python scripts/browser_screenshot.py "https://x.com/user1/status/123" -o images/article1/
python scripts/browser_screenshot.py "https://x.com/user2/status/456" -o images/article1/
```

## 常见问题

### Q: 浏览器打开后页面空白怎么办？

A: 可能是网络问题或需要登录。请在浏览器中手动刷新页面或登录后再截图。

### Q: 截图不完整怎么办？

A: 请确保在截图前滚动页面，使要截取的内容完全显示在屏幕上。

### Q: 如何截取长推文？

A: 对于长推文，建议：
1. 先点击推文进入详情页
2. 滚动显示完整内容
3. 使用 `--type full` 参数截取整个页面（如果支持）

### Q: 截图保存在哪里？

A: 默认保存在 `images/manual/` 目录，文件名格式为 `{platform}_{date}_{id}.png`

## 技术细节

- 使用 Playwright 启动真实的 Chromium 浏览器
- 2x 分辨率截图（高清）
- 支持中文界面和时区
- 自动检测平台并生成合适的文件名

## 相关工具

- `screenshot_webpage.py`：自动化截图工具，适合没有反爬虫机制的网站
- `browser_screenshot.py`：浏览器截图工具，适合有反爬虫机制的网站

## 更新日志

- 2026-06-03：创建浏览器截图工具
