from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    forename: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: Optional[str] = Field(max_length=50)
    phone_number: str = Field(max_length=20)
    born_date: date


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
