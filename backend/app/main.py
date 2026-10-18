import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.db import make_lifespan
from app.routers.indicators import router as indicator_router
from app.routers.analysis import router as analysis_router
from app.routers.auth import router as auth_router
from app.routers.workspace import router as workspace_router


def create_app(database_url: str | None = None) -> FastAPI:
    origins = os.getenv("SII_MB_UI_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    app = FastAPI(
        title="SII-MB · API local",
        description="Fuentes sintéticas, métodos declarativos y resultados reproducibles. Desarrollo local.",
        version="0.2.0",
        lifespan=make_lifespan(database_url),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type"],
        allow_credentials=True,
    )
    @app.middleware("http")
    async def local_protection(request: Request, call_next):
        origin = request.headers.get("origin")
        if request.method not in ("GET", "HEAD", "OPTIONS") and origin and origin not in origins:
            return JSONResponse({"detail": "Origen no permitido"}, status_code=403)
        if request.method in ("POST", "PATCH", "PUT"):
            length = request.headers.get("content-length", "0")
            if not length.isdigit() or int(length) > 2_000_000:
                return JSONResponse({"detail": "Solicitud demasiado grande"}, status_code=413)
            size = 0
            chunks = []
            async for chunk in request.stream():
                size += len(chunk)
                if size > 2_000_000:
                    return JSONResponse({"detail": "Solicitud demasiado grande"}, status_code=413)
                chunks.append(chunk)
            request._body = b"".join(chunks)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Frame-Options"] = "DENY"
        return response
    app.include_router(indicator_router)
    app.include_router(analysis_router)
    app.include_router(auth_router)
    app.include_router(workspace_router)

    @app.get("/api/v1/health", tags=["health"])
    def health():
        return {"status": "ok", "environment": "local-development", "version": "0.2.0"}

    return app


app = create_app()
