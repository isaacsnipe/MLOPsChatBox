from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyobjectid import PyObjectId


class Document(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    conversation_id: str
    title: str
    uploaded_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "conversation_id": "123456789",
                "title": "title",
            }
        }
