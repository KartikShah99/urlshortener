from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from prometheus_fastapi_instrumentator import Instrumentator
from nanoid import generate
import redis.asyncio as aioredis
import os

from database import get_db
from models import URL
from worker import record_click

app = FastAPI(title="URL Shortener API")
Instrumentator().instrument(app).expose(app)

redis_client = aioredis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost:6379/0")
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/shorten")
async def shorten_url(payload: dict, db: AsyncSession = Depends(get_db)):
    original_url = payload.get("url")
    if not original_url:
        raise HTTPException(status_code=400, detail="url is required")
    short_code = generate(size=7)
    url_obj = URL(short_code=short_code, original_url=original_url)
    db.add(url_obj)
    await db.commit()
    await redis_client.setex(f"url:{short_code}", 3600, original_url)
    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    return {
        "short_code": short_code,
        "short_url": f"{base_url}/{short_code}"
    }

@app.get("/api/stats/{short_code}")
async def stats(short_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(URL).where(URL.short_code == short_code))
    url_obj = result.scalar_one_or_none()
    if not url_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "short_code": short_code,
        "original_url": url_obj.original_url,
        "clicks": url_obj.click_count
    }

@app.get("/{short_code}")
async def redirect_url(short_code: str, request: Request, db: AsyncSession = Depends(get_db)):
    cached = await redis_client.get(f"url:{short_code}")
    if cached:
        record_click.delay(
            short_code,
            request.headers.get("user-agent", ""),
            request.client.host if request.client else ""
        )
        return RedirectResponse(url=cached.decode(), status_code=302)

    result = await db.execute(select(URL).where(URL.short_code == short_code))
    url_obj = result.scalar_one_or_none()
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")

    await redis_client.setex(f"url:{short_code}", 3600, url_obj.original_url)
    record_click.delay(
        short_code,
        request.headers.get("user-agent", ""),
        request.client.host if request.client else ""
    )
    return RedirectResponse(url=url_obj.original_url, status_code=302)
