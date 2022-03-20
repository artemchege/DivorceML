import uvicorn
from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from predict_divorce.schemas import User, UserCreated
from database import get_db, Base, engine
from crud import create_user_in_db

app = FastAPI()
Base.metadata.create_all(engine)


@app.post('/user/', status_code=status.HTTP_201_CREATED, response_model=UserCreated, tags=['user'])
def create_user(user_request: User, db: Session = Depends(get_db)):
    user = create_user_in_db(user_request=user_request, db=db)
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)
