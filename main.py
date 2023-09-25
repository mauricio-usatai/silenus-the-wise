from fastapi import FastAPI

from settings import Settings
from apps.routers.v0 import model_serving


settings = Settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(model_serving.router)


@app.get("/")
async def root():
    """Api version"""
    return {"version": settings.APP_VERSION}
