from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session

from fastapi import status, HTTPException

from database import Base, get_sync_db
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
    def get_user_by_email_and_password(cls, email: str, password: str, db: Session):
        user = db.query(cls).filter(cls.email == email).first()
        if not user:
            raise HTTPException(detail=f'User does not exists', status_code=status.HTTP_400_BAD_REQUEST)

        if not Hash.verify(plain_password=password, hashed_password=user.password):
            raise HTTPException(detail=f'Invalid password', status_code=status.HTTP_400_BAD_REQUEST)

        return user

    @classmethod
    def check_if_user_with_given_email_exists(cls, email: str) -> bool:
        db = next(get_sync_db())
        user = db.query(cls).filter(cls.email == email).first()
        return True if user else False

    def __repr__(self):
        return f'User obj with id: {self.id}'
