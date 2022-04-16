import asyncio
import aiopg
import json

from fastapi import APIRouter, HTTPException
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from database import dsn
from jwt import verify_token

router = APIRouter()


@router.websocket_route('/event_channel')
class WebSocketConnection(WebSocketEndpoint):
    encoding = 'json'

    def __init__(self, scope, receive, send):
        super().__init__(scope, receive, send)
        self.connected = False
        self.loop = asyncio.get_event_loop()
        self.websocket = {}

    async def listen(self, conn, channel):
        """ Listen PostgresSQL channel and send messages to the socket """

        async with conn.cursor() as cur:
            await cur.execute("LISTEN {0}".format(channel))
            while self.connected:
                msg = await conn.notifies.get()
                payload = json.loads(msg.payload)
                await self.websocket.send_json(data=payload)

    async def db_events(self, channel: str):
        """ Place where we get async DB connection  """

        async with aiopg.create_pool(dsn) as pool:
            async with pool.acquire() as conn:
                await asyncio.gather(self.listen(conn=conn, channel=channel))

    async def on_receive(self, websocket: WebSocket, data: dict):
        """ Hook when client send message to the socket """

        channel = data.get('channel')

        if self.has_permission(headers=dict(websocket.headers), channel=channel):
            asyncio.ensure_future(self.db_events(channel=channel), loop=self.loop)
        else:
            await websocket.close()

    async def on_connect(self, websocket: WebSocket):
        """ On connect hook, accept all connections """

        await websocket.accept()
        self.connected = True
        self.websocket = websocket

    async def on_close(self):
        """ On close hook """

        self.connected = False
        self.websocket.close()

    @staticmethod
    def has_permission(headers: dict, channel: str) -> bool:
        """ We must be sure that request user may listen only his channel """

        try:
            token = headers.get('authorization').split(' ')[1]
            token_data = verify_token(token)
            return True if str(token_data.id) == channel else False
        except (KeyError, IndexError, HTTPException):
            return False
