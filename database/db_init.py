import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base


def create_async_my_engine(url):
    return create_async_engine(url, echo=False, future=True, pool_pre_ping=True)


def create_async_session(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables(engine):
    """
    Создает таблицы в БД.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine):
    """
    Удаляет таблицы из БД.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

postgres_url = URL.create(
    "postgresql+asyncpg",
    username=POSTGRES_USER,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT,
)

# Создание движка для всего проекта
async_engine = create_async_my_engine(postgres_url)

# Создание сессии для всего проекта
async_session = create_async_session(async_engine)


# asyncio.run(create_tables(async_engine))
# asyncio.run(drop_tables(async_engine))
