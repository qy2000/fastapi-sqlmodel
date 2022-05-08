from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRead
from app.models.note import Note, NoteCreate, NoteRead, NoteUpdate
from datetime import datetime


class NoteDAL():
    """
    Data access layer to perform CRUD operations on Note
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_notes(self):
        result = await self.session.execute(select(Note))
        notes = result.scalars().all()
        return [NoteRead.from_orm(note) for note in notes]

    async def read_note(self, note_id: int):
        query = select(Note).where(Note.id == note_id)
        result = await self.session.execute(query)
        note = result.scalars().first()
        if not note:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="Note not found")
        return note

    async def create_note(self, note: NoteCreate, current_user: UserRead):
        db_note = Note.from_orm(note)
        db_note.owner = current_user
        db_note.owner_id = current_user.id
        db_note.created_at = datetime.utcnow()
        db_note.updated_at = datetime.utcnow()
        self.session.add(db_note)
        await self.session.commit()
        await self.session.refresh(db_note)
        return db_note

    async def update_note(self, note_id: int, note: NoteUpdate, current_user: UserRead):
        db_note = await self.read_note(note_id)
        if not db_note:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="note not found")
        if note.owner_id == current_user.id:
            note_update_data = note.dict(exclude_unset=True)
            for key, value in note_update_data.items():
                setattr(db_note, key, value)
        self.session.add(db_note)
        await self.session.commit()
        await self.session.refresh(db_note)
        return db_note

    async def delete_note(self, note_id: int, current_user: UserRead):
        note = await self.read_note(note_id)

        if not note:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="Note not found")

        if note.owner_id == current_user.id:
            await self.session.delete(note)
            await self.session.commit()
            return note

    async def delete_notes(self, current_user: UserRead):
        return await self.session.execute(delete(Note).where(Note.owner_id == current_user.id))

    async def admin_delete_notes(self, user_id: int):
        return await self.session.execute(delete(Note).where(Note.owner_id == user_id))
