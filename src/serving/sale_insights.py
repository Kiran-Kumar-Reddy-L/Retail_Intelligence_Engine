import tomllib
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from src.utils.log_utils import Logger


class SaleInsights:
    """Class to handle sales insights data processing.
    This class is responsible for loading, preprocessing, and analyzing sales data.
    """

    def __init__(self, config: str):
        """Initialize the SaleInsights class.

        Args:
            config (str): Path to the configuration file.
        """
        with open(config, "rb") as f:
            self.config = tomllib.load(f)

        self.logger = Logger.get_logger(self.__class__.__name__)
        self.drop_columns = self.config["data"]["drop_columns"]
        self.dtype_columns = self.config["data"]["dtype_columns"]
        self.status_mapping = self.config["data"]["status_mapping"]

    def load_data(self, data_in_path: str, **kwargs) -> pd.DataFrame:
        """Load data from a file.

        Args:
            data_in_path (str): Path to the input data file.
            **kwargs: Additional arguments for pd.read_csv.

        Returns:
            pd.DataFrame: Loaded data as a DataFrame.

        Raises:
            FileNotFoundError: If the file does not exist.
            pd.errors.EmptyDataError: If the file is empty.
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

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply data cleaning steps to the data.

        Args:
            data (pd.DataFrame): Input data to be preprocessed.

        Returns:
            pd.DataFrame: Preprocessed data.
        """
        # Remove duplicates
        data = data.drop_duplicates()

        # Drop columns
        data = data.drop(columns=self.drop_columns, errors="ignore")

        # Standardize column names
        data.columns = data.columns.str.strip()
        data.columns = data.columns.str.lower().str.replace(r"[ -]", "_", regex=True)

        # Convert data types
        data = data.convert_dtypes()
        data["date"] = pd.to_datetime(data["date"], format="%m-%d-%y")
        data["month"] = data["date"].dt.month_name().str.lower()

        # convert the string column values to lowercase
        data = data.apply(lambda x: x.str.lower() if x.dtype == "string" else x)
        data["status"] = data["status"].replace(self.status_mapping)

        return data

    def apply_advanced_preprocessing(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply advanced preprocessing steps to the data.

        Args:
            data (pd.DataFrame): Input data to be preprocessed.

        Returns:
            pd.DataFrame: Preprocessed data.
        """
        # apply the filter to remove cancelled orders
        filter_df = data.loc[data["status"] != "cancelled"]

        # Fill the missing values for the "amount" column
        # Get the unique sku values for the null amount records
        na_amt_skus = filter_df.loc[filter_df["amount"].isna()]["sku"].unique()

        # Loop over the na sku values to get the mode
        # Fill the missing amount values with the mode
        for sku in na_amt_skus:
            mode = filter_df.loc[filter_df["sku"] == sku]["amount"].mode()
            if len(mode) > 0:
                filter_df.loc[
                    ((filter_df["sku"] == sku) & (filter_df["amount"].isna())), "amount"
                ] = mode[0]
            else:
                filter_df.loc[
                    ((filter_df["sku"] == sku) & (filter_df["amount"].isna())), "amount"
                ] = 0.0

        # Fill the missing values for the shipping columns
        # ship_city", "ship_state", "ship_postal_code"
        filter_df = filter_df.dropna(
            subset=["ship_city", "ship_state", "ship_postal_code"]
        )

        return filter_df

    def derive_total_amount(self, data: pd.DataFrame) -> pd.DataFrame:
        """Derive the total amount from the data.

        Args:
            data (pd.DataFrame): Input data to derive total amount.

        Returns:
            pd.DataFrame: Data with total amount derived.
        """
        # Derive the total amount
        data["total_amount"] = data["amount"] * data["qty"]
        return data

    def get_revenue_per_day(
        self, data: pd.DataFrame, group_by: Union[str, List[str]]
    ) -> pd.DataFrame:
        """Get revenue per day from the data.

        Args:
            data (pd.DataFrame): Input data to get revenue per day.
            group_by (Union[str, List[str]]): Columns to group by.

        Returns:
            pd.DataFrame: Data with revenue per day.
        """
        # Filter the records to remove returned orders
        filter_df = data.loc[data["status"] != "returned"]

        # Group by date and calculate total amount
        grouped_df = (
            filter_df.groupby(group_by)
            .agg(revenue_per_day=("total_amount", "sum"))
            .reset_index()
        )

        # round off the date to the nearest decimal
        grouped_df["revenue_per_day"] = grouped_df["revenue_per_day"].apply(
            lambda x: f"{round(x):,}"
        )

        return grouped_df

    def get_top_skus(
        self, data: pd.DataFrame, group_by: Union[str, List[str]], top_n: int = 10
    ) -> pd.DataFrame:
        """Get top N SKUs from the data.

        Args:
            data (pd.DataFrame): Input data to get top SKUs.
            group_by (Union[str, List[str]]): Columns to group by.
            top_n (int, optional): Number of top SKUs to return. Defaults to 10.

        Returns:
            pd.DataFrame: Data with top SKUs.
        """
        # Group by SKU and calculate total amount
        grouped_df = (
            data.groupby(group_by)
            .agg(
                revenue_per_month=("total_amount", "sum"),
                order_count=("order_id", "count"),
            )
            .reset_index()
        )

        # Get the top N SKUs
        top_skus_df = grouped_df.nlargest(top_n, ["revenue_per_month", "order_count"])

        # round off the total amount to the nearest decimal
        top_skus_df["revenue_per_month"] = top_skus_df["revenue_per_month"].apply(
            lambda x: f"{round(x):,}"
        )

        return top_skus_df

    def get_avg_selling_price_and_count(
        self, data: pd.DataFrame, group_by: Union[str, List[str]]
    ) -> pd.DataFrame:
        """Get average selling price and order count from the data.

        Args:
            data (pd.DataFrame): Input data to get average selling price and count.
            group_by (Union[str, List[str]]): Columns to group by.

        Returns:
            pd.DataFrame: Data with average selling price and order count.
        """
        # Group by SKU and calculate total amount
        grouped_df = (
            data.groupby(group_by)
            .agg(
                average_selling_price=("total_amount", "mean"),
                order_count=("order_id", "count"),
            )
            .reset_index()
        )

        # fill the missing values with 0
        grouped_df["average_selling_price"] = grouped_df[
            "average_selling_price"
        ].fillna(0)
        grouped_df["order_count"] = grouped_df["order_count"].fillna(0)

        # round off the average selling price to the nearest decimal
        grouped_df["average_selling_price"] = grouped_df["average_selling_price"].apply(
            lambda x: f"{round(x):,}"
        )

        return grouped_df
