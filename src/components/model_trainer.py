import json
import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from src.exception import CustomException
from src.logger import get_logger
from src.utils import save_object, evaluate_models, regression_metrics

logger = get_logger(__name__)


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")
    metrics_file_path: str = os.path.join("artifacts", "metrics.json")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logger.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Linear Regression": LinearRegression(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Random Forest Regressor": RandomForestRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "AdaBoost Regressor": AdaBoostRegressor(random_state=42),
                "SVR": SVR(),
            }

            params = {
                "Linear Regression": {},
                "Ridge": {"alpha": [0.1, 1.0, 10.0]},
                "Lasso": {"alpha": [0.1, 1.0, 10.0]},
                "K-Neighbors Regressor": {"n_neighbors": [3, 5, 7, 9]},
                "Decision Tree": {"max_depth": [3, 5, 7, 10, None]},
                "Random Forest Regressor": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [5, 10, None],
                },
                "Gradient Boosting": {
                    "learning_rate": [0.05, 0.1],
                    "n_estimators": [100, 200],
                    "max_depth": [3, 5],
                },
                "AdaBoost Regressor": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.05, 0.1, 1.0],
                },
                "SVR": {"C": [1, 10, 100], "kernel": ["rbf", "linear"]},
            }

            model_report, fitted_models = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params=params,
            )

            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = fitted_models[best_model_name]

            logger.info(f"Best model found: {best_model_name} with R2 score {best_model_score:.4f}")

            if best_model_score < 0.5:
                logger.warning("No model met the minimum acceptable R2 threshold of 0.5")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            y_pred = best_model.predict(X_test)
            metrics = regression_metrics(y_test, y_pred)
            metrics["best_model_name"] = best_model_name
            metrics["all_model_scores"] = model_report

            with open(self.model_trainer_config.metrics_file_path, "w") as f:
                json.dump(metrics, f, indent=2)

            logger.info(f"Model metrics saved: {metrics}")

            return best_model_name, best_model_score

        except Exception as e:
            raise CustomException(e, sys)
