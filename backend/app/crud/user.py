from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserCreate, UserRead
from app.core.security import get_password_hash


class UserDAL():
    """
    Data access layer to perform CRUD operations on Note
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_users(self):
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        return [UserRead.from_orm(user) for user in users]

    async def read_user_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def read_user_by_username(self, username: int):
        query = select(User).where(User.username == username)
        results = await self.session.execute(query)
        user = results.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_user(self, user: UserCreate):
        query = select(User).where(User.username == user.username)
        results = await self.session.execute(query)
        user_in_db = results.scalars().first()
        if not user_in_db:
            hashed_password = get_password_hash(user.hashed_password)
            user.hashed_password = hashed_password
            db_user = User.from_orm(user)
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Username exists")

    async def admin_create_user(self, user: UserCreate, current_user: UserRead, is_superuser: bool):
        if not current_user.is_superuser:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="User is not a superuser")

        query = select(User).where(User.username == user.username)
        results = await self.session.execute(query)
        user_in_db = results.scalars().first()
        if not user_in_db:
            hashed_password = get_password_hash(user.hashed_password)
            user.hashed_password = hashed_password
            user.is_superuser = is_superuser
            db_user = User.from_orm(user)
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user

        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Username exists")

    async def update_to_superuser(self, user_id: int, current_user: UserRead):
        if not current_user.is_superuser:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="User is not a superuser")
        db_user = await self.read_user_by_id(user_id)
        if not db_user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="user not found")

        db_user.is_superuser = True
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int, current_user: UserRead):
        user = await self.read_user_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if user_id == current_user.id:
            await self.session.delete(user)
            await self.session.commit()
            return user

        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete")

    async def admin_delete_user(self, user_id: int, current_user: UserRead):
        if not current_user.is_superuser:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="User is not a superuser")

        user = await self.read_user_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        await self.session.delete(user)
        await self.session.commit()
        return user
