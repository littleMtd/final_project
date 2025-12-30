# 💰 Personal Finance System

<div align="center">

![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

一個基於 **Django REST Framework** 與 **Vue 3** 構建的現代化個人財務管理系統。
支援記帳、數據視覺化、月報生成與目標追蹤，並內建完整的 Docker 開發/部署流程。

[✨ 特色](#-特色功能) • [🚀 快速開始](#-快速開始) • [🛠️ 技術棧](#%EF%B8%8F-技術棧) • [📖 API](#-api-概覽)

</div>

---

## ✨ 特色功能

* **  安全認證**：完整的註冊、登入、JWT 身份驗證機制。
* **  記帳管理**：直觀的收入/支出記錄，支援分頁查詢與 CRUD 操作。
* **  數據分析**：整合 ECharts 圖表（圓餅圖、趨勢圖）與分類排行。
* **  智慧洞察**：根據消費習慣自動產生建議與文字分析。
* **  目標追蹤**：設定每月預算與類別目標，即時監控進度。
* **  報表匯出 **：自動生成月度財務報表並支援 PDF 下載。

## 🛠️ 技術棧

| 類別 | 技術 | 說明 |
| :--- | :--- | :--- |
| **Frontend** | Vue 3, TypeScript | Composition API, Vite |
| **UI / Viz** | Tailwind CSS (假設), ECharts | 響應式介面與圖表 |
| **Backend** | Django 6, DRF | RESTful API 設計 |
| **Database** | SQLite / PostgreSQL | 預設 SQLite，易於替換 |
| **DevOps** | Docker, Nginx, Gunicorn | 容器化部署方案 |

## 🚀 快速開始

本專案建議使用 Docker 進行開發與部署。

### 前置需求
- Git
- Docker

### 1. 取得專案
```bash
git clone [https://github.com/your-username/frontend-backend.git](https://github.com/your-username/frontend-backend.git)
cd frontend-backend
```

### 2. 設定環境變數
於專案根目錄建立 `.env.dev` 檔案：

```ini
# frontend-backend/.env.dev
SECRET_KEY=django-insecure-dev-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_HTTPS=False
```

### 3. 啟動容器 (開發模式)
```bash
docker compose -f docker-compose.dev.yml up -d --build
```

### 4. 開始使用
* **前端頁面**: [http://localhost](http://localhost)
* **後端 API**: [http://localhost:8000](http://localhost:8000)

> 停止容器：`docker compose -f docker-compose.dev.yml down`

---

## 📂 專案結構

```
frontend-backend/
├── backend/                      # Django Server
│   ├── myapp/                    # App Logic & Models
│   └── Dockerfile
├── frontend/                     # Vue Client
│   ├── src/                      # Components & Views
│   └── Dockerfile
├── docker-compose.dev.yml        # 開發環境 (Hot-reload)
├── docker-compose.prod.cf.yml    # 生產（Cloudflare 反向代理）
└── docker-compose.prod.direct.yml# 生產（直連 Docker）
```

## ⚙️ 環境變數設定

主要由 Docker Compose 的 `env_file` 注入（建議放在專案根目錄）：
- 開發：`frontend-backend/.env.dev`
- 生產：`frontend-backend/.env.prod`
（也可在容器層級直接設定環境變數，或於後端使用其他 .env 管理方式）

| 變數名稱 | 說明 | 範例 |
| :--- | :--- | :--- |
| `SECRET_KEY` | Django 安全金鑰 (Prod 必填) | `django-secret-...` |
| `DEBUG` | 除錯模式 | `True` / `False` |
| `ALLOWED_HOSTS` | 允許的主機名稱 | `localhost,127.0.0.1` |
| `USE_HTTPS` | 是否啟用 HTTPS 設定 | `False` |
| `CSRF/CORS_...` | 跨域與來源信任清單 | `https://yourdomain.com` |

## 📦 生產環境部署

<details>
<summary>點擊展開生產環境部署指南</summary>

### 選項 1: Cloudflare Tunnel / Proxy (推薦)
適合使用 Cloudflare 處理 SSL 憑證的情境。

```bash
# 需準備 .env.prod
docker compose -f docker-compose.prod.cf.yml up -d --build
```

### 選項 2: 直接部署
直接暴露 Docker 服務。

```bash
docker compose -f docker-compose.prod.direct.yml up -d --build
```

</details>

## 💻 本機開發 (無 Docker)

若不使用 Docker，請分別啟動前後端：

**Backend**
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1 / Mac: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 📖 API 概覽

| 功能 | 方法 |路徑 |
| :--- | :--- | :--- |
| **Auth** | POST | `/api/signup/`, `/api/signin/` |(登入、註冊驗證)
| **Profile** | GET | `/api/me/` | (個人頁面)
| **Expense** | GET/POST | `/api/expense/`, `/api/income/` | (收入支出)
| **Ledger** | GET | `/api/ledger/` (明細查詢) |
| **Insight** | GET | `/api/insights/` | (建議)
| **Report** | POST | `/api/report/{YYYY-MM}` (產生月報) |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.