from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from core import authToken
from core.database import db
from core.hashing import hash_bcrypt, hash_verify
from schemas.user import User

router = APIRouter()


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"email": request.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )
    if not hash_verify(user["password"], request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    access_token = authToken.create_access_token(
        data={"id": user["_id"], "sub": user["email"], "role": user["role"]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user["_id"],
        "email": user["email"],
    }


@router.post("/register")
async def register_user(request: User):
    # Check if email is already used
    user = await db.users.find_one({"email": request.email})
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken"
        )

    # Check if username is already used
    username = await db.users.find_one({"username": request.username})
    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create user
    new_user = User(
        username=request.username,
        email=request.email,
        password=hash_bcrypt(request.password),
        created_at=datetime.now(),
    )

    new_user = jsonable_encoder(new_user)

    await db.users.insert_one(new_user)
    access_token = authToken.create_access_token(
        data={"id": new_user["_id"], "sub": new_user["email"], "role": new_user["role"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": new_user["_id"],
        "email": new_user["email"],
    }  # new_user


@router.get("/logout")
async def logout_user():
    pass
