import datetime

from sqlalchemy import select
from fastapi import HTTPException, status

from database import async_session_local
from predict_divorce.schemas import DivorceQuestionsCreate
from predict_divorce.models import DivorcePredictionRequest
from models import User


async def create_divorce_request(divorce_request: DivorceQuestionsCreate, user: User, prediction: float):
    async with async_session_local() as session:
        async with session.begin():
            db_divorce_request = DivorcePredictionRequest(hate_subject=divorce_request.hate_subject.value,
                                                          happy=divorce_request.happy.value,
                                                          dreams=divorce_request.dreams.value,
                                                          freedom_value=divorce_request.freedom_value.value,
                                                          likes=divorce_request.likes.value,
                                                          calm_breaks=divorce_request.calm_breaks.value,
                                                          harmony=divorce_request.harmony.value,
                                                          roles=divorce_request.roles.value,
                                                          inner_world=divorce_request.inner_world.value,
                                                          current_stress=divorce_request.current_stress.value,
                                                          friends_social=divorce_request.friends_social.value,
                                                          contact=divorce_request.contact.value,
                                                          insult=divorce_request.insult.value,
                                                          created=datetime.datetime.now(),
                                                          user_id=user.id,
                                                          prediction=prediction)

            session.add(db_divorce_request)
            await session.flush()


async def list_divorce_requests(user: User):
    async with async_session_local() as session:
        async with session.begin():
            db_request = await session.execute(select(DivorcePredictionRequest).
                                               where(DivorcePredictionRequest.user_id == user.id))
            divorce_requests = db_request.scalars().all()

            if not divorce_requests:
                raise HTTPException(detail=f'objs were not found', status_code=status.HTTP_404_NOT_FOUND)
            return divorce_requests


async def get_divorce_request(divorce_id: int, user: User):
    async with async_session_local() as session:
        async with session.begin():
            db_request = await session.execute(select(DivorcePredictionRequest).where(
                DivorcePredictionRequest.id == divorce_id,
                DivorcePredictionRequest.creator.has(id=user.id)))

            divorce_request = db_request.one_or_none()
            if divorce_request is not None:
                (divorce_request,) = divorce_request
            else:
                raise HTTPException(detail=f'objs were not found', status_code=status.HTTP_404_NOT_FOUND)

            return divorce_request
