import datetime

from sqlalchemy.orm import Session

from schemas import User as UserSchema
from models import User as UserModel
from hashing import Hash


def create_user_in_db(db: Session, user_request: UserSchema):
    user = UserModel(name=user_request.name, email=user_request.email, created=datetime.datetime.now(),
                     password=Hash.hash_password(user_request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(UserModel).filter(UserModel.name == name).first()
