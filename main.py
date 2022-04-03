import uvicorn
from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from schemas import Login, User, UserCreated, Token
from database import get_sync_db
from crud import create_user_in_db, get_user_by_name
from predict_divorce.router import router as predict_divorce_router
from models import User as UserModel
from jwt import create_access_token, get_current_user

app = FastAPI()
app.include_router(predict_divorce_router)


@app.post('/user/', status_code=status.HTTP_201_CREATED, response_model=UserCreated, tags=['user'])
def create_user(user_request: User, db: Session = Depends(get_sync_db)):
    user = create_user_in_db(user_request=user_request, db=db)
    return user


@app.get('/user/', status_code=status.HTTP_200_OK, response_model=UserCreated, tags=['user'])
def get_logged_user(db: Session = Depends(get_sync_db), user: User = Depends(get_current_user)):
    return get_user_by_name(db=db, name=user.name)


@app.post('/login/', status_code=status.HTTP_200_OK, tags=['auth'], response_model=Token)
def login(login_request: Login, db: Session = Depends(get_sync_db)):
    user = UserModel.get_user_by_email_and_password(email=login_request.email, db=db, password=login_request.password)
    access_token = create_access_token(data={"name": user.name, 'id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)
