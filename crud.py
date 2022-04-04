import datetime
from typing import Union

from sqlalchemy.future import select

from schemas import User as UserSchema
from models import User as UserModel
from hashing import Hash
from database import async_session_local


async def create_user_in_db(user_request: UserSchema):
    async with async_session_local() as session:
        async with session.begin():
            user = UserModel(name=user_request.name, email=user_request.email, created=datetime.datetime.now(),
                             password=Hash.hash_password(user_request.password))
            session.add(user)
            await session.flush()
            return user


async def get_user_by_id(user_id: int):
    async with async_session_local() as session:
        async with session.begin():
            db_request = await session.execute(select(UserModel).where(UserModel.id == user_id))
            user = db_request.one_or_none()
            if user is not None:
                (user,) = user
            return user


async def get_user_by_name(name: str) -> Union[None, UserModel]:
    async with async_session_local() as session:
        async with session.begin():
            db_request = await session.execute(select(UserModel).where(UserModel.name == name))
            user = db_request.one_or_none()
            if user is not None:
                (user,) = user
            return user
