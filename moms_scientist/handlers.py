from moms_scientist.event import Event
from moms_scientist.crud import create_trained_model
from moms_scientist.utils import PickleModel


def handle_model_trained(data: dict) -> None:
    create_trained_model(name=data['name'], accuracy=data['accuracy'], precision=data['precision'],
                         recall=data['recall'], path=data['path'], user_file_id=data['user_file_id'])
    PickleModel.pickle_python_object(python_object=data['best_model'], path=data['path'])


def register_handlers():
    Event.subscribe(event_type='model_trained', fn=handle_model_trained)

