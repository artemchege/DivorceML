from moms_scientist.observer import Observer
from moms_scientist.crud import create_trained_model
from moms_scientist.utils import PickleModel, PostgresBroadcast
from logger import logger


async def handle_model_trained(data: dict) -> None:
    """ Some parts that must be triggered after model is trained """

    create_trained_model(name=data['name'], accuracy=data['accuracy'], precision=data['precision'],
                         recall=data['recall'], path=data['path'], user_file_id=data['user_file_id'])
    PickleModel.pickle_python_object(python_object=data['best_model'], path=data['path'])
    logger.info(f"Models were trained for {data['user_file_id']=}")

    broadcast = PostgresBroadcast()
    await broadcast.connect()
    await broadcast.publish(user_id=str(data['user_id']), message=f'Model {data["name"]} was created for user_file_id'
                                                                  f'{data["user_file_id"]}')


def register_handlers() -> None:
    Observer.subscribe(event_type='model_trained', fn=handle_model_trained)
