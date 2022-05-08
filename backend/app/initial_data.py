from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL, FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD
from app.db.session import create_first_superuser
import asyncio


async def init() -> None:
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    session = async_session()
    await create_first_superuser(session)
    session.close()
    return


if __name__ == "__main__":
    print("Creating superuser")
    asyncio.run(init())
    print("Superuser created")
