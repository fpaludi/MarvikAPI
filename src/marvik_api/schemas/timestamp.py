from pydantic import BaseModel


class TimestampMode(BaseModel):
    mode: bool


class TimestampResponse(BaseModel):
    timestamp: str
