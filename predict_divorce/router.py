from typing import List

from fastapi import Depends, status, APIRouter

from predict_divorce.schemas import DivorceQuestionsShow, DivorceQuestionsCreate, PredictionResponse
from schemas import User
from predict_divorce.crud import create_divorce_request, get_divorce_request, list_divorce_requests
from predict_divorce.services import get_divorce_prediction
from jwt import get_current_user

router = APIRouter(
    tags=['divorce'],
    prefix='/predict_divorce'
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PredictionResponse)
async def async_predict(questions: DivorceQuestionsCreate, user: User = Depends(get_current_user)):
    prediction = get_divorce_prediction(questions)
    await create_divorce_request(divorce_request=questions, prediction=prediction, user=user)
    return {'prediction': prediction}


@router.get('/', response_model=List[DivorceQuestionsShow])
async def async_return_divorce_requests(user: User = Depends(get_current_user)):
    divorce_requests = await list_divorce_requests(user=user)
    return divorce_requests


@router.get('/{id}', response_model=DivorceQuestionsShow)
async def async_return_divorce_request(id: int, user: User = Depends(get_current_user)):
    divorce_request = await get_divorce_request(divorce_id=id, user=user)
    return divorce_request
