from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LoadDataRequest(BaseModel):
    """
    Request model for loading data.
    """

    path: str = Field(..., description="Path to the data file.")


class LoadDataResponse(BaseModel):
    """
    Response model for loading data.
    """

    message: str
    status_code: int


class ProcessDataResponse(BaseModel):
    """
    Response model for processing data.
    """

    message: str
    status_code: int


class DataValidationSchema(BaseModel):
    """
    Request model for processing data.
    """

    order_id: str
    date: date
    status: str
    fulfilment: str
    sales_channel: str
    style: str
    sku: str
    category: str
    size: str
    qty: int
    amount: float
    ship_city: str
    ship_state: str
    ship_postal_code: int
    b2b: bool


class DailyRevenueRequest(BaseModel):
    """
    Request model for daily revenue insights.
    """

    ship_state: Optional[str] = Field(None, description="State to filter the data.")
    category: Optional[str] = Field(None, description="Category to filter the data.")
    sku: Optional[str] = Field(None, description="SKU to filter the data.")
    date_range: Optional[date] = Field(
        None, description="Date range to filter the data."
    )


class DailyRevenueResponse(BaseModel):
    """
    Response model for daily revenue insights.
    """

    date: datetime
    revenue_per_day: str
    ship_state: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None


class TopSkusRequest(BaseModel):
    """
    Request model for top SKUs insights.
    """

    month: Optional[str] = Field(None, description="Month to filter the data.")
    top_n: Optional[int] = Field(10, description="Number of top SKUs to return.")


class TopSkusResponse(BaseModel):
    """
    Response model for top SKUs insights.
    """

    sku: str
    revenue_per_month: str
    order_count: int
    month: Optional[str] = None


class ASPOrderCountResponse(BaseModel):
    """
    Response model for ASP order count insights.
    """

    sku: Optional[str] = None
    category: Optional[str] = None
    average_selling_price: str
    order_count: int
