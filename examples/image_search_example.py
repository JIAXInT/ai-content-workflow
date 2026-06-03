#!/usr/bin/env python3
"""
图片搜索功能示例
演示如何使用图片搜索功能为文章添加配图
"""

import sys
from pathlib import Path

# 添加 scripts 目录到 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from search_images import ImageSearcher


def example_basic_search():
    """基本搜索示例"""
    print("=== 基本搜索示例 ===\n")

    # 创建搜索器
    searcher = ImageSearcher()

    # 搜索图片
    query = "人工智能"
    count = 3
    print(f"搜索关键词: {query}")
    print(f"搜索数量: {count}")

    images = searcher.search_images(query, count)
    print(f"\n找到 {len(images)} 张图片:")

    for i, img in enumerate(images, 1):
        print(f"\n{i}. 平台: {img['source']}")
        print(f"   描述: {img['description'][:50]}...")
        print(f"   作者: {img['author']}")
        print(f"   URL: {img['url'][:60]}...")

    return images


def example_article_search():
    """文章配图搜索示例"""
    print("\n=== 文章配图搜索示例 ===\n")

    # 创建搜索器
    searcher = ImageSearcher()

    # 文章信息
    title = "MiMo 2.5 Pro 永久降价，最高降幅99%，跟DeepSeek V4 Pro同价"
    tags = ["MiMo", "DeepSeek", "AI模型", "价格战", "小米"]
    category = "产品发布"

    print(f"文章标题: {title}")
    print(f"文章标签: {tags}")
    print(f"文章分类: {category}")

    # 搜索相关图片
    images = searcher.search_article_images(title, tags, category, count=3)
    print(f"\n找到 {len(images)} 张相关图片:")

    for i, img in enumerate(images, 1):
        print(f"\n{i}. 平台: {img['source']}")
        print(f"   描述: {img['description'][:50]}...")
        print(f"   作者: {img['author']}")
        print(f"   URL: {img['url'][:60]}...")

    return images


def example_download_images(images):
    """下载图片示例"""
    print("\n=== 下载图片示例 ===\n")

    if not images:
        print("没有图片可下载")
        return

    # 创建搜索器
    searcher = ImageSearcher()

    # 下载第一张图片
    img = images[0]
    print(f"下载图片: {img['description'][:50]}...")

    filepath = searcher.download_image(img, "example_image.jpg")
    if filepath:
        print(f"下载成功: {filepath}")
        print(f"文件大小: {filepath.stat().st_size / 1024:.1f} KB")

        # 清理示例文件
        filepath.unlink(missing_ok=True)
        print("(示例文件已清理)")
    else:
        print("下载失败")


def example_insert_to_content():
    """插入图片到文章内容示例"""
    print("\n=== 插入图片到文章内容示例 ===\n")

    # 模拟文章内容
    article_content = """昨天刷到一条消息，愣了一下。

小米的MiMo-V2.5系列API，永久降价，最高降幅99%。

没看错，99%。

我反复确认了两遍，不是限时促销，不是新用户专享，是永久调价。而且同步把token套餐升级了，同样的价格，可用的token量增加5到8倍。计费规则也重新梳理了一遍，变得更简单透明。

最关键的一句，所有现有用户的套餐额度，全额重置。

就是说你之前剩多少额度，不重要了，直接给你满上。

我寻思了一下，上一次看到这种力度的降价，还是DeepSeek把价格打下来那次。

坦率的讲，小米这次做的事，跟DeepSeek当年的逻辑是一样的，不是在原有价格体系上做微调，而是直接掀桌子。你不是觉得AI API贵吗，好，我给你干到跟最便宜的那个同价。

但这里有个细节我觉得挺有意思的。

小米官方说这次降价的原因是「全栈推理优化与服务效率提升」，后续还会发技术博客详细讲。这句话翻译一下就是，我不是在烧钱补贴，我是真的把成本做下来了。

这个区别很重要。

烧钱补贴的降价不可持续，今天能降明天就能涨回来。但如果是技术驱动的成本下降，那这个价格就是新常态。DeepSeek当年能做到低价，靠的是MoE架构带来的推理效率。小米说自己的全栈优化做到了，具体怎么做到的，等技术博客出来再看。

但不管技术细节是什么，结果已经摆在这了。

MiMo-V2.5-Pro，跟DeepSeek V4 Pro同价。"""

    # 模拟图片
    images = [
        {"path": Path("images/test1.jpg"), "info": {"alt": "AI技术"}},
        {"path": Path("images/test2.jpg"), "info": {"alt": "价格下降"}},
        {"path": Path("images/test3.jpg"), "info": {"alt": "小米Logo"}},
    ]

    print("原始文章长度:", len(article_content), "字符")
    print("插入图片数量:", len(images))

    # 导入插入函数
    from save_to_feishu import insert_images_to_content

    # 插入图片
    new_content = insert_images_to_content(article_content, images)
    print("\n插入后文章长度:", len(new_content), "字符")

    # 显示插入位置
    lines = new_content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('!['):
            print(f"\n图片插入位置 (第{i+1}行):")
            print(f"  {line}")


def main():
    """主函数"""
    print("图片搜索功能示例\n")

    # 检查 API 配置
    searcher = ImageSearcher()
    if not any([searcher.unsplash_key, searcher.pexels_key, searcher.pixabay_key]):
        print("错误: 未配置 API key")
        print("请在 config/image_api_keys.json 中配置 API key")
        print("\n获取 API key:")
        print("- Unsplash: https://unsplash.com/developers")
        print("- Pexels: https://www.pexels.com/api/")
        print("- Pixabay: https://pixabay.com/api/docs/")
        return

    # 运行示例
    images = example_basic_search()
    example_article_search()
    example_download_images(images)
    example_insert_to_content()

    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main()
