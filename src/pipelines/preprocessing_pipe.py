"""
Preprocessing pipeline for data preprocessing tasks.
This pipeline includes data cleaning, feature engineering, and data transformation steps.
It inherits from the DataPipeline class and implements the run method to execute the pipeline.
"""

from src.pipelines.data_pipe import DataPipe
import pandas as pd
from typing import Dict, Any, AnyStr

class PreprocessingPipeline(DataPipe):
    """_summary_

    Args:
        DataPipe (_type_): _description_
    """
    def __init__(self, config: Dict[AnyStr, Any]):
        super().__init__(config)
        self.config = config
    
    def run(self):
        """
        Run the preprocessing pipeline.
        """
        # Read data
        data = self.read_data(self.config["input_data_path"])
        
        # Preprocess data
        preprocessed_data = self.preprocess_data(data)
        
        # Write data
        self.write_data(preprocessed_data)
                        
    def apply_data_cleaning(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply data cleaning steps to the data.
        """
        # Example: Remove duplicates
        data = data.drop_duplicates()
        
        # Example: Fill missing values
        data = data.fillna(method='ffill')
        
        return data
    
    def apply_feature_engineering(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering steps to the data.
        """
        # Example: Create new features
        return data

    def apply_data_transformation(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply data transformation steps to the data.
        """
        # Example: Normalize data
        data = (data - data.mean()) / data.std()

        return data
    
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data by applying data cleaning, feature engineering, and transformation.
        """
        data = self.apply_data_cleaning(data)
        data = self.apply_feature_engineering(data)
        data = self.apply_data_transformation(data)

        return data
