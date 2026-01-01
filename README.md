# 💰 Personal Finance System

一個「直接能用」的記帳系統。前端用 Vue 3，後端用 Django REST Framework，已附好 Docker 讓你一鍵啟動。

- 想試跑：只要裝好 Docker，**一行指令複製設定 + 啟動**即可（不需要 Python、Node.js）。
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

## 2 分鐘快速啟動（Docker）
1) 下載專案
```bash
git clone https://github.com/littleMtd/final_project.git
cd frontend-backend
```

2) 複製環境設定檔
```bash
# Windows PowerShell
copy .env.dev.example .env.dev

# macOS / Linux
cp .env.dev.example .env.dev
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
- 我需要安裝 Python 嗎？
	- 不用。Docker 會處理所有環境，本機不需要裝 Python、Node.js 等。
- 我要用自己的資料庫嗎？
	- 不需要。預設用 SQLite。要換 PostgreSQL 就編輯 `.env.dev` 填 `DATABASE_URL`。
- Docker 啟動失敗怎麼辦？
	- 確認 Docker Desktop 已啟動，然後重試 `docker compose -f docker-compose.dev.yml up --build`。
- 想改 SECRET_KEY 怎麼辦？
	- 編輯 `.env.dev`，把 `SECRET_KEY=` 後面換成任何長隨機字串即可。

---

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
