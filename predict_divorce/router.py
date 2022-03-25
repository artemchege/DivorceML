from typing import List

from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from predict_divorce.schemas import DivorceQuestionsShow, DivorceQuestionsCreate
from schemas import User
from predict_divorce.crud import create_divorce_request, get_divorce_request, list_divorce_requests
from predict_divorce.services import get_divorce_prediction
from jwt import get_current_user

router = APIRouter(
    tags=['divorce'],
    prefix='/predict_divorce'
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def predict(questions: DivorceQuestionsCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    create_divorce_request(db=db, divorce_request=questions, user=user)
    prediction = get_divorce_prediction(questions)
    return f'The result is: {prediction}'


@router.get('/', response_model=List[DivorceQuestionsCreate])
def return_divorce_requests(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    divorce_requests = list_divorce_requests(db=db, user=user)
    return divorce_requests


@router.get('/{id}', response_model=DivorceQuestionsShow)
def return_divorce_request(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    divorce_request = get_divorce_request(divorce_id=id, db=db, user=user)
    return divorce_request
