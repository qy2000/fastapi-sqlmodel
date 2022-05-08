from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.crud.user import UserDAL
from app.models.user import UserCreate

from app.core.config import DATABASE_URL, FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD
from app.core.security import get_password_hash

"""
Initialize a new SQLAlchemy engine using create_engine from SQLModel
"""

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def init_db():
    """
    Initialize a new database
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Create a SQLAlchemy async session
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def create_first_superuser(session):
    user_dal = UserDAL(session)
    user_in = UserCreate(
        first_name=FIRST_SUPERUSER,
        last_name=FIRST_SUPERUSER,
        username=FIRST_SUPERUSER,
        hashed_password=FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    return await user_dal.create_user(user_in)
