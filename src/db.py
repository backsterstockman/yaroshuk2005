from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated
from src.config import get_database_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


intpk = Annotated[int, mapped_column(primary_key=True)]


DATABASE_URL = get_database_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class BaseCRUD:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create(cls, obj):
        async with async_session_maker() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def delete(cls, obj):
        async with async_session_maker() as session:
            session.delete(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def update_by_id(cls, id, new_obj):
        async with async_session_maker() as session:
            obj = session.query(cls.model).get(id)
            obj = new_obj
            await session.commit()
            return obj

    @classmethod
    async def get_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == id)
            obj = await session.execute(query)
            return obj.scalar_one_or_none()
