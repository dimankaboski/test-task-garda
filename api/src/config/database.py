from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config.base import base_config

engine = create_async_engine(base_config.DATABASE_URL_asyncpg)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(base_config.DATABASE_URL_psycopg)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
