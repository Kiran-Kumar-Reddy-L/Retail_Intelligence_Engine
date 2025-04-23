"""
Base pipeline class for data ingestion tasks.
This module defines the DataPipe class, which is responsible for loading and saving data.
"""
from src.pipelines.base_pipe import BasePipeline
import pandas as pd
from src.utils.log_utils import Logger
from typing import Dict, Any, AnyStr, Optional

class DataPipeline(BasePipeline):
    """
    Data pipeline class that handles data ingestion tasks.
    """
    def __init__(self, config: AnyStr):
        super().__init__(config)
        self.logger = Logger.get_logger(self.__class__.__name__)

    def run(self):
        """
        Run the data pipeline.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("The run method should be implemented by subclasses.")
        
    def load_data(self, data_in_path: AnyStr, **kwargs) -> pd.DataFrame:
        """
        Load data from a file.
        """
        try:
            data = pd.read_csv(data_in_path, **kwargs)
            self.logger.info("Data loaded from: %s", data_in_path)
            return data
        except FileNotFoundError:
            self.logger.error("The file %s does not exist.", data_in_path)
            raise
        except pd.errors.EmptyDataError:
            self.logger.error("The file %s is empty.", data_in_path)
            raise

    def write_data(self, data_df: pd.DataFrame, data_out_path: AnyStr) -> None:
        """Write data to a file.

        "write_data" method to save the data to a CSV file.

        Args:
            data_df (pd.DataFrame): DataFrame to be saved.
        
        Returns:
            None
        
        Raises:
            Exception: If there is an error saving the data.
        """
        try:
            data_df.to_csv(data_out_path, index=False)
            self.logger.info("Data is saved to path: %s", data_out_path)
        except Exception as e:
            self.logger.error("Error saving data to %s: %s", data_out_path, str(e))
            raise

    def combine_dataframes(
        self,
        data_df : pd.DataFrame,
        data_df_to_combine: pd.DataFrame,
        operation: AnyStr,
        key: Optional[AnyStr] = None,
        **kwargs
    ) -> pd.DataFrame:
        """Combine multiple dataframes based on the specified operation.

        "combine_dataframes" method can be used to merge, join, or concatenate dataframes 
        based on the operation specified.

        Args:
            data_df (pd.DataFrame): DataFrame to be combined.
            operation (str): Operation to perform on the dataframes.
            key (str, optional): Key to join on. Defaults to None.
            **kwargs: Additional arguments for the operation.
        
        Returns:
            pd.DataFrame: Combined DataFrame.

        Raises:
            ValueError: If the operation is not supported.
        """
        if operation == "merge":
            if key is None:
                self.logger.error("Key is not provided for merge operation.")
                raise ValueError("Key must be provided for merge operation.")
            self.logger.info("Merging dataframes on key: %s", key)
            return data_df.merge(data_df_to_combine, on=key, **kwargs)
        elif operation == "join":
            if key is None:
                self.logger.error("Key is not provided for join operation.")
                raise ValueError("Key must be provided for join operation.")
            self.logger.info("Joining dataframes on key: %s", key)
            return data_df.join(data_df_to_combine.set_index(key), **kwargs)
        elif operation == "concat":
            self.logger.info("Concatenating dataframes.")
            return pd.concat([data_df, data_df_to_combine], **kwargs)
        else:
            raise ValueError(f"Operation {operation} is not supported.")
