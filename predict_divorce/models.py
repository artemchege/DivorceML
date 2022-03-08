from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from database import Base


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

