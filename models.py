from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session

from fastapi import status, HTTPException

from database import Base
from hashing import Hash


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    divorce_prediction_request = relationship('DivorcePredictionRequest', back_populates='creator')

    @classmethod
    def get_user_by_name_and_password(cls, name: str, password: str, db: Session):
        user = db.query(cls).filter(cls.name == name).first()
        if not user:
            raise HTTPException(detail=f'User does not exists', status_code=status.HTTP_400_BAD_REQUEST)

        if not Hash.verify(plain_password=password, hashed_password=user.password):
            raise HTTPException(detail=f'Invalid password', status_code=status.HTTP_400_BAD_REQUEST)

        return user

    def __repr__(self):
        return f'User obj with id: {self.id}'