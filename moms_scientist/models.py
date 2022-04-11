from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class UserFile(Base):
    __tablename__ = "user_file"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), onupdate=func.now())
    path = Column(String, unique=True)
    name = Column(String, unique=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    file_creator = relationship('User', back_populates='user_file', lazy='subquery')

    def __repr__(self):
        return f'UserFile obj with id: {self.id}'
