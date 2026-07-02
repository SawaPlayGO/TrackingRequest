from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from utils.logging import logger
from database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await logger.ainfo("Application is starting up...", version="1.0.0")
    yield
    await logger.ainfo("Application is shutting down...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

@app.get("/health_check")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST_API, port=settings.PORT_API)
