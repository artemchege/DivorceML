import datetime

from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from database import get_sync_db, async_session_local
from moms_scientist.models import UserFile, TrainedModel


def crate_user_file(path: str, user_id: int, name: str) -> UserFile:
    """ Create a row with user file in DB """

    user_file = UserFile(path=path, user_id=user_id, created=datetime.datetime.now(), name=name)
    db = next(get_sync_db())
    db.add(user_file)
    db.commit()
    db.refresh(user_file)
    return user_file


async def list_user_files(user_id: int):
    """ List all UserFile obj that belongs to user """

    async with async_session_local() as session:
        async with session.begin():
            db_request = await session.execute(select(UserFile).where(UserFile.user_id == user_id))
            divorce_requests = db_request.scalars().all()

            if not divorce_requests:
                raise HTTPException(detail=f'objs were not found', status_code=status.HTTP_404_NOT_FOUND)

            return divorce_requests


def get_user_file(user_file_id: int) -> UserFile:
    """ Get particular UserFile obj that belongs to user """

    # todo: проверить что если такого файла не будет
    db = next(get_sync_db())
    user_file = db.query(UserFile).filter(UserFile.id == user_file_id).first()
    return user_file


def create_trained_model(name: str, precision: float, recall: float, accuracy: float, path: str, user_file_id: int) \
        -> TrainedModel:
    """ Create TrainedModel obj """

    trained_model = TrainedModel(name=name, precision=precision, recall=recall, accuracy=accuracy, path=path,
                                 user_file_id=user_file_id, created=datetime.datetime.now())
    db = next(get_sync_db())
    db.add(trained_model)
    db.commit()
    db.refresh(trained_model)
    return trained_model
