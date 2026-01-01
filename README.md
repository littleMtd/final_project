# 💰 Personal Finance System

一個「直接能用」的記帳系統。前端用 Vue 3，後端用 Django REST Framework，已附好 Docker 讓你一鍵啟動。

- 想試跑：只要裝好 Docker，就能 5 分鐘看到畫面。
- 想改程式：前後端程式碼都在專案裡，改完重建容器即可。

---

## 我會得到什麼？
- 記錄收入 / 支出，查看每月明細。
- 圓餅圖、趨勢圖，快速看分類花費。
- 產生月報，下載 PDF。
- 目標／預算追蹤，超支提醒。

## 開始之前你需要
- Git（用來下載專案）
- Docker（用來跑後端 + 前端）

---

## 5 分鐘快速啟動（Docker）
1) 下載專案
```bash
git clone https://github.com/littleMtd/final_project.git
cd frontend-backend
```

2) 準備設定檔（環境變數）
- 複製範本：
	- Windows PowerShell：`copy .env.example .env.dev`
	- macOS/Linux：`cp .env.example .env.dev`
- 生成一組隨機 SECRET_KEY（複製結果貼到 .env.dev 的 SECRET_KEY）：
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
- 最小內容示例（編輯 `.env.dev`）：
```ini
SECRET_KEY=在這裡貼上剛剛產生的字串
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_HTTPS=False
CORS_ALLOWED_ORIGINS_EXTRA=
CSRF_TRUSTED_ORIGINS_EXTRA=
# 留空就是用內建 SQLite；想用 PostgreSQL 就填：postgresql://USER:PASS@HOST:5432/DB
DATABASE_URL=
```

3) 啟動
```bash
docker compose -f docker-compose.dev.yml up -d --build
```

4) 打開瀏覽器
- 前端頁面：http://localhost
- 後端 API：http://localhost:8000

5) 想停掉的時候
```bash
docker compose -f docker-compose.dev.yml down
```

---

## 如果你不用 Docker
**後端（Django）**
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**前端（Vite）**
```bash
cd frontend
npm install
npm run dev
```
預設前端會用 Vite 的 dev server，後端在 8000 端口。

---

## 專案結構（看不懂也沒關係）
```
frontend-backend/
├── backend/           # 後端 Django 專案
├── frontend/          # 前端 Vue 專案
├── docker-compose.dev.yml        # 開發用 Docker 編排
├── docker-compose.prod.cf.yml    # 生產：Cloudflare 代理
└── docker-compose.prod.direct.yml# 生產：直接對外
```

---
## 常見問題
- SECRET_KEY 要填什麼？
	- 用上面的 python 指令生一組亂數，複製貼上即可。
- 我要用自己的資料庫嗎？
	- 不需要。留空就會自動用 SQLite。要換 PostgreSQL 就把 `DATABASE_URL` 填好。
- Docker 啟動失敗怎麼辦？
	- 先確認 `.env.dev` 有填 SECRET_KEY，然後重新 `docker compose -f docker-compose.dev.yml up --build`。

---

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
