from typing import Any, AnyStr, Dict

import pandas as pd

from src.pipelines.preprocessing_pipe import PreprocessingPipeline
from src.utils.log_utils import Logger


class RIEDataProcessingPipeline(PreprocessingPipeline):
    """
    Retail Intelligence Engine Data Processing Pipeline.
    This class extends the PreprocessingPipeline to handle specific data processing tasks.
    """

    def __init__(self, config: AnyStr):
        super().__init__(config)
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.run_tag = self.config.get("run_tag", None)
        self.raw_input_data_paths = config.get("raw_input_data_paths")
        self.preprocessed_output_data_paths = config.get(
            "preprocessed_output_data_paths"
        )
        self.combined_data_out_path = config.get("combined_data_out_path")

    def run(self):
        """_summary_"""
        # Load and preprocess Amazon sales report data
        self.load_and_preprocess_amazon_sale_report_data()

        # Load and preprocess generic sales report data
        self.load_and_preprocess_generic_sale_report_data()

        # Load and preprocess expense report data
        self.load_and_preprocess_int_sales_report_data()

        # Load and preprocess profit and loss report data
        self.load_and_preprocess_pl_report_data()

        # Combine all preprocessed data
        self.combined_preprocessed_data()

    def load_and_preprocess_amazon_sale_report_data(self):
        """
        Load and preprocess data.
        """
        # Load data
        self.logger.info("Load and Preprocess the amazon sales report data.")
        data = self.load_data(
            self.raw_input_data_paths["amazon_sales_report"], sep=",", encoding="utf-8"
        )

        # Preprocess data
        preprocessed_data = self.preprocess_data(data)

        # Save preprocessed data
        self.write_data(
            preprocessed_data,
            self.preprocessed_output_data_paths["amazon_sales_report_preprocessed"],
        )

    def load_and_preprocess_generic_sale_report_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # Load data
        self.logger.info("Load and Preprocess the generic sales report data.")
        data = self.load_data(
            self.raw_input_data_paths["sales_report"], sep=",", encoding="utf-8"
        )

        # Preprocess data
        preprocessed_data = self.preprocess_data(data)

        # Save preprocessed data
        self.write_data(
            preprocessed_data,
            self.preprocessed_output_data_paths["sales_report_preprocessed"],
        )

    def load_and_preprocess_int_sales_report_data(self):
        """
        load and preprocess data.
        """
        # Load data
        self.logger.info("Load and Preprocess the international sales report data.")
        data = self.load_data(
            self.raw_input_data_paths["int_sales_report"], sep=",", encoding="utf-8"
        )

        # Preprocess data
        preprocessed_data = self.preprocess_data(data)

        # Save preprocessed data
        self.write_data(
            preprocessed_data,
            self.preprocessed_output_data_paths["int_sales_report_preprocessed"],
        )

    def load_and_preprocess_pl_report_data(self):
        """
        Load and preprocess data.
        """
        # Load data for march p&l report
        self.logger.info("Load and Preprocess the profit and loss report data.")
        data_march = self.load_data(
            self.raw_input_data_paths["pl_report_march"], sep=",", encoding="utf-8"
        )

        # Load data for may p&l report
        self.logger.info("Load and Preprocess the profit and loss report data.")
        data_may = self.load_data(
            self.raw_input_data_paths["pl_report_may"], sep=",", encoding="utf-8"
        )

        # combine the data for march and may
        combined_pl_data = self.combine_dataframes(
            data_df=data_march,
            data_df_to_combine=data_may,
            operation="concat",
            axis=0,
            ignore_index=True,
        )

        # preprocess the combined data
        preprocessed_data = self.preprocess_data(combined_pl_data)

        # Save preprocessed data
        self.write_data(
            preprocessed_data,
            self.preprocessed_output_data_paths["pl_report_preprocessed"],
        )

    def combined_preprocessed_data(self):
        """_summary_"""
        # Load data
        self.logger.info("Load and combine all preprocessed data.")
        data_amazon_sales_report = self.load_data(
            self.preprocessed_output_data_paths["amazon_sales_report_preprocessed"],
            sep=",",
            encoding="utf-8",
        )
        data_generic_sales_report = self.load_data(
            self.preprocessed_output_data_paths["sales_report_preprocessed"],
            sep=",",
            encoding="utf-8",
        )
        data_int_sales_report = self.load_data(
            self.preprocessed_output_data_paths["int_sales_report_preprocessed"],
            sep=",",
            encoding="utf-8",
        )
        data_pl_report = self.load_data(
            self.preprocessed_output_data_paths["pl_report_preprocessed"],
            sep=",",
            encoding="utf-8",
        )

        # Combine all preprocessed data
        combined_df_1 = self.combine_dataframes(
            data_df=data_amazon_sales_report,
            data_df_to_combine=data_generic_sales_report,
            operation="",
            axis=0,
            ignore_index=True,
        )

        combined_df_2 = self.combine_dataframes(
            data_df=combined_df_1,
            data_df_to_combine=data_int_sales_report,
            operation="",
            axis=0,
            ignore_index=True,
        )

        combined_data = self.combine_dataframes(
            data_df=combined_df_2,
            data_df_to_combine=data_pl_report,
            operation="",
            axis=0,
            ignore_index=True,
        )

        # Save combined preprocessed data
        self.write_data(combined_data, self.combined_data_out_path)
