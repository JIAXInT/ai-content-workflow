# 图片搜索功能指南

本文档介绍如何使用免费图片搜索功能，为文章自动添加配图。

## 功能概述

图片搜索功能可以根据文章的标题、标签和分类，自动从免费图片平台搜索相关图片，并下载到本地，最后插入到飞书文档中。

### 支持的图片平台

| 平台 | 免费额度 | 特点 |
|------|----------|------|
| **Unsplash** | 50请求/小时 | 高质量摄影作品，支持按尺寸调整 |
| **Pexels** | 200请求/小时 | 丰富的图片库，支持多种尺寸 |
| **Pixabay** | 100请求/分钟 | 图片、插图、矢量图等多种类型 |

所有平台的图片均可免费用于商业用途。

## 配置步骤

### 1. 获取 API Key

#### Unsplash
1. 访问 https://unsplash.com/developers
2. 注册账号并创建应用
3. 获取 Access Key

#### Pexels
1. 访问 https://www.pexels.com/api/
2. 注册账号
3. 获取 API Key

#### Pixabay
1. 访问 https://pixabay.com/api/docs/
2. 注册账号并登录
3. 在页面上获取 API Key

### 2. 配置 API Key

在项目根目录的 `config/image_api_keys.json` 文件中配置：

```json
{
  "unsplash_access_key": "your_unsplash_access_key_here",
  "pexels_api_key": "your_pexels_api_key_here",
  "pixabay_api_key": "your_pixabay_api_key_here"
}
```

**注意**：至少配置一个平台的 API key 即可使用图片搜索功能。

### 3. 测试配置

运行测试脚本验证配置是否正确：

```bash
python scripts/test_image_search.py
```

## 使用方法

### 自动保存时搜索图片

当使用 `save_to_feishu.py` 保存文章时，图片搜索会自动执行：

```bash
# 保存文章到飞书（包含封面图和配图）
python scripts/save_to_feishu.py articles/2025-05-27_mimo-price-drop.md

# 不搜索配图
python scripts/save_to_feishu.py articles/2025-05-27_mimo-price-drop.md --no-images
```

### 单独搜索图片

如果只想搜索图片而不保存到飞书：

```bash
# 搜索关键词相关图片
python scripts/search_images.py "人工智能" 3

# 搜索多个关键词
python scripts/search_images.py "AI 科技" 5
```

### 在代码中使用

```python
from search_images import ImageSearcher

# 创建搜索器
searcher = ImageSearcher()

# 搜索图片
images = searcher.search_images("人工智能", count=3)

# 下载图片
for img in images:
    filepath = searcher.download_image(img)
    print(f"下载完成: {filepath}")

# 根据文章信息搜索
title = "MiMo 2.5 Pro 永久降价"
tags = ["MiMo", "DeepSeek", "AI模型"]
category = "产品发布"

article_images = searcher.search_article_images(title, tags, category, count=3)
```

## 图片插入逻辑

### 插入位置

图片会根据文章长度自动选择插入位置：

- **文章较短**（≤3段）：不插入图片
- **文章中等**（4-10段）：在 1/3 和 2/3 处各插入一张
- **文章较长**（>10段）：在 1/3、2/3 和 3/4 处各插入一张

### 插入格式

图片使用 Markdown 格式插入：

```markdown
![图片描述](images/article_img_20250527_1.jpg)
```

飞书文档会自动识别并显示图片。

## 常见问题

### Q: 为什么没有找到图片？

可能的原因：
1. 未配置 API key
2. 搜索关键词太具体
3. 网络连接问题

解决方案：
- 检查 `config/image_api_keys.json` 配置
- 尝试更通用的关键词
- 检查网络连接

### Q: 图片质量如何保证？

- 所有平台都提供高质量图片
- 默认使用 landscape（横向）方向，适合文章配图
- Unsplash 支持按尺寸调整，确保图片清晰

### Q: 图片版权问题？

所有平台的图片均可免费用于商业用途：
- **Unsplash**：推荐署名但非必须
- **Pexels**：推荐署名但非必须
- **Pixabay**：无需署名

### Q: 如何调整图片数量？

修改 `search_and_download_images` 函数的 `count` 参数：

```python
# 搜索 5 张图片
images = search_and_download_images(title, tags, category, count=5)
```

### Q: 图片下载失败怎么办？

可能的原因：
1. 网络连接问题
2. 图片 URL 无效
3. 磁盘空间不足

解决方案：
- 检查网络连接
- 尝试其他图片平台
- 检查磁盘空间

## 性能优化

### 缓存机制

- 已下载的图片不会重复下载
- 可以添加本地图片缓存数据库

### 并发下载

- 当前为串行下载，适合少量图片
- 如需大量图片，可考虑并发下载

### 图片压缩

- 下载的图片为原始质量
- 可以添加图片压缩功能减少文件大小

## 扩展功能

### 添加更多图片平台

在 `search_images.py` 中添加新的搜索方法：

```python
def search_new_platform(self, query: str, count: int = 5) -> List[Dict]:
    """从新平台搜索图片"""
    # 实现搜索逻辑
    pass
```

### 图片筛选

可以添加图片筛选功能：

```python
# 按颜色筛选
images = searcher.search_images("科技", color="blue")

# 按方向筛选
images = searcher.search_images("风景", orientation="landscape")

# 按尺寸筛选
images = searcher.search_images("产品", min_width=1000)
```

### 图片编辑

可以添加简单的图片编辑功能：

```python
from PIL import Image

# 调整图片大小
img = Image.open(filepath)
img = img.resize((800, 600))
img.save(filepath)

# 添加水印
# ...
```

## 更新日志

### v1.0.0 (2025-05-27)
- 初始版本
- 支持 Unsplash、Pexels、Pixabay 三个平台
- 自动搜索和下载图片
- 集成到飞书保存流程
