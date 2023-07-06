from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core import authToken
from core.config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return authToken.verify_token(data, credentials_exception)
