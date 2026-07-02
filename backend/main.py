from fastapi import FastAPI

from config import settings

app = FastAPI()


@app.get("/health_check")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST_API, port=settings.PORT_API)
