# GitHub Trending Top 10 飞书通知

每日定时抓取 GitHub Trending Top 10 仓库，发送飞书群消息卡片通知。

## 功能

- 抓取 GitHub Trending 每日 Top 10 仓库
- 飞书 Interactive Card 格式展示，含仓库跳转链接
- 发送失败自动重试（最多 3 次，指数退避）
- GitHub Actions 每日北京时间 9:00 自动执行

## 配置

### 1. 获取飞书 Webhook URL

1. 在飞书群中添加 **自定义机器人**
2. 复制 Webhook 地址，格式为：`https://open.feishu.cn/open-apis/bot/v2/hook/xxx`

### 2. 配置 GitHub Secrets

在你的 GitHub 仓库中：

1. 进入 **Settings → Secrets and variables → Actions**
2. 点击 **New repository secret**
3. Name: `FEISHU_WEBHOOK_URL`
4. Value: 粘贴你的飞书 Webhook URL

### 3. 推送代码

```bash
git init
git add .
git commit -m "feat: github trending monitor with feishu notification"
git remote add origin <your-repo-url>
git push -u origin main
```

## 本地运行

```bash
pip install -r requirements.txt
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx python -m src.main
```

## 手动触发

在 GitHub 仓库 **Actions → Daily GitHub Trending → Run workflow** 手动触发一次执行。

## 定时计划

- 默认每天北京时间 **9:00** 执行（UTC 1:00）
- 可在 `.github/workflows/daily-trending.yml` 中修改 `cron` 表达式
