from sklearn.linear_model import LinearRegression
from src.utils.log_utils import Logger
from typing import AnyStr, Dict, Any
from src.pipelines.training_pipe import TrainingPipeline


class RIETraining(TrainingPipeline):
    """
    Retail Intelligence Engine Training Pipeline.
    This class extends the TrainingPipeline to handle specific training tasks.
    """
    def __init__(self, config: AnyStr):
        super().__init__(config)

    def run(self):
        """
        Run the training pipeline.
        """
        # Setup MLflow tracking
        self.setup_mlflow_tracking()

        # Load the preprocessed data
        data_df = self.load_data(data_in_path=self.config["combined_data_out_path"])

        # Split the data into training and testing sets
        train_data, test_data = self.train_test_split(data_df, test_size=0.2)

        # Extract features and labels
        x_train = train_data.drop(columns=["target_column"])
        y_train = train_data["target_column"]
        x_test = test_data.drop(columns=["target_column"])
        y_test = test_data["target_column"]

        # Train the model
        trained_model = self.model_training(
            model=LinearRegression,
            hyperparameters=self.config["hyperparameters"],
            X_train=x_train,
            y_train=y_train
        )

        # Log the model
        self.log_model_with_metadata(
            model=trained_model,
            X_test=x_test,
            y_test=y_test
        )

    
