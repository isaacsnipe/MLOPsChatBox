from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyobjectid import PyObjectId


class Roles(Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    password: str
    role: Roles = Roles.USER
    created_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "janedoe",
                "email": "jdoe@example.com",
                "password": "password",
            }
        }
