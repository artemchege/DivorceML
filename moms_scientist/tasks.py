from moms_scientist.ml import list_of_ml_handlers
from moms_scientist.utils import PathHandler, PickleModel


def create_ml_models(target_column: str, user_file_id: int) -> None:
    for ml_handler in list_of_ml_handlers:
        model = ml_handler(target_column=target_column, user_file_id=user_file_id)
        best_model, score, precision, recall = model.get_best_model()
        path = PathHandler.get_user_path_folder(unique_int=user_file_id, folder='trained_models',
                                                filename=f'{model.ml_model_name}.pickle')

        # todo: write to db

        PickleModel.pickle_python_object(python_object=best_model, path=path)
