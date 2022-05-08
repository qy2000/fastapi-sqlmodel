from sqlmodel import SQLModel
from typing import Optional


# data only pydantic models
class TokenData(SQLModel):
    username: Optional[str] = None


class Token(SQLModel):
    access_token: str
    token_type: str
