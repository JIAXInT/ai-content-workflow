# AI 内容创作工作流

## 项目概述
这是一个 AI 内容账号的每日创作工作流，覆盖公众号、小红书、抖音三端，支持自动保存到飞书文档。

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

### 第三步：生成公众号文章
用户确认选题后，使用 `khazix-writer` 技能生成公众号长文：
1. 基于选题素材，以「数字生命卡兹克」风格写作
2. 文章 4000-8000 字
3. 跑四层自检体系（L1 硬性规则 → L2 风格一致性 → L3 内容质量 → L4 活人感）
4. 输出质检报告

### 第四步：保存到飞书文档
文章生成后，自动保存到飞书文档：
1. 保存文章到本地：`articles/YYYY-MM-DD_标题.md`
2. 生成封面图：运行 `python scripts/screenshot.py`
3. 保存到飞书：运行 `python scripts/save_to_feishu.py "标题" "文章路径" "封面图路径"`
4. 输出飞书文档链接

### 第五步：多端适配（可选）
- 公众号：完整长文
- 小红书：提炼 3-5 个核心观点，配图文案
- 抖音：口播脚本或短视频文案

## 快捷命令
- `今日热点` / `AI 日报` → 拉取最新热点
- `写文章` → 基于已选热点生成公众号文章
- `质检` → 对已写文章跑四层自检
- `保存到飞书` → 将文章保存到飞书文档

## 飞书集成

### 前置条件
1. 安装飞书 CLI：`npm install -g @larksuite/cli`
2. 添加 skills：`npx skills add larksuite/cli -g -y`
3. 配置认证：`npx @larksuite/cli config init --new`
4. 登录授权：`npx @larksuite/cli auth login --recommend`
5. 启用权限：在飞书开发者后台启用 `docs:document.media:upload` 权限

### 使用方法
```bash
# 保存文章到飞书
python scripts/save_to_feishu.py "文章标题" "articles/YYYY-MM-DD_标题.md" "covers/cover-main.png"

# 测试飞书功能
python scripts/test_feishu_save.py
```

### 常见问题
- **认证过期**：运行 `npx @larksuite/cli auth login --recommend` 重新登录
- **权限不足**：在飞书开发者后台启用相应权限
- **编码问题**：确保脚本使用 `encoding='utf-8'` 参数
