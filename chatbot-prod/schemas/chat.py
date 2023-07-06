from typing import List

from pydantic import BaseModel


class ChatOut(BaseModel):
    prompt: str
    response: str
    sources: list
    page_number: list
