from fastapi import HTTPException, UploadFile
import os
import shutil
from pathlib import Path
from abc import ABC, abstractmethod

from schemas import TokenData

from moms_scientist.crud import crate_user_file


class FileHandler(ABC):
    """ Interface for file handler classes """

    def __init__(self, file: UploadFile):
        self.file = file

    @abstractmethod
    def handle_file(self):
        """ Main interface for handling a file """
        pass

    @abstractmethod
    def _validate_file(self):
        """ Validate size, format of the file """
        pass

    @abstractmethod
    def _save_file(self, destination: Path) -> None:
        """ Actually save a file on the server """
        pass


class FileHandlerCSV(FileHandler):
    """ Realization for CSV files """

    def __init__(self, file, user: TokenData):
        super().__init__(file)
        self.user = user

    def handle_file(self):
        self._validate_file()
        path = self._get_path(self.user)
        self._save_file(path)
        crate_user_file(path=path, user_id=self.user.id)

    def _validate_file(self):

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

    def _get_path(self, user) -> str:
        """ Get path where to save a file """

        app_root = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.join(app_root, f'csv_files/{user.id}/')
        path_with_prefix = os.path.abspath(upload_folder)
        attributes_file_location = os.path.join(path_with_prefix, self.file.filename)
        return attributes_file_location


