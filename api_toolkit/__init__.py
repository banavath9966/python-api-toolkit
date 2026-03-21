"""
python-api-toolkit: Production-grade FastAPI toolkit.
"""
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import time
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthConfig(BaseModel):
    secret: str
    algorithm: str = "HS256"
    expire_minutes: int = 30


class CacheConfig(BaseModel):
    backend: str = "memory"
    url: Optional[str] = None
    ttl: int = 300


class RateLimitConfig(BaseModel):
    requests_per_minute: int = 60
    burst: int = 10


def create_app(
    auth: Optional[AuthConfig] = None,
    cache: Optional[CacheConfig] = None,
    rate_limit: Optional[RateLimitConfig] = None,
) -> FastAPI:
    """Create a pre-configured FastAPI application with production defaults."""
    app = FastAPI(
        title="API Toolkit App",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Store config
    app.state.auth = auth
    app.state.cache = cache or CacheConfig()
    app.state.rate_limit = rate_limit or RateLimitConfig()

    @app.middleware("http")
    async def log_requests(request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            },
        )
        return response

    @app.get("/health")
    async def health():
        return {"status": "ok", "timestamp": time.time()}

    return app
