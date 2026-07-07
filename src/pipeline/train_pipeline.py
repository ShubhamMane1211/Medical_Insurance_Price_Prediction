import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import get_logger

logger = get_logger(__name__)


def run_training_pipeline():
    try:
        logger.info(">>>>> Training pipeline started <<<<<")

        data_ingestion = DataIngestion()
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
            train_data_path, test_data_path
        )

        model_trainer = ModelTrainer()
        best_model_name, best_model_score = model_trainer.initiate_model_trainer(
            train_arr, test_arr
        )

        logger.info(">>>>> Training pipeline completed <<<<<")
        print(f"Best model: {best_model_name} | R2 score: {best_model_score:.4f}")

        return best_model_name, best_model_score

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    run_training_pipeline()
