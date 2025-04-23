from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ConfigValidator(BaseModel):
    """
    ConfigValidator is a Pydantic model for validating configuration files.
    """
    data_in_path: str = Field(..., description="Path to the input data file.")
    data_out_path: str = Field(..., description="Path to save the output data file.")
    run_id: Optional[str] = Field(None, description="Unique identifier for the run.")
    encoding: Optional[str] = Field("utf-8", description="Encoding of the input data file.")
    columns: Optional[List[str]] = Field(None, description="List of columns to be used in the pipeline.")
    
    class Config:
        schema_extra = {
            "example": {
                "data_path": "/path/to/data.csv",
                "output_path": "/path/to/output.csv",
                "run_id": "12345",
                "encoding": "utf-8",
                "columns": ["column1", "column2"]
            }
        }