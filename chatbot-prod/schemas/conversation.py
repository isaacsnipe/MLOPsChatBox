from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyobjectid import PyObjectId


class Conversation(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    title: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    started_at: datetime = datetime.now()
    ended_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "123456789",
            }
        }
