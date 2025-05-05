"""
Base pipeline class for data processing pipelines.
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AnyStr, Dict


@dataclass
class RunTag:
    """
    A class to represent a run tag for the pipeline.
    """

    run_id: AnyStr


class BasePipeline(ABC):
    """
    Base class for all pipelines.
    """

    def __init__(self, config: AnyStr):
        self.config = self.read_config(config)
        self.run_tag = RunTag(run_id=self.config.get("run_id", "default_run"))

    def read_config(self, filepath: AnyStr, **kwargs) -> Dict[AnyStr, Any]:
        """Function to read the configuration file."""
        encoding = kwargs.get("encoding", "utf-8")
        with open(filepath, "r", encoding=encoding, **kwargs) as file:
            config = json.load(file)
        return config

    @abstractmethod
    def run(self):
        """
        Abstract method to run the pipeline.
        This method should be implemented by subclasses.
        """
