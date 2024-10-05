from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserDB
from app.api.schemas.user import User
from app.db.database import get_async_session
from app.core.security import hashed_password, verify_password, encode_jwt

router_user = APIRouter(prefix="/auth", tags=["Authorization"])


@router_user.post("/register")
async def register(user: User, session: AsyncSession = Depends(get_async_session)) -> dict:
    query = select(UserDB).where(UserDB.username == user.username)
    result = await session.execute(query)
    exist_user = result.scalar_one_or_none()

    if exist_user:
        raise HTTPException(status_code=400, detail="Username exists")

    hash_passwd = hashed_password(user.password)
    new_user = UserDB(
        username=user.username,
        password=hash_passwd
    )
    session.add(new_user)
    await session.commit()
    return {"message": "Registration successful, please log in"}


@router_user.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    query = select(UserDB).where(UserDB.username == form_data.username)
    result = await session.execute(query)
    user_db = result.scalar_one_or_none()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = encode_jwt(user_db.username)
    return {"access_token": token, "token_type": "bearer"}
