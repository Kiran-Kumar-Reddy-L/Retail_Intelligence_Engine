import mlflow.pyfunc
import pandas as pd

class InferencePipeline:
    def __init__(self, model_uri: str):
        """
        Initialize the inference pipeline with the MLflow PyFunc model.

        :param model_uri: The URI of the MLflow model to load.
        """
        self.model = mlflow.pyfunc.load_model(model_uri)

    def predict(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """
        Perform inference on the input data using the loaded model.

        :param input_data: A pandas DataFrame containing the input features.
        :return: A pandas DataFrame containing the predictions.
        """
        predictions = self.model.predict(input_data)
        return pd.DataFrame(predictions, columns=["predictions"])

# Example usage:
# pipeline = InferencePipeline(model_uri="models:/my_model/1")
# input_data = pd.DataFrame({...})
# predictions = pipeline.predict(input_data)