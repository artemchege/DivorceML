from typing import List

from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from predict_divorce.schemas import DivorceQuestions
from predict_divorce.crud import create_divorce_request, get_divorce_request, list_divorce_request
from predict_divorce.services import get_divorce_prediction

router = APIRouter(
    tags=['divorce'],
    prefix='/predict_divorce'
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def predict(questions: DivorceQuestions, db: Session = Depends(get_db)):
    # todo: сделать только для авторизованных бюзеров
    create_divorce_request(db, questions)
    prediction = get_divorce_prediction(questions)
    return f'The result is: {prediction}'


@router.get('/', response_model=List[DivorceQuestions])
# todo: ограничить только авторизованным юзером
def return_divorce_requests(db: Session = Depends(get_db)):
    divorce_requests = list_divorce_request(db=db)
    return divorce_requests


@router.get('/{id}', response_model=DivorceQuestions)
# todo: ограничить только авторизованным юзером
def return_divorce_request(id: int, db: Session = Depends(get_db)):
    divorce_request = get_divorce_request(divorce_id=id, db=db)
    return divorce_request
