from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session

from fastapi import status, HTTPException

from database import Base
from hashing import Hash


class DivorcePredictionRequest(Base):
    __tablename__ = "divorce_prediction_request"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), onupdate=func.now())
    hate_subject = Column(Integer)
    happy = Column(Integer)
    dreams = Column(Integer)
    freedom_value = Column(Integer)
    likes = Column(Integer)
    calm_breaks = Column(Integer)
    harmony = Column(Integer)
    roles = Column(Integer)
    inner_world = Column(Integer)
    current_stress = Column(Integer)
    friends_social = Column(Integer)
    contact = Column(Integer)
    insult = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    creator = relationship('User', back_populates='divorce_prediction_request')


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

