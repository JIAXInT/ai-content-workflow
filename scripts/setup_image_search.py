#!/usr/bin/env python3
"""
图片搜索配置脚本
帮助用户配置免费图片平台的 API key
"""

import json
import os
from pathlib import Path


def check_config():
    """检查当前配置状态"""
    config_path = Path(__file__).parent.parent / "config" / "image_api_keys.json"

    print("=== 图片搜索配置检查 ===\n")

    if not config_path.exists():
        print("配置文件不存在: config/image_api_keys.json")
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        print("当前配置状态:")
        print(f"  Unsplash: {'✓ 已配置' if config.get('unsplash_access_key') else '✗ 未配置'}")
        print(f"  Pexels:   {'✓ 已配置' if config.get('pexels_api_key') else '✗ 未配置'}")
        print(f"  Pixabay:  {'✓ 已配置' if config.get('pixabay_api_key') else '✗ 未配置'}")

        return config

    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return None


def setup_config():
    """交互式配置 API key"""
    print("\n=== 图片搜索配置向导 ===\n")

    config_path = Path(__file__).parent.parent / "config" / "image_api_keys.json"

    # 读取现有配置
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    print("请配置以下图片平台的 API key（直接回车跳过）:\n")

    # Unsplash
    print("1. Unsplash (https://unsplash.com/developers)")
    print("   免费额度: 50请求/小时")
    unsplash_key = input("   Access Key: ").strip()
    if unsplash_key:
        config["unsplash_access_key"] = unsplash_key

    # Pexels
    print("\n2. Pexels (https://www.pexels.com/api/)")
    print("   免费额度: 200请求/小时")
    pexels_key = input("   API Key: ").strip()
    if pexels_key:
        config["pexels_api_key"] = pexels_key

    # Pixabay
    print("\n3. Pixabay (https://pixabay.com/api/docs/)")
    print("   免费额度: 100请求/分钟")
    pixabay_key = input("   API Key: ").strip()
    if pixabay_key:
        config["pixabay_api_key"] = pixabay_key

    # 保存配置
    if config:
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"\n配置已保存到: {config_path}")
        print("\n配置完成! 现在可以使用图片搜索功能了。")
    else:
        print("\n未配置任何 API key")


def show_help():
    """显示帮助信息"""
    print("""
=== 图片搜索配置帮助 ===

图片搜索功能支持以下免费图片平台:

1. Unsplash
   - 网站: https://unsplash.com/developers
   - 免费额度: 50请求/小时
   - 特点: 高质量摄影作品，支持按尺寸调整

2. Pexels
   - 网站: https://www.pexels.com/api/
   - 免费额度: 200请求/小时
   - 特点: 丰富的图片库，支持多种尺寸

3. Pixabay
   - 网站: https://pixabay.com/api/docs/
   - 免费额度: 100请求/分钟
   - 特点: 图片、插图、矢量图等多种类型

配置方法:
1. 访问上述网站注册账号
2. 获取 API key
3. 运行本脚本或手动编辑 config/image_api_keys.json

配置文件格式:
{
  "unsplash_access_key": "your_key_here",
  "pexels_api_key": "your_key_here",
  "pixabay_api_key": "your_key_here"
}

注意: 至少配置一个平台的 API key 即可使用图片搜索功能。
""")


def main():
    """主函数"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_help()
        return

    print("图片搜索配置工具\n")

    # 检查当前配置
    config = check_config()

    if config and any(config.values()):
        print("\n已有配置。")
        choice = input("是否重新配置? (y/N): ").strip().lower()
        if choice != 'y':
            return

    # 开始配置
    setup_config()


if __name__ == "__main__":
    main()
