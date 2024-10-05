from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_passwd: str) -> str:
    return pwd_context.verify(password, hash_passwd)


def encode_jwt(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=int(settings.expire))
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm)


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, key=settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
