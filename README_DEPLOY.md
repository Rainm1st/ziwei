# Ziwei Fortune URL Website

这是一个可部署的紫薇斗数 AI 解读网站 Demo。

## 本地运行

```bash
pip install -r requirements.txt
python app.py
```

打开：

```text
http://127.0.0.1:8000
```

## API 调用

```bash
curl -X POST http://127.0.0.1:8000/api/chart \
  -H "Content-Type: application/json" \
  -d '{"name":"小林","birth_date":"1990-01-15","birth_time":"14:30","gender":"男","address":"北京"}'
```

## 部署到 Render

1. 新建 GitHub 仓库，把本文件夹内容上传。
2. 打开 Render，选择 New Web Service。
3. 连接 GitHub 仓库。
4. 设置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. 部署完成后，Render 会给你一个 URL。

## 部署到云服务器

```bash
sudo apt update
sudo apt install -y python3-pip nginx
pip3 install -r requirements.txt
gunicorn -b 0.0.0.0:8000 app:app
```

然后用 Nginx 反向代理到 8000 端口，并绑定域名。

## 重要说明

当前版本是演示型产品：
- 已有网页表单
- 已有命盘生成
- 已有十二宫展示
- 已有 JSON API
- 可以部署成 URL

正式商用前建议继续升级：
- 完整紫薇斗数排盘算法
- 用户登录
- 历史报告保存
- PDF 报告导出
- AI 大模型深度解读
- 隐私政策与免责声明
