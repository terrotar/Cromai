
from pydantic import BaseModel


class Message(BaseModel):
    filename: str
    message: str
