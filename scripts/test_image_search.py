#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片搜索功能测试脚本
测试从 Unsplash、Pexels、Pixabay 搜索免费图片
"""

import sys
from pathlib import Path

# 添加 scripts 目录到 Python 路径
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from search_images import ImageSearcher


def test_image_search():
    """测试图片搜索功能"""
    print("=== Image Search Test ===\n")

    # 创建搜索器
    searcher = ImageSearcher()

    # 检查 API key 配置
    print("1. Check API key configuration:")
    print(f"   Unsplash: {'OK' if searcher.unsplash_key else 'NOT SET'}")
    print(f"   Pexels:   {'OK' if searcher.pexels_key else 'NOT SET'}")
    print(f"   Pixabay:  {'OK' if searcher.pixabay_key else 'NOT SET'}")

    if not any([searcher.unsplash_key, searcher.pexels_key, searcher.pixabay_key]):
        print("\nError: No API key configured")
        print("Please configure API key in config/image_api_keys.json")
        print("\nGet API key:")
        print("- Unsplash: https://unsplash.com/developers")
        print("- Pexels: https://www.pexels.com/api/")
        print("- Pixabay: https://pixabay.com/api/docs/")
        return False

    # 测试搜索
    print("\n2. Test search functionality:")
    test_queries = [
        ("artificial intelligence", 2),
        ("technology", 2),
        ("data", 2),
    ]

    for query, count in test_queries:
        print(f"\n   Search: '{query}' (count: {count})")
        results = searcher.search_images(query, count)
        print(f"   Found: {len(results)} images")

        for i, img in enumerate(results, 1):
            desc = img.get('description', '') or img.get('alt', '')
            print(f"   {i}. [{img['source']}] {desc[:40]}...")
            print(f"      URL: {img['url'][:60]}...")

    # 测试文章图片搜索
    print("\n3. Test article image search:")
    title = "MiMo 2.5 Pro price drop"
    tags = ["MiMo", "DeepSeek", "AI", "price", "Xiaomi"]
    category = "product"

    print(f"   Title: {title}")
    print(f"   Tags: {tags}")
    print(f"   Category: {category}")

    images = searcher.search_article_images(title, tags, category, count=3)
    print(f"\n   Found: {len(images)} related images")

    for i, img in enumerate(images, 1):
        desc = img.get('description', '') or img.get('alt', '')
        print(f"   {i}. [{img['source']}] {desc[:40]}...")
        print(f"      Author: {img['author']}")

    # 测试下载
    print("\n4. Test image download:")
    if images:
        img = images[0]
        print(f"   Download: {img['url'][:60]}...")
        filepath = searcher.download_image(img, "test_image.jpg")
        if filepath:
            print(f"   Success: {filepath}")
            # 清理测试文件
            filepath.unlink(missing_ok=True)
            print("   (Test file cleaned)")
        else:
            print("   Failed: Unable to download image")

    print("\n=== Test Complete ===")
    return True


if __name__ == "__main__":
    success = test_image_search()
    sys.exit(0 if success else 1)
