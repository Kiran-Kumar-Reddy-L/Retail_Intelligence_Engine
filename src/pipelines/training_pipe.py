import numpy as np
import pandas as pd
import os
import logging
import mlflow
from typing import Dict, Any, AnyStr
from src.pipelines.base_pipe import BasePipeline
from sklearn.model_selection import train_test_split
from mlflow.models.model import Model
from src.utils.log_utils import Logger

class TrainingPipe(BasePipeline):
    """_summary_

    Args:
        BasePipeline (_type_): _description_
    """
    def __init__(self, config: Dict[AnyStr, Any]):
        super().__init__(config)
        self.tracking_uri = config.get("tracking_uri", "http://localhost:5000")
        self.experiment_name = config.get("experiment_name")
        self.model_hyperparameters = config.get("model_hyperparameters")
        self.model_save_path = config.get("model_save_path")
        self.logger = Logger.get_logger(self.__class__.__name__)


    def setup_mlflow_tracking(self):
        """
        Setup MLflow tracking.
        """
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)
        self.logger.info("MLflow tracking URI set to : %s", self.tracking_uri)
        self.logger.info("MLflow experiment name set to : %s", self.experiment_name)


    def train_test_split(self, data: pd.DataFrame, test_size: float = 0.2) -> tuple:
        """
        Split the data into training and testing sets.
        """
        train_data, test_data = train_test_split(data, test_size=test_size, random_state=42)
        return train_data, test_data
    

    def model_training(
        self,
        model : Any,
        hyperparameters: Dict[str, Any],
        X_train: np.array, 
        y_train: np.array
    ) -> Any:
        """_summary_

        Args:
            model (_type_): _description_
            X_train (np.array): _description_
            y_train (np.array): _description_

        Returns:
            Any: _description_
        """
        self.logger.info("Training the model with hyperparameters: %s", hyperparameters)
        model = model(**hyperparameters)
        model.fit(X_train, y_train)
        return model
    
    def model_evaluation(
        self,
        model: Any,
        X_test: np.array,
        y_test: np.array
    ) -> float:
        """_summary_

        Args:
            model (_type_): _description_
            X_test (np.array): _description_
            y_test (np.array): _description_

        Returns:
            float: _description_
        """
        self.logger.info("Evaluating the model.")
        predictions = model.predict(X_test)
        accuracy = np.mean(predictions == y_test)
        self.logger.info("Model accuracy: %f", accuracy)
        return accuracy
    

    def run(self):
        pass