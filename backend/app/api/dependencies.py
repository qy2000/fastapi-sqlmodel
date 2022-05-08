from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.models.token import TokenData
from app.core.auth import oauth2_scheme
from app.core.config import SECRET_KEY, ALGORITHM
from app.crud.user import UserDAL
from app.db.session import get_session


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user_dal = UserDAL(session)
    user = await user_dal.read_user_by_username(username=token_data.username)
    if not user:
        raise credentials_exception

    return user


async def get_current_superuser(current_user=Depends(get_current_user),):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
