import os
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd
import uvicorn
from fastapi import APIRouter, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.serving.base_models import (
    ASPOrderCountResponse,
    DailyRevenueRequest,
    DailyRevenueResponse,
    DataValidationSchema,
    LoadDataRequest,
    LoadDataResponse,
    ProcessDataResponse,
    TopSkusRequest,
    TopSkusResponse,
)
from src.serving.sale_insights import SaleInsights

# Create router
router = APIRouter()

# Create a single instance of SaleInsights
insights = SaleInsights(config="config.toml")

# Global state dictionary
app_state: Dict[str, Any] = {"raw_data": None, "processed_data": None}


def validate_data_availability():
    """Decorator to validate if data is available."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if app_state["processed_data"] is None:
                raise HTTPException(
                    status_code=400,
                    detail="No processed data available. Please process data first.",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def validate_column_value(column: str):
    """Decorator to validate if a column value exists in the data."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            value = kwargs.get(column)
            if value is not None:
                if value not in app_state["processed_data"][column].unique():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid {column}. Please check the available {column}s.",
                    )
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def filter_non_null_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out columns that contain only null values."""
    return df.loc[:, ~df.isna().all()]


@router.post("/load-data/", response_model=LoadDataResponse)
async def load_dataset(request: LoadDataRequest) -> LoadDataResponse:
    """
    Load the dataset from the specified path.
    """
    try:
        app_state["raw_data"] = insights.load_data(request.path)
        return LoadDataResponse(
            message="Data loaded successfully", status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/process-data/", response_model=ProcessDataResponse)
async def process_data() -> ProcessDataResponse:
    """
    Process the loaded dataset.
    """
    try:
        if app_state["raw_data"] is None:
            raise HTTPException(
                status_code=400, detail="No data loaded. Please load data first."
            )

        app_state["processed_data"] = insights.preprocess_data(app_state["raw_data"])
        app_state["processed_data"] = insights.derive_total_amount(
            app_state["processed_data"]
        )

        # Validate only the first row of the processed data
        if len(app_state["processed_data"]) > 0:
            first_row = app_state["processed_data"].iloc[0].to_dict()
            DataValidationSchema(**first_row)
        else:
            raise HTTPException(
                status_code=400, detail="No data records found after processing"
            )

        return ProcessDataResponse(
            message="Data preprocessed successfully", status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/insights/daily-revenue",
    response_model=List[DailyRevenueResponse],
    response_model_exclude_defaults=True,
)
@validate_data_availability()
@validate_column_value("ship_state")
@validate_column_value("category")
@validate_column_value("sku")
async def daily_revenue(
    ship_state: Optional[str] = Query(None, description="State to filter the data"),
    category: Optional[str] = Query(None, description="Category to filter the data"),
    sku: Optional[str] = Query(None, description="SKU to filter the data"),
) -> List[DailyRevenueResponse]:
    """
    Get the daily revenue insights.
    """
    try:
        # Define the group by columns based on the filter
        group_by = ["date"]
        filter_col = None
        filter_value = None

        if ship_state:
            group_by.append("ship_state")
            filter_col = "ship_state"
            filter_value = ship_state.lower()
        elif category:
            group_by.append("category")
            filter_col = "category"
            filter_value = category.lower()
        elif sku:
            group_by.append("sku")
            filter_col = "sku"
            filter_value = sku.lower()

        # Get revenue data
        revenue_df = insights.get_revenue_per_day(
            data=app_state["processed_data"], group_by=group_by
        )

        # Apply filter if needed
        if filter_col:
            revenue_df = revenue_df[revenue_df[filter_col] == filter_value]

        # Filter out null columns and convert to response models
        revenue_df = filter_non_null_columns(revenue_df)
        records = revenue_df.to_dict(orient="records")
        return [DailyRevenueResponse(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/insights/top-skus",
    response_model=List[TopSkusResponse],
    response_model_exclude_defaults=True,
)
@validate_data_availability()
@validate_column_value("month")
async def top_skus(
    month: str = Query(..., description="Month to filter the data"),
    top_n: int = Query(10, description="Number of top SKUs to return", ge=1, le=100),
) -> List[TopSkusResponse]:
    """
    Get the top SKUs insights.
    """
    try:
        # Get top SKUs data
        top_skus_df = insights.get_top_skus(
            data=app_state["processed_data"], group_by=["sku", "month"], top_n=top_n
        )

        top_skus_df = top_skus_df[top_skus_df["month"] == month.lower()]

        # Filter out null columns and convert to response models
        top_skus_df = filter_non_null_columns(top_skus_df)
        records = top_skus_df.to_dict(orient="records")
        return [TopSkusResponse(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/insights/asp-order-count",
    response_model=List[ASPOrderCountResponse],
    response_model_exclude_defaults=True,
)
@validate_data_availability()
async def asp_order_count(
    filter_by: Optional[str] = Query(None, description="Filter by SKU or Category")
) -> List[ASPOrderCountResponse]:
    """
    Get the ASP order count insights.
    """
    try:
        if filter_by == "sku":
            asp_order_count_df = insights.get_avg_selling_price_and_count(
                data=app_state["processed_data"], group_by=["sku"]
            )
        elif filter_by == "category":
            asp_order_count_df = insights.get_avg_selling_price_and_count(
                data=app_state["processed_data"], group_by=["category"]
            )
        else:
            asp_order_count_df = insights.get_avg_selling_price_and_count(
                data=app_state["processed_data"], group_by=["sku", "category"]
            )

        # Filter out null columns and convert to response models
        asp_order_count_df = filter_non_null_columns(asp_order_count_df)
        records = asp_order_count_df.to_dict(orient="records")
        return [ASPOrderCountResponse(**record) for record in records]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
