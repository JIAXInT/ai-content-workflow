#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 图片生成脚本
使用 flow2api 生成文章配图
"""

import requests
import json
import base64
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class ImageGenerator:
    """AI 图片生成器"""

    def __init__(self, api_url: str = "http://localhost:38000", api_key: str = "han1234"):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.images_dir = Path("images")
        self.images_dir.mkdir(exist_ok=True)

    def generate_image(self, prompt: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        使用 flow2api 生成图片

        Args:
            prompt: 图片生成提示词
            filename: 保存的文件名

        Returns:
            生成的图片路径，失败返回 None
        """
        try:
            # 构建请求
            url = f"{self.api_url}/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gemini-3.1-flash-image-landscape",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            }

            print(f"Generating image with prompt: {prompt[:50]}...")
            response = requests.post(url, headers=headers, json=data, timeout=120)

            if response.status_code != 200:
                print(f"API error: {response.status_code} - {response.text}")
                return None

            # 解析响应
            result = response.json()

            # 提取图片数据
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                content = message.get("content", "")

                # 检查是否有图片数据
                if "parts" in message:
                    for part in message["parts"]:
                        if "inlineData" in part:
                            image_data = part["inlineData"].get("data", "")
                            if image_data:
                                return self._save_image(image_data, filename)

                # 尝试从 content 解析 base64
                if content and content.startswith("data:image"):
                    # 提取 base64 数据
                    base64_data = content.split(",")[1] if "," in content else content
                    return self._save_image(base64_data, filename)

            print("No image data found in response")
            return None

        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    def _save_image(self, base64_data: str, filename: Optional[str] = None) -> Optional[Path]:
        """保存 base64 图片到文件"""
        try:
            if not filename:
                date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ai_generated_{date_str}.png"

            filepath = self.images_dir / filename

            # 解码并保存
            image_bytes = base64.b64decode(base64_data)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            print(f"Image saved: {filepath}")
            return filepath

        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def generate_article_images(self, title: str, tags: List[str], category: str, count: int = 3) -> List[Dict]:
        """
        根据文章信息生成配图

        Args:
            title: 文章标题
            tags: 文章标签
            category: 文章分类
            count: 生成图片数量

        Returns:
            生成的图片信息列表
        """
        # 生成提示词
        prompts = self._generate_prompts(title, tags, category, count)

        generated_images = []
        for i, prompt in enumerate(prompts, 1):
            print(f"\nGenerating image {i}/{len(prompts)}...")
            filename = f"article_img_{datetime.now().strftime('%Y%m%d')}_{i}.png"
            filepath = self.generate_image(prompt, filename)

            if filepath:
                generated_images.append({
                    "path": filepath,
                    "prompt": prompt,
                    "source": "flow2api"
                })

        return generated_images

    def _generate_prompts(self, title: str, tags: List[str], category: str, count: int = 3) -> List[str]:
        """根据文章信息生成提示词"""
        # 分析文章主题
        is_ai_related = any(tag in ["AI", "人工智能", "大模型", "GPT", "DeepSeek", "MiMo"] for tag in tags)
        is_price_related = any(tag in ["价格", "降价", "价格战", "优惠"] for tag in tags)
        is_product_related = any(tag in ["产品", "发布", "更新", "手机", "小米"] for tag in tags)

        prompts = []

        # 根据文章内容生成不同风格的提示词
        if is_price_related and is_ai_related:
            # AI 价格相关文章
            prompts.extend([
                "A professional business chart showing a dramatic 99% price reduction, clean modern design with blue and green colors, suitable for a tech blog article, realistic data visualization style, no text overlay",
                "A smartphone displaying a pricing comparison app on its screen, placed on a modern office desk with a laptop and coffee, natural daylight from window, lifestyle photography style, warm and inviting atmosphere",
                "A minimalist infographic design showing two arrows - one pointing up labeled 'Value' and one pointing down labeled 'Price', modern flat design style, professional color palette of navy blue and coral, clean white background"
            ])

        elif is_product_related:
            # 产品相关文章
            prompts.extend([
                "A sleek modern smartphone on a clean white surface, surrounded by floating holographic UI elements showing price tags and discount symbols, soft studio lighting, product photography style, high-end commercial look",
                "A person's hands holding a smartphone in a bright, modern coffee shop, the screen showing a shopping app with special offers, blurred background with warm lighting, authentic lifestyle photography",
                "A flat lay photograph of tech accessories including a smartphone, wireless earbuds, and a smartwatch, arranged on a marble surface with subtle price tags, overhead shot, clean and organized composition"
            ])

        else:
            # 通用科技文章
            prompts.extend([
                "A modern data center with rows of server racks, blue LED lights glowing in the dark, cinematic lighting, wide angle shot showing the scale of the facility, professional photography",
                "A developer working at a desk with multiple monitors showing code and charts, natural office lighting, documentary style photography, focus on the screens with person slightly blurred",
                "An abstract visualization of digital data flow, streams of light blue particles moving through a dark space, creating patterns that suggest connectivity and innovation, artistic digital illustration"
            ])

        return prompts[:count]


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_images.py <prompt> [output_filename]")
        print("Example: python generate_images.py 'A beautiful sunset over mountains' sunset.png")
        sys.exit(1)

    prompt = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else None

    generator = ImageGenerator()
    result = generator.generate_image(prompt, filename)

    if result:
        print(f"\nSuccess! Image saved to: {result}")
    else:
        print("\nFailed to generate image")
        sys.exit(1)


if __name__ == "__main__":
    main()
