from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from app.models.user import UserRead

# base model that others inherit from


class NoteBase(SQLModel):
    text: str
    completed: bool = Field(default=False)


# table model, so it's a pydantic and SQLAlchemy model and represents a database table.
class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[UserRead] = Relationship(
        back_populates="notes", sa_relationship_kwargs={"lazy": "selectin"})


# data only pydantic model
class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    text: Optional[str] = None
    completed: Optional[bool] = None
    owner_id: Optional[int]


class NoteRead(NoteBase):
    id: int
