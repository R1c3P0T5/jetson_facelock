from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.core.config import get_settings
from src.core.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = get_settings()
    await init_db()
    try:
        yield
    finally:
        await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
