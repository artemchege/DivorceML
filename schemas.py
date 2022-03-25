from typing import Optional
from pydantic import BaseModel, root_validator

from database import get_db
from models import User as UserModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Login(BaseModel):
    name: str
    password: str


class User(BaseModel):
    name: str
    email: str
    password: str

    @root_validator()
    def validate_that_email_does_not_exists(cls, values):
        email = values.get('email')

        db = next(get_db())
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if user is not None:
            raise ValueError(f'User with that email: {email} already exists')

        return values


class UserCreated(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
