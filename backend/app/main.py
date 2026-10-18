from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import make_lifespan
from app.routers.indicators import router as indicator_router


def create_app(database_url: str | None = None) -> FastAPI:
    app = FastAPI(
        title="SII-MB · API local",
        description="Primer hito: registro y consulta de indicadores en borrador. No apto para producción.",
        version="0.1.0",
        lifespan=make_lifespan(database_url),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type"],
    )
    app.include_router(indicator_router)

    @app.get("/api/v1/health", tags=["health"])
    def health():
        return {"status": "ok", "environment": "local-development", "version": "0.1.0"}

    return app


app = create_app()
