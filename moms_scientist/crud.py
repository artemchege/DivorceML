import datetime

from moms_scientist.models import UserFile
from database import get_sync_db


def crate_user_file(path: str, user_id: int):
    """ Create a row with user file in DB """

    user_file = UserFile(path=path, user_id=user_id, created=datetime.datetime.now())
    db = next(get_sync_db())
    db.add(user_file)
    db.commit()
    db.refresh(user_file)
    return user_file
