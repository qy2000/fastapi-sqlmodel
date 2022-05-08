from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.note import NoteDAL
from app.models.user import UserRead
from app.models.note import NoteRead, NoteCreate, NoteUpdate
from app.api.dependencies import get_current_user
from app.db.session import get_session

from typing import List

note_router = router = APIRouter()


@router.get(
    "/notes", response_model=List[NoteRead]
)
async def read_notes(current_user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    note_dal = NoteDAL(session)
    return await note_dal.read_notes()


@router.get(
    "/note/{note_id}",
    response_model=NoteRead,
)
async def read_note(
    note_id: int, current_user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    note_dal = NoteDAL(session)
    return await note_dal.read_note(note_id)


@router.post(
    "/note",
    response_model=NoteRead,
)
async def create_note(
    note: NoteCreate, current_user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    note_dal = NoteDAL(session)
    return await note_dal.create_note(note, current_user)


@router.put(
    "/note/{note_id}"
)
async def update_note(
    note_id: int, note: NoteUpdate, current_user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    note_dal = NoteDAL(session)
    return await note_dal.update_note(note_id, note, current_user)


@router.delete(
    "/note/{note_id}",
    response_model=NoteRead,
)
async def delete_note(
    note_id: int, current_user: UserRead = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    note_dal = NoteDAL(session)
    return await note_dal.delete_note(note_id, current_user)
