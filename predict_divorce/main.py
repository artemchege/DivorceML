# from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from predict_divorce.schemas import DivorceQuestions
from predict_divorce.crud import create_divorce_request
from predict_divorce.models import Base
from predict_divorce.services import get_divorce_prediction

Base.metadata.create_all(engine)

app = FastAPI()


@app.post('/predict_divorce/')
def predict(questions: DivorceQuestions, db: Session = Depends(get_db)):
    create_divorce_request(db, questions)
    prediction = get_divorce_prediction(questions)
    return f'The result is: {prediction}'


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)

