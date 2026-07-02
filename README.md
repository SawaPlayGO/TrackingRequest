# TrackingRequest

Веб-приложение для отслеживания заявок/запросов. Backend на FastAPI, frontend на React + TypeScript.

## Стек

**Backend**
- Python 3.12
- FastAPI
- uv (управление зависимостями)
- JWT-авторизация (python-jose)
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