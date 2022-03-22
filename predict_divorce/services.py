import pickle
import numpy as np
import warnings
import pathlib

from predict_divorce.schemas import DivorceQuestionsCreate

warnings.filterwarnings('ignore')  # disable: X does not have valid feature names for some time. Fix later


def get_divorce_prediction(questions: DivorceQuestionsCreate) -> int:
    """ Transform users input and return result (prediction: 1 - divorce, 0 - peace ) """

    list_of_questions = [value.value for name, value in questions]
    np_array = np.array(list_of_questions).reshape(1, -1)
    path = ('/'.join(pathlib.Path(__file__).parent.resolve().parts[:-1]) + '/DataScience/divorce.pickle')[1:]
    prediction_model = pickle.load(open(path, "rb"))
    result = prediction_model.predict(np_array)[0]
    return int(result)


