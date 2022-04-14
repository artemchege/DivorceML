import asyncio
import json
import aiopg

import uvicorn
from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from schemas import Login, User, UserCreated, Token, TokenData
from database import get_sync_db
from crud import create_user_in_db, get_user_by_id
from predict_divorce.router import router as predict_divorce_router
from moms_scientist.router import router as moms_scientist_router
from models import User as UserModel
from jwt import create_access_token, get_current_user

app = FastAPI()
app.include_router(predict_divorce_router)
app.include_router(moms_scientist_router)

dsn = 'dbname = fastapi user = postgres password = 1234 host = 127.0.0.1'


@app.websocket_route('/order_events')
class WebSocketOrders(WebSocketEndpoint):
    encoding = 'json'

    def __init__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        self.connected = False
        self.loop = asyncio.get_event_loop()
        self.websocket = {}

    @asyncio.coroutine
    async def listen(self, conn, channel):
        async with conn.cursor() as cur:
            await cur.execute("LISTEN {0}".format(channel))
            while self.connected:
                msg = await conn.notifies.get()
                print(msg.payload)
                # payload: dict = json.loads(msg.payload)
                # if payload.get("action") == "INSERT":
                #     insert_data = payload.get("data")
                #     await self.websocket.send_json({"message": "New order", "data": insert_data})
                # elif payload.get("action") == "UPDATE":
                #     update_data = payload.get("data")
                #     await self.websocket.send_json({"message": "Order update", "data": update_data})

    async def db_events(self, data: dict, websocket: WebSocket, channel: str):
        async with aiopg.create_pool(dsn) as pool:
            async with pool.acquire() as conn:
                await asyncio.gather(self.listen(conn, channel))

    async def on_receive(self, websocket: WebSocket, data: dict):
        channel: str = data.get('channel')
        asyncio.ensure_future(self.db_events(data, websocket, channel), loop=self.loop)

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connected = True
        self.websocket = websocket

    async def on_close(self, websocket):
        self.connected = False
        self.websocket.close()


@app.post('/user/', status_code=status.HTTP_201_CREATED, response_model=UserCreated, tags=['user'])
async def create_user(user_request: User):
    user = await create_user_in_db(user_request=user_request)
    return user


@app.get('/user/', status_code=status.HTTP_200_OK, response_model=UserCreated, tags=['user'])
async def get_logged_user(user: TokenData = Depends(get_current_user)):
    user = await get_user_by_id(user_id=user.id)
    return user


@app.post('/login/', status_code=status.HTTP_200_OK, tags=['auth'], response_model=Token)
def login(login_request: Login, db: Session = Depends(get_sync_db)):
    user = UserModel.get_user_by_email_and_password(email=login_request.email, db=db, password=login_request.password)
    access_token = create_access_token(data={"name": user.name, 'id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8123)
