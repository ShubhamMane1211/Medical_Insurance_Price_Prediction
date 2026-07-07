import os
import sys

import dill
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models: dict, params: dict):
    try:
        report = {}
        fitted_models = {}

        for model_name, model in models.items():
            param_grid = params.get(model_name, {})

            if param_grid:
                gs = GridSearchCV(model, param_grid, cv=3, scoring="r2", n_jobs=-1)
                gs.fit(X_train, y_train)
                best_model = gs.best_estimator_
            else:
                best_model = model
                best_model.fit(X_train, y_train)

            y_test_pred = best_model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            fitted_models[model_name] = best_model

        return report, fitted_models

    except Exception as e:
        raise CustomException(e, sys)


def regression_metrics(y_true, y_pred) -> dict:
    try:
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = mse ** 0.5
        r2 = r2_score(y_true, y_pred)
        return {"mae": mae, "mse": mse, "rmse": rmse, "r2_score": r2}
    except Exception as e:
        raise CustomException(e, sys)
