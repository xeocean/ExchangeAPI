from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.db.models import Base

engine = create_async_engine(settings.url_db)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

