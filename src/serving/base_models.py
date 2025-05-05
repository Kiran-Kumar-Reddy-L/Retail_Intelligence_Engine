from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, AnyStr
from datetime import datetime, date


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
    order_id: AnyStr
    date: date
    status: AnyStr
    fulfilment: AnyStr
    sales_channel: AnyStr
    style: AnyStr
    sku: AnyStr
    category: AnyStr
    size: AnyStr
    qty: int
    amount: float
    ship_city: AnyStr
    ship_state: AnyStr
    ship_postal_code: int
    b2b: bool


class DailyRevenueRequest(BaseModel):
    """
    Request model for daily revenue insights.
    """
    ship_state: Optional[AnyStr] = Field(None, description="State to filter the data.")
    category: Optional[AnyStr] = Field(None, description="Category to filter the data.")
    sku: Optional[AnyStr] = Field(None, description="SKU to filter the data.")
    date_range: Optional[date] = Field(None, description="Date range to filter the data.")


class DailyRevenueResponse(BaseModel):
    """
    Response model for daily revenue insights.
    """    
    date: datetime
    revenue_per_day: str
    ship_state: Optional[AnyStr] = None
    category: Optional[AnyStr] = None
    sku: Optional[AnyStr] = None


class TopSkusRequest(BaseModel):
    """
    Request model for top SKUs insights.
    """
    month: Optional[AnyStr] = Field(None, description="Month to filter the data.")
    top_n: Optional[int] = Field(10, description="Number of top SKUs to return.")


class TopSkusResponse(BaseModel):
    """
    Response model for top SKUs insights.
    """    
    sku: AnyStr
    revenue_per_month: AnyStr
    order_count: int
    month: Optional[AnyStr] = None


class ASPOrderCountResponse(BaseModel):
    """
    Response model for ASP order count insights.
    """    
    sku: Optional[AnyStr] = None
    category: Optional[AnyStr] = None
    average_selling_price: str
    order_count: int