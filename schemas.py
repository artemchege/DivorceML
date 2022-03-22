from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Login(BaseModel):
    name: str
    password: str
