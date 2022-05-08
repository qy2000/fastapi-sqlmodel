from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class UserBase(SQLModel):
    first_name: str
    last_name: str
    username: str
    age: Optional[int] = None
    is_superuser: bool = Field(default=False)


# table model, so it's a pydantic and SQLAlchemy model and represents a database table.
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(
        nullable=False, index=True
    )
    notes: List["Note"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "delete",  # Instruct the ORM how to track changes to local objects
        },
    )


# data only pydantic models
class UserCreate(UserBase):
    hashed_password: str


class UserRead(UserBase):
    id: int
