import datetime

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool


class ShowUploadedFiles(BaseModel):
    id: int
    name: str
    created: datetime.datetime

    class Config:
        orm_mode = True


class TrainModels(BaseModel):
    target_column: str
    user_file_id: int

    # todo: check that user-file_id exists and blelongs to user, прокинуть как то сюда юзера
    # todo: check that models has not been trained before

