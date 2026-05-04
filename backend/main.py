from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.auth.service import ensure_default_admin
from src.core.config import get_settings
import src.core.database as db
from src.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await db.init_db()
    await db.create_db_and_tables()
    if db.async_session is None:
        raise RuntimeError("Database is not initialized. Call init_db() first.")
    async with db.async_session() as session:
        await ensure_default_admin(get_settings(), session)
    try:
        yield
    finally:
        await db.close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Jetson Facelock API",
        description="Backend API for Jetson Facelock user authentication and access control.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(users_router)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
