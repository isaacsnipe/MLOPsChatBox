from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyobjectid import PyObjectId


class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    conversation_id: str
    prompt: str
    response: str
    sources: str
    page_number: str
    sent_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "conversation_id": "123456789",
                "prompt": "question",
                "response": "answer",
                "sources": "a,b,c",
                "page_number": "1,2,3",
            }
        }
