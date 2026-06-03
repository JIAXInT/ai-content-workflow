#!/usr/bin/env python3
"""
免费图片搜索脚本
支持从 Unsplash、Pexels、Pixabay 搜索免费图片
根据文章关键词返回相关图片URL
"""

import requests
import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class ImageSearcher:
    """免费图片搜索器"""

    def __init__(self, config_path: Optional[str] = None):
        # 从环境变量或配置文件读取 API keys
        self.unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY", "")
        self.pexels_key = os.getenv("PEXELS_API_KEY", "")
        self.pixabay_key = os.getenv("PIXABAY_API_KEY", "")

        # 如果环境变量没有配置，尝试从配置文件读取
        if not any([self.unsplash_key, self.pexels_key, self.pixabay_key]):
            self._load_config(config_path)

        # 图片保存目录
        self.images_dir = Path("images")
        self.images_dir.mkdir(exist_ok=True)

    def _load_config(self, config_path: Optional[str] = None):
        """从配置文件加载 API keys"""
        if config_path is None:
            # 默认配置文件路径
            config_path = Path(__file__).parent.parent / "config" / "image_api_keys.json"
        else:
            config_path = Path(config_path)

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.unsplash_key = config.get("unsplash_access_key", "")
                    self.pexels_key = config.get("pexels_api_key", "")
                    self.pixabay_key = config.get("pixabay_api_key", "")
                    print(f"Loaded API keys from {config_path}")
            except Exception as e:
                print(f"Failed to load config: {e}")

    def search_unsplash(self, query: str, count: int = 5) -> List[Dict]:
        """从 Unsplash 搜索图片"""
        if not self.unsplash_key:
            print("Unsplash API key not configured")
            return []

        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {self.unsplash_key}"
        }
        params = {
            "query": query,
            "per_page": count,
            "orientation": "landscape"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for photo in data.get("results", []):
                results.append({
                    "source": "unsplash",
                    "id": photo["id"],
                    "url": photo["urls"]["regular"],  # 1080px wide
                    "thumb": photo["urls"]["thumb"],
                    "author": photo["user"]["name"],
                    "author_url": photo["user"]["links"]["html"],
                    "description": photo.get("description", ""),
                    "alt": photo.get("alt_description", query)
                })
            return results

        except Exception as e:
            print(f"Unsplash search failed: {e}")
            return []

    def search_pexels(self, query: str, count: int = 5) -> List[Dict]:
        """从 Pexels 搜索图片"""
        if not self.pexels_key:
            print("Pexels API key not configured")
            return []

        url = "https://api.pexels.com/v1/search"
        headers = {
            "Authorization": self.pexels_key
        }
        params = {
            "query": query,
            "per_page": count,
            "orientation": "landscape"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for photo in data.get("photos", []):
                results.append({
                    "source": "pexels",
                    "id": photo["id"],
                    "url": photo["src"]["large"],  # 940px wide
                    "thumb": photo["src"]["tiny"],
                    "author": photo["photographer"],
                    "author_url": photo["photographer_url"],
                    "description": photo.get("alt", ""),
                    "alt": photo.get("alt", query)
                })
            return results

        except Exception as e:
            print(f"Pexels search failed: {e}")
            return []

    def search_pixabay(self, query: str, count: int = 5) -> List[Dict]:
        """从 Pixabay 搜索图片"""
        if not self.pixabay_key:
            print("Pixabay API key not configured")
            return []

        url = "https://pixabay.com/api/"
        params = {
            "key": self.pixabay_key,
            "q": query,
            "image_type": "photo",
            "orientation": "horizontal",
            "per_page": count,
            "safesearch": "true"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for hit in data.get("hits", []):
                results.append({
                    "source": "pixabay",
                    "id": hit["id"],
                    "url": hit["webformatURL"],  # 640px wide
                    "thumb": hit["previewURL"],
                    "author": hit["user"],
                    "author_url": f"https://pixabay.com/users/{hit['user']}-{hit['user_id']}",
                    "description": hit.get("tags", ""),
                    "alt": hit.get("tags", query)
                })
            return results

        except Exception as e:
            print(f"Pixabay search failed: {e}")
            return []

    def search_images(self, query: str, count: int = 3) -> List[Dict]:
        """
        从所有可用平台搜索图片
        返回去重后的结果列表
        """
        all_results = []

        # 尝试所有平台
        all_results.extend(self.search_unsplash(query, count))
        all_results.extend(self.search_pexels(query, count))
        all_results.extend(self.search_pixabay(query, count))

        # 按相关性排序（这里简单用源的顺序，实际可以用更复杂的算法）
        # 去重（基于图片ID）
        seen_ids = set()
        unique_results = []
        for img in all_results:
            img_id = f"{img['source']}_{img['id']}"
            if img_id not in seen_ids:
                seen_ids.add(img_id)
                unique_results.append(img)

        return unique_results[:count]

    def search_article_images(self, title: str, tags: List[str], category: str, count: int = 3) -> List[Dict]:
        """
        根据文章信息搜索相关图片
        优先使用标签，其次使用标题关键词
        """
        # 中文到英文的关键词映射（AI/科技相关）
        keyword_mapping = {
            # AI 相关
            "AI": "artificial intelligence robot",
            "人工智能": "artificial intelligence robot",
            "机器学习": "machine learning neural network",
            "深度学习": "deep learning AI brain",
            "大模型": "large language model AI",
            "模型": "AI model neural network",
            "GPT": "AI chatbot conversation",
            "ChatGPT": "AI chatbot conversation",
            "Claude": "AI assistant chatbot",
            "DeepSeek": "artificial intelligence technology",
            "MiMo": "smartphone technology Xiaomi",
            "小米": "Xiaomi smartphone technology",
            # 价格相关
            "价格": "price tag sale discount",
            "降价": "price drop sale discount",
            "价格战": "price war competition business",
            "优惠": "discount offer sale",
            "促销": "sale promotion discount",
            "免费": "free gift present",
            # 技术相关
            "技术": "technology innovation digital",
            "科技": "technology digital innovation",
            "芯片": "chip processor semiconductor",
            "算力": "computing power server",
            "服务器": "server data center rack",
            "云计算": "cloud computing server",
            "API": "code programming developer",
            "开发者": "developer coding programmer",
            "程序员": "programmer laptop coding",
            # 产品相关
            "产品": "product launch announcement",
            "产品发布": "product launch announcement press",
            "发布": "product release launch",
            "更新": "software update upgrade",
            "升级": "upgrade improvement arrow",
            "手机": "smartphone mobile phone",
            "电脑": "computer laptop work",
            # 商业相关
            "商业": "business meeting office",
            "公司": "company office building",
            "创业": "startup business entrepreneur",
            "融资": "investment money finance",
            "市场": "market chart graph",
            "竞争": "competition race business",
        }

        # 构建搜索关键词（英文）
        keywords = []

        # 添加分类的英文映射
        if category:
            en_category = keyword_mapping.get(category, category)
            keywords.append(en_category)

        # 添加标签的英文映射（取前3个）
        for tag in tags[:3]:
            if tag and len(tag) > 1:
                en_tag = keyword_mapping.get(tag, tag)
                keywords.append(en_tag)

        # 如果关键词不够，添加通用的 AI/科技关键词
        if len(keywords) < 2:
            keywords.append("artificial intelligence technology")

        # 过滤掉可能找不到结果的关键词（太长或太具体）
        filtered_keywords = []
        for kw in keywords:
            # 如果关键词超过3个单词，只取前2个
            words = kw.split()
            if len(words) > 3:
                filtered_keywords.append(" ".join(words[:2]))
            else:
                filtered_keywords.append(kw)

        print(f"搜索关键词: {filtered_keywords}")

        # 搜索图片
        all_images = []
        for keyword in filtered_keywords[:2]:  # 最多用2个关键词搜索
            images = self.search_images(keyword, count=2)
            all_images.extend(images)

        # 去重
        seen_ids = set()
        unique_images = []
        for img in all_images:
            img_id = f"{img['source']}_{img['id']}"
            if img_id not in seen_ids:
                seen_ids.add(img_id)
                unique_images.append(img)

        return unique_images[:count]

    def download_image(self, image_info: Dict, filename: Optional[str] = None) -> Optional[Path]:
        """下载图片到本地"""
        try:
            url = image_info["url"]
            if not filename:
                # 生成文件名
                ext = ".jpg"
                filename = f"{image_info['source']}_{image_info['id']}{ext}"

            filepath = self.images_dir / filename

            # 下载图片
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 保存图片
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"下载成功: {filepath}")
            return filepath

        except Exception as e:
            print(f"下载失败: {e}")
            return None


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python search_images.py <关键词> [数量]")
        print("示例: python search_images.py 'AI 人工智能' 3")
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    searcher = ImageSearcher()
    results = searcher.search_images(query, count)

    print(f"\n找到 {len(results)} 张图片:")
    for i, img in enumerate(results, 1):
        print(f"{i}. [{img['source']}] {img['description'][:50]}...")
        print(f"   URL: {img['url']}")
        print(f"   作者: {img['author']}")
        print()


if __name__ == "__main__":
    main()
