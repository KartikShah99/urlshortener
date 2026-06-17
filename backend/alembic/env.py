from alembic import context
from sqlalchemy import create_engine
import os
import sys

sys.path.insert(0, "/app")

from database import Base

config = context.config

target_metadata = Base.metadata

def run_migrations_online():
    db_url = os.environ.get("DATABASE_URL", "").replace("postgresql+asyncpg", "postgresql")
    engine = create_engine(db_url)
    with engine.connect() as conn:
        context.configure(
            connection=conn,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
