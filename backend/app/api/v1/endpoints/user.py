from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import UserDAL
from app.crud.note import NoteDAL
from app.models.user import UserRead
from app.api.dependencies import get_current_user
from app.db.session import get_session

user_router = router = APIRouter()


@router.get(
    "/users/whoami", response_model=UserRead
)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@router.delete(
    "/user/{user_id}"
)
async def delete_user(
    user_id: int, current_user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    note_dal = NoteDAL(session)
    await note_dal.delete_notes(current_user)
    user_dal = UserDAL(session)
    return await user_dal.delete_user(user_id, current_user)
