from datetime import datetime, timedelta
import os

from jose import JWTError, jwt

from schemas.token import TokenData

SECRET_KEY = "d29e9203-c999-4e75-9a52-ff62b319c82cdtget"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: str = payload.get("id")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
        return TokenData(id=id, email=email, role=role)
    except JWTError:
        raise credentials_exception
