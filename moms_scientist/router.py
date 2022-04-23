from typing import List

from fastapi import File, UploadFile,  Depends, APIRouter, BackgroundTasks

from schemas import TokenData
from jwt import get_current_user
from moms_scientist.utils import FileHandlerCSV
from moms_scientist.schemas import SuccessResponse, TrainModels, ShowUploadedFiles, TrainedModels, UserFile
from moms_scientist.crud import list_user_files, get_user_file, list_trained_models
from moms_scientist.tasks import create_ml_models
from moms_scientist.handlers import register_handlers


router = APIRouter(
    tags=['moms_scientist'],
    prefix='/moms_scientist'
)


@router.on_event("startup")
async def startup_event():
    register_handlers()


@router.post("/upload_csv", summary="Save csv file", response_model=SuccessResponse)
def upload_csv(name_of_csv: str, file: UploadFile = File(...), user: TokenData = Depends(get_current_user)):
    file_handler = FileHandlerCSV(file, user, name=name_of_csv)
    file_handler.handle_file()
    return {'success': True}


@router.get("/list_csv", summary="List uploaded csv", response_model=List[ShowUploadedFiles])
async def list_files(user: TokenData = Depends(get_current_user)):
    uploaded_files = await list_user_files(user_id=user.id)
    return uploaded_files


@router.get("/get_csv/{id}", summary="Retrieve uploaded csv", response_model=ShowUploadedFiles)
async def retrieve_file(id: int, user: TokenData = Depends(get_current_user)):
    uploaded_file = await get_user_file(user_id=user.id, user_file_id=id)
    return uploaded_file


@router.post("/train_models", summary="Train models", response_model=SuccessResponse)
def train_models(train: TrainModels, background_tasks: BackgroundTasks, user: TokenData = Depends(get_current_user)):
    background_tasks.add_task(create_ml_models, target_column=train.target_column, user_file_id=train.user_file_id,
                              user_id=user.id)
    return {'success': True}


@router.post("/trained_models", summary="Trained models", response_model=List[TrainedModels])
def train_results(user_file_id: UserFile, user: TokenData = Depends(get_current_user)):
    trained_models = list_trained_models(user_file_id=user_file_id.user_file_id, user_id=user.id)
    return trained_models

