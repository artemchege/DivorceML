from moms_scientist.ml import list_of_ml_handlers
from moms_scientist.utils import PathHandler
from moms_scientist.observer import Observer


async def create_ml_models(target_column: str, user_file_id: int, user_id: int) -> None:
    for ml_handler in list_of_ml_handlers:
        model = ml_handler(target_column=target_column, user_file_id=user_file_id)
        best_model, score, precision, recall = model.get_best_model()
        path = PathHandler.get_user_path_folder(unique_int=user_file_id, folder='trained_models',
                                                filename=f'{model.ml_model_name}.pickle')

        data = {
            'name': model.ml_model_name,
            'precision': precision,
            'recall': recall,
            'accuracy': score,
            'path': path,
            'user_file_id': user_file_id,
            'best_model': best_model,
            'user_id': user_id
        }
        await Observer.post_event(event_type='model_trained', data=data)
