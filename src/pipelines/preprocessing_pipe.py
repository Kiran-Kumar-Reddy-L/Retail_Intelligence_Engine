"""
Preprocessing pipeline for data preprocessing tasks.
This pipeline includes data cleaning, feature engineering, and data transformation steps.
It inherits from the DataPipeline class and implements the run method to execute the pipeline.
"""

from typing import Any, AnyStr, Dict, List

import pandas as pd

from src.pipelines.data_pipe import DataPipeline
from src.utils.log_utils import Logger


class PreprocessingPipeline(DataPipeline):
    """_summary_

    Args:
        DataPipe (_type_): _description_
    """

    def __init__(self, config: AnyStr):
        super().__init__(config)
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.drop_columns = config.get("drop_columns", [])
        self.dtype_columns = config.get("dtype_columns", {})

    def apply_data_cleaning(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply data cleaning steps to the data.
        """
        # Remove duplicates
        data = data.drop_duplicates()

        # Drop columns
        data = data.drop(columns=self.drop_columns, errors="ignore")

        # Standardize column names
        data.columns = data.columns.str.lower().str.replace(" ", "")

        # Convert data types
        for column, dtype in self.dtype_columns.items():
            if column in data.columns:
                data[column] = data[column].astype(dtype)
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

    def apply_groupby_aggregation(
        self,
        data: pd.DataFrame,
        group_by: List[AnyStr] | AnyStr,
        agg_func: Dict[str, str],
    ) -> pd.DataFrame:
        """
        Apply groupby aggregation to the data.
        """
        data = data.groupby(group_by).agg(agg_func).reset_index()
        return data

    def filter_data(self, data: pd.DataFrame, filter_condition: str) -> pd.DataFrame:
        """
        Filter the data based on a condition.
        """
        data = data.query(filter_condition)
        return data

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data by applying data cleaning, feature engineering, and transformation.
        """
        data = self.apply_data_cleaning(data)
        data = self.apply_feature_engineering(data)
        data = self.apply_data_transformation(data)

        return data
