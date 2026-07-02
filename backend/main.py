from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from routers.ticket_routers import router as ticket_router
from utils.logging import logger
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await logger.ainfo("Application is starting up...")
    yield
    await logger.ainfo("Application is shutting down...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(ticket_router)


@app.get("/health_check")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST_API, port=settings.PORT_API)
