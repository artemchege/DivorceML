# from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from predict_divorce.schemas import DivorceQuestions
from predict_divorce.crud import create_divorce_request
from predict_divorce.models import Base

Base.metadata.create_all(engine)

app = FastAPI()


@app.post('/predict_divorce/', response_model=DivorceQuestions)
def predict(questions: DivorceQuestions, db: Session = Depends(get_db)):
    db_divorce_request = create_divorce_request(db, questions)
    # TODO: здесь достать prediction из skit learn
    return db_divorce_request


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)




