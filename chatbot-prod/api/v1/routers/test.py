from fastapi import APIRouter, Depends

from core.oauth2 import get_current_user
from schemas.user import User

router = APIRouter()


@router.get("/")
async def test_get(current_user: User = Depends(get_current_user)):
    print(current_user)
    return {"Hello": "World"}
