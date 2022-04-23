import os
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
import pickle
from typing import Any
import asyncpg
import asyncio

from fastapi import HTTPException, UploadFile

from database import SQLALCHEMY_DATABASE_URL
from moms_scientist.models import UserFile
from schemas import TokenData
from moms_scientist.crud import crate_user_file, check_file_not_unique


class PathHandler:
    """ Class for handling path operations """

    @staticmethod
    def get_user_path_folder(unique_int: int, filename: str, folder: str) -> str:
        """ Get path where to save a file for a particular user"""

        app_root = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.join(app_root, f'{folder}/{unique_int}/')
        path_with_prefix = os.path.abspath(upload_folder)
        attributes_file_location = os.path.join(path_with_prefix, filename)
        return attributes_file_location


class FileHandler(ABC):
    """ Interface for file handler classes """

    def __init__(self, file: UploadFile, name: str):
        self.file = file
        self.name = name

    @abstractmethod
    def handle_file(self) -> UserFile:
        """ Main interface for handling a file """
        pass

    @abstractmethod
    def _validate_file(self) -> None:
        """ Validate size, format of the file """
        pass

    @abstractmethod
    def _save_file(self, destination: Path) -> None:
        """ Actually save a file on the server """
        pass


class FileHandlerCSV(FileHandler, PathHandler):
    """ Realization for CSV files """

    def __init__(self, file: UploadFile, user: TokenData, name: str):
        super().__init__(file, name)
        self.user = user

    def handle_file(self) -> UserFile:
        self._validate_file()
        path = self.get_user_path_folder(unique_int=self.user.id, filename=self.file.filename, folder='csv_files')
        self._save_file(path)
        user_file = crate_user_file(path=path, user_id=self.user.id, name=self.name)
        return user_file

    def _validate_file(self) -> None:

        if check_file_not_unique(filename=self.file.filename, user_id=self.user.id):
            raise HTTPException(status_code=406, detail=f"File with that name already exists for user: {self.user.id}")

        if self.file.filename[-4:] != '.csv':
            raise HTTPException(status_code=406, detail="Format of the file is unacceptable. You must provide csv file")

    def _save_file(self, destination: str) -> None:
        """ Save the file on our server """

        try:
            # create dirs if it does not exist
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            with open(destination, "wb") as buffer:
                shutil.copyfileobj(self.file.file, buffer)
        finally:
            self.file.file.close()


class PickleModel:
    """ This class is needed to hugely reduce amount of time to train models each time """

    @staticmethod
    def pickle_python_object(python_object, path: str) -> None:
        """ Pickle (save as bytes) python object, so it can be restored later """

        # create dirs if it does not exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(python_object, file)

    @staticmethod
    def unpickle_python_object(path: str):
        """ Get python object from files """

        return pickle.load(open(path, "rb"))


class BroadcastBackend(ABC):
    """ Interface for broadcasting """

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def subscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def publish(self, channel: str, message: Any) -> None:
        pass

    @abstractmethod
    async def next_published(self):
        pass


class Message:
    def __init__(self, channel: str, message: str) -> None:
        self.channel = channel
        self.message = message

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Message)
            and self.channel == other.channel
            and self.message == other.message
        )

    def __str__(self) -> str:
        return f"Event(channel={self.channel}, message={self.message})"


class PostgresBroadcast(BroadcastBackend):
    """ PostgresSql implementation of broadcasting """

    def __init__(self, url: str = SQLALCHEMY_DATABASE_URL):
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

    async def publish(self, user_id: str, message: str) -> None:
        channel = f'channel{user_id}'
        await self._conn.execute("SELECT pg_notify($1, $2);", channel, message)

    def _listener(self, *args: Any) -> None:
        connection, pid, channel, payload = args
        event = Message(channel=channel, message=payload)
        self._listen_queue.put_nowait(event)

    async def next_published(self) -> Message:
        return await self._listen_queue.get()
