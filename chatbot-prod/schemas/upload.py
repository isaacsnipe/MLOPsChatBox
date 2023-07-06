from typing import List

from pydantic import BaseModel


class UploadOut(BaseModel):
    info: str
