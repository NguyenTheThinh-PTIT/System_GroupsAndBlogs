from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str

class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True