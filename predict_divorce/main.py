from typing import List

import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from predict_divorce.schemas import DivorceQuestions
from predict_divorce.crud import create_divorce_request
from predict_divorce.models import Base, DivorcePredictionRequest
from predict_divorce.services import get_divorce_prediction

Base.metadata.create_all(engine)

app = FastAPI()


@app.post('/predict_divorce/', status_code=status.HTTP_201_CREATED)
def predict(questions: DivorceQuestions, db: Session = Depends(get_db)):
    # todo: сделать только для авторизованных бюзеров
    create_divorce_request(db, questions)
    prediction = get_divorce_prediction(questions)
    return f'The result is: {prediction}'


@app.get('/return_divorce_requests/', response_model=List[DivorceQuestions])
# todo: ограничить только авторизованным юзером
def return_divorce_requests(db: Session = Depends(get_db)):
    divorce_requests = db.query(DivorcePredictionRequest).all()
    if not divorce_requests:
        raise HTTPException(detail=f'objs were not found', status_code=status.HTTP_404_NOT_FOUND)
    return divorce_requests


@app.get('/return_divorce_request/{id}', response_model=DivorceQuestions)
# todo: ограничить только авторизованным юзером
def return_divorce_request(id: int, db: Session = Depends(get_db)):
    divorce_request = db.query(DivorcePredictionRequest).filter(DivorcePredictionRequest.id == id).first()
    if not divorce_request:
        raise HTTPException(detail=f'obj with id: {id} was not found', status_code=status.HTTP_404_NOT_FOUND)
    return divorce_request


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)

