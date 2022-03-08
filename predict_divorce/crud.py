import datetime

from sqlalchemy.orm import Session

from predict_divorce.schemas import DivorceQuestions
from predict_divorce.models import DivorcePredictionRequest


def create_divorce_request(db: Session, divorce_request: DivorceQuestions):
    db_divorce_request = DivorcePredictionRequest(hate_subject=divorce_request.hate_subject.value,
                                                  happy=divorce_request.happy.value,
                                                  dreams=divorce_request.dreams.value,
                                                  freedom_value=divorce_request.freedom_value.value,
                                                  likes=divorce_request.likes.value,
                                                  calm_breaks=divorce_request.calm_breaks.value,
                                                  harmony=divorce_request.harmony.value,
                                                  roles=divorce_request.roles.value,
                                                  inner_world=divorce_request.inner_world.value,
                                                  current_stress=divorce_request.current_stress.value,
                                                  friends_social=divorce_request.friends_social.value,
                                                  contact=divorce_request.contact.value,
                                                  insult=divorce_request.insult.value,
                                                  created=datetime.datetime.now())
    db.add(db_divorce_request)
    db.commit()
    db.refresh(db_divorce_request)
    return db_divorce_request


def get_divorce_request(db: Session, divorce_id: int):
    return db.query(DivorcePredictionRequest).filter(DivorcePredictionRequest.id == divorce_id).first()
