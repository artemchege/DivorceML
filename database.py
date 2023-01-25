import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '1234')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'fastapi')

# Async setup
ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                          f"@db:{POSTGRES_PORT}/{POSTGRES_DB}"


async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session_local = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


# Sync setup
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                          f"@db:{POSTGRES_PORT}/{POSTGRES_DB}"
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL, )
sync_session_local = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False,)

dsn = f'dbname = {POSTGRES_DB} user = {POSTGRES_USER} password = {POSTGRES_PASSWORD} host = db'

Base = declarative_base()


def get_sync_db():
    db = sync_session_local()
    try:
        yield db
    finally:
        db.close()
