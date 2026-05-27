#!/bin/bash

# 飞书文档保存脚本
# 用法: ./save_to_feishu.sh <文章标题> <文章文件路径> <封面图路径>

set -e

TITLE="$1"
ARTICLE_FILE="$2"
COVER_IMAGE="$3"

if [ -z "$TITLE" ] || [ -z "$ARTICLE_FILE" ]; then
    echo "用法: $0 <文章标题> <文章文件路径> [封面图路径]"
    exit 1
fi

echo "正在创建飞书文档: $TITLE"

# 读取文章内容
CONTENT=$(cat "$ARTICLE_FILE")

# 创建飞书文档（使用 Markdown 格式）
DOC_RESULT=$(npx @larksuite/cli docs +create --api-version v2 --title "$TITLE" --doc-format markdown --as bot --content "$CONTENT" 2>&1)

# 提取文档 URL
DOC_URL=$(echo "$DOC_RESULT" | grep -oP 'https://[^\s]+' | head -1)

if [ -z "$DOC_URL" ]; then
    echo "创建文档失败: $DOC_RESULT"
    exit 1
fi

echo "文档创建成功: $DOC_URL"

# 如果有封面图，插入到文档
if [ -n "$COVER_IMAGE" ] && [ -f "$COVER_IMAGE" ]; then
    echo "正在插入封面图..."
    npx @larksuite/cli docs +media-insert --doc "$DOC_URL" --file "$COVER_IMAGE" --as bot
    echo "封面图插入成功"
fi

echo "飞书文档保存完成: $DOC_URL"
