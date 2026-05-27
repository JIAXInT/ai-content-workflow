#!/usr/bin/env python3
"""
测试飞书文档保存功能
"""

import subprocess
import sys
from pathlib import Path


def test_auth_status():
    """测试认证状态"""
    print("1. 检查飞书 CLI 认证状态...")
    result = subprocess.run(
        "npx @larksuite/cli auth status",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    if result.returncode == 0:
        print("   [OK] 认证状态正常")
        return True
    else:
        print(f"   [FAIL] 认证失败: {result.stderr}")
        return False


def test_create_doc():
    """测试创建文档"""
    print("\n2. 测试创建飞书文档...")

    test_content = """# 测试文档

这是一个测试文档，用于验证飞书 CLI 的文档创建功能。

## 测试内容

- 文档创建
- 格式化
- 中文支持

**测试完成！**
"""

    # 写入临时文件
    temp_file = Path("test_content.md")
    temp_file.write_text(test_content, encoding="utf-8")

    cmd = 'npx @larksuite/cli docs +create --api-version v2 --title "飞书CLI测试文档" --doc-format markdown --as bot --content "$(cat test_content.md)"'

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # 清理临时文件
    temp_file.unlink(missing_ok=True)

    if result.returncode == 0:
        # 提取文档 URL
        import re
        import json
        json_match = re.search(r'\{.*\}', result.stdout, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            if data.get("ok"):
                doc_url = data["data"]["document"]["url"]
                print(f"   [OK] 文档创建成功: {doc_url}")
                return doc_url

    print(f"   [FAIL] 文档创建失败: {result.stderr}")
    return None


def test_insert_media(doc_url):
    """测试插入媒体"""
    print("\n3. 测试插入封面图...")

    # 创建测试图片（简单文本文件）
    test_image = Path("test_cover.txt")
    test_image.write_text("测试封面图内容", encoding="utf-8")

    cmd = f'npx @larksuite/cli docs +media-insert --doc "{doc_url}" --file test_cover.txt --as bot'

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # 清理测试文件
    test_image.unlink(missing_ok=True)

    if result.returncode == 0:
        print("   [OK] 媒体插入成功")
        return True
    else:
        print(f"   [FAIL] 媒体插入失败: {result.stderr}")
        print("   [INFO]  需要在飞书开发者后台启用 docs:document.media:upload 权限")
        return False


def main():
    print("=" * 50)
    print("飞书文档保存功能测试")
    print("=" * 50)

    # 测试认证
    if not test_auth_status():
        print("\n[FAIL] 认证失败，请先运行: npx @larksuite/cli auth login --recommend")
        sys.exit(1)

    # 测试创建文档
    doc_url = test_create_doc()
    if not doc_url:
        print("\n[FAIL] 文档创建失败")
        sys.exit(1)

    # 测试插入媒体
    test_insert_media(doc_url)

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
    print(f"\n文档链接: {doc_url}")
    print("\n下一步:")
    print("1. 访问上面的文档链接，确认文档创建成功")
    print("2. 如果媒体插入失败，需要在飞书开发者后台启用权限:")
    print("   https://open.feishu.cn/page/scope-apply?clientID=cli_aa80d73f2df9dcd2&scopes=docs%3Adocument.media%3Aupload")


if __name__ == "__main__":
    main()
