import uvicorn
from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
# from datetime import timedelta

from predict_divorce.schemas import User, UserCreated
from schemas import Login
from database import get_db, Base, engine
from crud import create_user_in_db, get_user_by_name
from predict_divorce.router import router as predict_divorce_router
from predict_divorce.models import User as UserModel
from hashing import Hash
from jwt import create_access_token, get_current_user

app = FastAPI()
app.include_router(predict_divorce_router)

Base.metadata.create_all(engine)


@app.post('/user/', status_code=status.HTTP_201_CREATED, response_model=UserCreated, tags=['user'])
def create_user(user_request: User, db: Session = Depends(get_db)):
    user = create_user_in_db(user_request=user_request, db=db)
    return user


@app.get('/user/', status_code=status.HTTP_200_OK, response_model=UserCreated, tags=['user'])
def get_logged_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_user_by_name(db=db, name=user.name)


@app.post('/login/', status_code=status.HTTP_200_OK, tags=['auth'])
def login(login_request: Login, db: Session = Depends(get_db)):
    # TODO: задвинуть бизнс логику в модель юзера
    user = db.query(UserModel).filter(UserModel.name == login_request.name).first()
    if not user:
        raise HTTPException(detail=f'User does not exists', status_code=status.HTTP_400_BAD_REQUEST)

    if not Hash.verify(plain_password=login_request.password, hashed_password=user.password):
        raise HTTPException(detail=f'Invalid password', status_code=status.HTTP_400_BAD_REQUEST)

    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)
