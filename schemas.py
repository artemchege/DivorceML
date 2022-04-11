from typing import Optional
from pydantic import BaseModel, root_validator

from models import User as UserModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Login(BaseModel):
    email: str
    password: str


class User(BaseModel):
    name: str
    email: str
    password: str

    @root_validator()
    def validate_that_email_does_not_exists(cls, values):
        email = values.get('email')
        exists = UserModel.check_if_user_with_given_email_exists(email=email)
        if exists:
            raise ValueError(f'User with that email: {email} already exists')
        return values


class UserCreated(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
