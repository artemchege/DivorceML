from fastapi import HTTPException, UploadFile
import os
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
import pickle

from moms_scientist.models import UserFile
from schemas import TokenData

from moms_scientist.crud import crate_user_file


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

        # todo: validate that row in db does not exists

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
    def unpickle_python_object():
        """ Get python object from files """

        # todo: later when predicting
        pass
