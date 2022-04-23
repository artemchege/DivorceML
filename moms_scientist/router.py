from typing import List

from fastapi import File, UploadFile, Depends, APIRouter, BackgroundTasks, HTTPException

from schemas import TokenData
from jwt import get_current_user
from moms_scientist.utils import FileHandlerCSV
from moms_scientist.schemas import SuccessResponse, TrainModels, ShowUploadedFiles, TrainedModels, UserFile
from moms_scientist.crud import list_user_files, get_user_file_for_user, list_trained_models, \
    check_user_file_belongs_to_user
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
    uploaded_file = await get_user_file_for_user(user_id=user.id, user_file_id=id)
    return uploaded_file


def start_background_task(train: TrainModels, background_tasks: BackgroundTasks,
                          user: TokenData = Depends(get_current_user)) -> bool:
    """ Dependency that checks some permission and starts the task """

    if check_user_file_belongs_to_user(user_file_id=train.user_file_id, user_id=user.id):
        background_tasks.add_task(create_ml_models, target_column=train.target_column, user_file_id=train.user_file_id,
                                  user_id=user.id)
        return True
    else:
        raise HTTPException(detail=f'you do not have permission to work with user_file_id={train.user_file_id}',
                            status_code=401)


@router.post("/train_models", summary="Train models", response_model=SuccessResponse)
def train_models(status: bool = Depends(start_background_task)):
    return {'success': status}


@router.post("/trained_models", summary="Trained models", response_model=List[TrainedModels])
def train_results(user_file_id: UserFile, user: TokenData = Depends(get_current_user)):
    trained_models = list_trained_models(user_file_id=user_file_id.user_file_id, user_id=user.id)
    return trained_models
