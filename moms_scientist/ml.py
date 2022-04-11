import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split, GridSearchCV

from moms_scientist.crud import get_user_file


class SkitLearnMLHandler:
    """ Interface for ML handlers """

    def __init__(self, target_column: str, user_file_id: int):
        self.target_column = target_column
        self.user_file_id = user_file_id

    @property
    def classifier(self):
        raise NotImplementedError

    @property
    def train_parameters(self):
        raise NotImplementedError

    def get_best_model(self) -> tuple:
        csv = self._read_file()
        X_train, X_test, y_train, y_test = train_test_split(self._get_x(csv), self._get_y(csv), test_size=0.33,
                                                            random_state=42)

        clf_rf = self.classifier()
        grid_search_cv_clf = GridSearchCV(clf_rf, self.train_parameters, cv=5, n_jobs=-1, verbose=1)
        grid_search_cv_clf.fit(X_train, y_train)
        best_model = grid_search_cv_clf.best_estimator_

        score = self._get_score(x_test=X_test, y_test=y_test, model=best_model)
        precision = self._get_precision(model=best_model, y_test=y_test, x_test=X_test)
        recall = self._get_recall(model=best_model, y_test=y_test, x_test=X_test)

        return best_model, score, precision, recall

    def _read_file(self) -> pd.DataFrame:
        user_file = get_user_file(self.user_file_id)
        return pd.read_csv(user_file.path)

    def _get_x(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop([self.target_column], axis=1)

    def _get_y(self, df: pd.DataFrame) -> pd.Series:
        return df[self.target_column]

    @staticmethod
    def _get_score(x_test, y_test, model) -> float:
        return model.score(x_test, y_test)

    @staticmethod
    def _get_precision(model, y_test, x_test) -> float:
        y_pred = model.predict(x_test)
        return precision_score(y_test, y_pred)

    @staticmethod
    def _get_recall(model, y_test, x_test) -> float:
        y_pred = model.predict(x_test)
        return recall_score(y_test, y_pred)


class RandomForest(SkitLearnMLHandler):
    ml_model_name = 'random_forest_tree'

    @property
    def classifier(self):
        return RandomForestClassifier

    @property
    def train_parameters(self):
        return {'n_estimators': range(10, 50, 10), 'max_depth': range(1, 12, 2), 'min_samples_leaf': range(1, 7),
                'min_samples_split': range(2, 9, 2)}


class KNeighbors(SkitLearnMLHandler):
    ml_model_name = 'k_neighbors'

    def get_best_model(self) -> tuple:
        return super().get_best_model()

    @property
    def classifier(self):
        return KNeighborsClassifier

    @property
    def train_parameters(self):
        return {'n_neighbors': range(3, 15, 2), 'weights': ['uniform', 'distance'],
                'metric': ['euclidean', 'manhattan']}


list_of_ml_handlers = (RandomForest, KNeighbors,)
