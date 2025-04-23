import mlflow
import pandas as pd

class PyFuncModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model):
        """
        Initialize the PyFunc model wrapper with a trained model.

        :param model: The trained model to wrap.
        """
        self.model = model

    def predict(self, context, model_input: pd.DataFrame) -> pd.DataFrame:
        """
        Perform inference using the wrapped model.

        :param context: MLflow context (not used here).
        :param model_input: A pandas DataFrame containing the input features.
        :return: A pandas DataFrame containing the predictions.
        """
        predictions = self.model.predict(model_input)
        return pd.DataFrame(predictions, columns=["predictions"])
