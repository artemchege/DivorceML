from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float
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
    trained_model = relationship('TrainedModel', back_populates='user_file_trained_model')

    def __repr__(self):
        return f'UserFile obj with id: {self.id}'


class TrainedModel(Base):
    __tablename__ = "trained_model"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    path = Column(String, unique=True)

    user_file_id = Column(Integer, ForeignKey('user_file.id'), nullable=False)
    user_file_trained_model = relationship('UserFile', back_populates='trained_model', lazy='subquery')

    def __repr__(self):
        return f'TrainedModel obj with {self.id=}, {self.name=}'
