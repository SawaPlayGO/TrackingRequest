from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers.ticket_routers import router as ticket_router
from routers.admin_routers import router as admin_router
from utils.logging import logger
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await logger.ainfo("Application is starting up...")
    yield
    await logger.ainfo("Application is shutting down...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)
app.include_router(ticket_router)
app.include_router(admin_router)


@app.get("/health_check")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST_API, port=settings.PORT_API)
