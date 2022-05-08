from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.user import UserDAL
from app.crud.note import NoteDAL
from app.models.user import UserRead, UserCreate
from app.api.dependencies import get_current_superuser
from app.db.session import get_session

admin_router = router = APIRouter()


@router.get(
    "/admin/users/", response_model=List[UserRead]
)
async def read_all_users(current_superuser: UserRead = Depends(get_current_superuser),
                         session: AsyncSession = Depends(get_session)):
    user_dal = UserDAL(session)
    return await user_dal.read_users()


@router.post(
    "/admin/user/", response_model=UserRead
)
async def create_user(
        user: UserCreate,
        is_superuser: bool,
        current_superuser: UserRead = Depends(get_current_superuser),
        session: AsyncSession = Depends(get_session)):
    user_dal = UserDAL(session)
    return await user_dal.admin_create_user(user, current_superuser, is_superuser)


@router.put(
    "/admin/update_to_superuser/", response_model=UserRead
)
async def update_user_role(
        user_id: int,
        current_superuser: UserRead = Depends(get_current_superuser),
        session: AsyncSession = Depends(get_session)):
    user_dal = UserDAL(session)
    return await user_dal.update_to_superuser(user_id, current_superuser)


@router.delete(
    "/admin/user/{user_id}", response_model=UserRead
)
async def delete_user(
        user_id: int, current_superuser: UserRead = Depends(get_current_superuser),
        session: AsyncSession = Depends(get_session)):
    note_dal = NoteDAL(session)
    await note_dal.admin_delete_notes(user_id)
    user_dal = UserDAL(session)
    return await user_dal.admin_delete_user(user_id, current_superuser)
