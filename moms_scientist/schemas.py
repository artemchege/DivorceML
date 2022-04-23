import datetime

from pydantic import BaseModel, validator

from moms_scientist.crud import check_user_file_exists, check_models_were_trained_for_user_file


class SuccessResponse(BaseModel):
    success: bool


class ShowUploadedFiles(BaseModel):
    id: int
    name: str
    created: datetime.datetime

    class Config:
        orm_mode = True


class UserFile(BaseModel):
    user_file_id: int


class TrainModels(BaseModel):

    target_column: str
    user_file_id: int

    @validator('user_file_id')
    def validate_user_file_id(cls, user_file_id):

        if not check_user_file_exists(user_file_id=user_file_id):
            raise ValueError(f'You cannot train models for {user_file_id=}, this user file does not exists')

        if check_models_were_trained_for_user_file(user_file_id=user_file_id):
            raise ValueError(f'You cannot train model for {user_file_id=}, models have been already trained')

        return user_file_id


class TrainedModels(BaseModel):
    name: str
    accuracy: float
    precision: float
    recall: float
    user_file_id: int

    class Config:
        orm_mode = True
