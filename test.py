from typing import Any

import asyncpg
import asyncio


class BroadcastBackend:

    async def connect(self) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        raise NotImplementedError()

    async def subscribe(self, group: str) -> None:
        raise NotImplementedError()

    async def unsubscribe(self, group: str) -> None:
        raise NotImplementedError()

    async def publish(self, channel: str, message: Any) -> None:
        raise NotImplementedError()

    async def next_published(self):
        raise NotImplementedError()


class Event:
    def __init__(self, channel: str, message: str) -> None:
        self.channel = channel
        self.message = message

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Event)
            and self.channel == other.channel
            and self.message == other.message
        )

    def __repr__(self) -> str:
        return f"Event(channel={self.channel!r}, message={self.message!r})"


class PostgresBackend(BroadcastBackend):
    def __init__(self, url: str):
        self._url = url

    async def connect(self) -> None:
        self._conn = await asyncpg.connect(self._url)
        self._listen_queue: asyncio.Queue = asyncio.Queue()

    async def disconnect(self) -> None:
        await self._conn.close()

    async def subscribe(self, channel: str) -> None:
        await self._conn.add_listener(channel, self._listener)

    async def unsubscribe(self, channel: str) -> None:
        await self._conn.remove_listener(channel, self._listener)

    async def publish(self, channel: str, message: str) -> None:
        await self._conn.execute("SELECT pg_notify($1, $2);", channel, message)

    def _listener(self, *args: Any) -> None:
        connection, pid, channel, payload = args
        event = Event(channel=channel, message=payload)
        self._listen_queue.put_nowait(event)

    async def next_published(self) -> Event:
        return await self._listen_queue.get()
