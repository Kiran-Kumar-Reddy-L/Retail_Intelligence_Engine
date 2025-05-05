"""_summary_
"""

import logging
import os
from typing import Any, AnyStr, Dict

import mlflow
import numpy as np
import pandas as pd
from mlflow.models.model import Model
from sklearn.model_selection import train_test_split

from src.pipelines.data_pipe import DataPipeline
from src.utils.log_utils import Logger
from src.utils.pyfunc_model_wrapper import PyFuncModelWrapper


class TrainingPipeline(DataPipeline):
    """_summary_

    Args:
        BasePipeline (_type_): _description_
    """

    def __init__(self, config: AnyStr):
        super().__init__(config)
        self.tracking_uri = config.get("tracking_uri", "http://localhost:5000")
        self.experiment_name = config.get("experiment_name")
        self.model_save_path = config.get("model_save_path")
        self.model_type = config.get("model_type")
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
        train_data, test_data = train_test_split(
            data, test_size=test_size, random_state=42
        )
        return train_data, test_data

    def model_training(
        self,
        model: Any,
        hyperparameters: Dict[str, Any],
        X_train: np.array,
        y_train: np.array,
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

    def log_model_with_metadata(
        self, model: Any, X_test: np.array, y_test: np.array
    ) -> None:
        """_summary_

        Args:
            model (Any): _description_
            X_test (np.array): _description_
            y_test (np.array): _description_
        """
        self.logger.info("Logging the model and metrics to MLflow.")

        # Wrap the model with PyFuncModelWrapper
        wrapped_model = PyFuncModelWrapper(model)

        # Log the model and evaluate metrics
        with mlflow.start_run():
            mlflow.pyfunc.log_model(
                artifact_path=self.model_save_path, python_model=wrapped_model
            )

            # use mlflow.evaluate to log metrics
            evaluation_result = mlflow.evaluate(
                model=wrapped_model,
                data=(X_test, y_test),
                targets=y_test,
                model_type=self.model_type,
                evaluator_config={"metric_prefix": "test_"},
            )

            self.logger.info("Model evaluation result: %s", evaluation_result)

        self.logger.info("Model and Metrics logged successfully.")

    def run(self):
        pass
