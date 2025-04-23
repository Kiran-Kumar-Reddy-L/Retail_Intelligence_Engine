"""
Preprocessing pipeline for data preprocessing tasks.
This pipeline includes data cleaning, feature engineering, and data transformation steps.
It inherits from the DataPipeline class and implements the run method to execute the pipeline.
"""

from src.pipelines.data_pipe import DataPipeline
from src.utils.log_utils import Logger
import pandas as pd
from typing import Dict, Any, AnyStr

class PreprocessingPipeline(DataPipeline):
    """_summary_

    Args:
        DataPipe (_type_): _description_
    """
    def __init__(self, config: AnyStr):
        super().__init__(config)
        self.logger = Logger.get_logger(self.__class__.__name__)
    
    def run(self):
        """
        Run the preprocessing pipeline.
        """
        raise NotImplementedError("The run method should be implemented by subclasses.")
                        
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
