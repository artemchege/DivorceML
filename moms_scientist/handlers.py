from moms_scientist.event import Event
from moms_scientist.crud import create_trained_model
from moms_scientist.utils import PickleModel
from logger import logger


def handle_model_trained(data: dict) -> None:
    create_trained_model(name=data['name'], accuracy=data['accuracy'], precision=data['precision'],
                         recall=data['recall'], path=data['path'], user_file_id=data['user_file_id'])
    PickleModel.pickle_python_object(python_object=data['best_model'], path=data['path'])
    logger.info(f"Models were trained for {data['user_file_id']=}")


def register_handlers() -> None:
    Event.subscribe(event_type='model_trained', fn=handle_model_trained)

