from typing import List

from fastapi import File, UploadFile,  Depends, APIRouter, BackgroundTasks

from schemas import TokenData
from jwt import get_current_user
from moms_scientist.utils import FileHandlerCSV
from moms_scientist.schemas import SuccessResponse, TrainModels, ShowUploadedFiles
from moms_scientist.crud import list_user_files
from moms_scientist.tasks import create_ml_models


router = APIRouter(
    tags=['moms_scientist'],
    prefix='/moms_scientist'
)


@router.post("/upload_csv", summary="Save csv file", response_model=SuccessResponse)
def upload_csv(name_of_csv: str, file: UploadFile = File(...), user: TokenData = Depends(get_current_user)):
    file_handler = FileHandlerCSV(file, user, name=name_of_csv)
    file_handler.handle_file()
    return {'success': True}


@router.get("/list_csv", summary="List uploaded csv", response_model=List[ShowUploadedFiles])
async def list_csv(user: TokenData = Depends(get_current_user)):
    uploaded_files = await list_user_files(user_id=user.id)
    return uploaded_files


@router.post("/train_models", summary="Train models", response_model=SuccessResponse)
def train_models(train: TrainModels, background_tasks: BackgroundTasks, user: TokenData = Depends(get_current_user)):
    background_tasks.add_task(create_ml_models, target_column=train.target_column, user_file_id=train.user_file_id)
    return {'success': True}
