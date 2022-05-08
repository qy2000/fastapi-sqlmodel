from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import UserDAL
from app.models.token import Token
from app.models.user import UserCreate, UserRead
from app.core.auth import validate_user, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.session import get_session

auth_router = router = APIRouter()


@router.post("/register", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_dal = UserDAL(session)
    return await user_dal.create_user(user)


@router.post("/login", response_model=Token)
async def login(form_user_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await validate_user(session, form_user_data.username, form_user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
