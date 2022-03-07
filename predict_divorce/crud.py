from sqlalchemy.orm import Session

from predict_divorce.schemas import DivorceQuestions
from predict_divorce.models import DivorcePredictionRequest


def create_divorce_request(db: Session, divorce_request: DivorceQuestions):
    db_divorce_request = DivorcePredictionRequest(hate_subject=divorce_request.hate_subject,
                                                  happy=divorce_request.happy,
                                                  dreams=divorce_request.dreams,
                                                  freedom_value=divorce_request.freedom_value,
                                                  likes=divorce_request.likes,
                                                  calm_breaks=divorce_request.calm_breaks,
                                                  harmony=divorce_request.harmony,
                                                  roles=divorce_request.roles,
                                                  inner_world=divorce_request.inner_world,
                                                  current_stress=divorce_request.current_stress,
                                                  friends_social=divorce_request.friends_social,
                                                  contact=divorce_request.contact,
                                                  insult=divorce_request.insult)
    db.add(db_divorce_request)
    db.commit()
    db.refresh(db_divorce_request)
    return db_divorce_request


def get_divorce_request(db: Session, divorce_id: int):
    return db.query(DivorcePredictionRequest).filter(DivorcePredictionRequest.id == divorce_id).first()
