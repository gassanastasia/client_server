from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class RequestBase(BaseModel):
    text: str = Field(..., max_length=500, example="Sample request text")
    request_date: str = Field(..., example="2023-12-19")
    request_time: str = Field(..., example="15:30:00")
    click_count: int = Field(..., ge=1, example=1)

    @validator('request_date')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

    @validator('request_time')
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, '%H:%M:%S')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM:SS format')

class RequestCreate(RequestBase):
    pass

class RequestResponse(BaseModel):
    id: int
    text: str
    request_date: str
    request_time: str
    click_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class RequestList(BaseModel):
    items: list[RequestResponse]
    total: int
    page: int
    pages: int
    per_page: int