from fastapi import File, UploadFile,  Depends, APIRouter

from schemas import User
from jwt import get_current_user
from moms_scientist.utils import FileHandlerCSV
from moms_scientist.schemas import SuccessResponse


router = APIRouter(
    tags=['moms_scientist'],
    prefix='/moms_scientist'
)


@router.post("/upload_csv", summary="Upload and save csv file", response_model=SuccessResponse)
def upload_csv(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    file_handler = FileHandlerCSV(file, user)
    file_handler.handle_file()
    return {'success': True}
