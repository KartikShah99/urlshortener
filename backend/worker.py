from celery import Celery
import os

celery_app = Celery(
    "urlshortener",
    broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
)

@celery_app.task
def record_click(short_code: str, user_agent: str, ip_address: str):
    from sqlalchemy import create_engine, text
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg", "postgresql")
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO clicks (short_code, user_agent, ip_address) VALUES (:sc, :ua, :ip)"),
            {"sc": short_code, "ua": user_agent, "ip": ip_address}
        )
        conn.execute(
            text("UPDATE urls SET click_count = click_count + 1 WHERE short_code = :sc"),
            {"sc": short_code}
        )
        conn.commit()
