# TrackingRequest

Веб-приложение для отслеживания заявок/запросов. Backend на FastAPI, frontend на React + TypeScript.

### Стек технологий:
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ВАШ_НИК_НА_GITHUB/TrackingRequest/ci.yml?branch=main&label=CI&style=flat-square)
![uv version](https://img.shields.io/badge/uv-v0.5+-007ec6?logo=python&style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white&style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white)

**Backend**
- Python 3.12
- FastAPI
- uv (управление зависимостями)
- Pydantic v2

**Frontend**
- React + TypeScript
- Vite
- ESLint

**Инфраструктура**
- Docker / Docker Compose
- Nginx (production сборка фронтенда)

## Структура проекта

```
TrackingRequest/
├── .github/workflows/     # CI/CD пайплайны
├── backend/
│   ├── config.py
│   ├── main.py
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── .env
├── docker-compose.yml
└── .env                   # переменные для docker-compose (порты)
```

## Запуск проекта

### Требования
- Docker и Docker Compose
- (для локальной разработки без Docker) Python 3.12+, uv, Node.js 20+

### Через Docker Compose

1. Создай `.env` в корне проекта:
```env
PORT_API=8000
PORT_WEB=3000
```

2. Создай `backend/.env` с настройками приложения:
```env
HOST_API=0.0.0.0
PORT_API=8000
```

3. Запусти:
```bash
docker compose up -d
```

Backend будет доступен на `http://localhost:8000`, frontend — на `http://localhost:3000`.

### Локальная разработка

**Backend:**
```bash
cd backend
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## CI/CD

Workflow в `.github/workflows/backend_build.yml` - выполнение CI перед pr в main