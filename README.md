# Retail Intelligence Engine API

A FastAPI-based API for retail data analysis and insights.

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Load Data
Loads the dataset from the specified path.

```http
POST /load-data/
```

**Request Body:**
```json
{
    "path": "path/to/your/data.csv"
}
```

**Response:**
```json
{
    "message": "Data loaded successfully",
    "status_code": 200
}
```

#### 2. Process Data
Processes the loaded dataset.

```http
POST /process-data/
```

**Response:**
```json
{
    "message": "Data preprocessed successfully",
    "status_code": 200
}
```

#### 3. Daily Revenue Insights
Get daily revenue insights with optional filtering.

```http
GET /insights/daily-revenue
```

**Query Parameters:**
- `ship_state` (optional): Filter by state
- `category` (optional): Filter by category
- `sku` (optional): Filter by SKU

**Response:**
```json
[
    {
        "date": "2024-01-01T00:00:00",
        "revenue_per_day": "1000",
        "ship_state": "california"  // Only included if filtered by state
    }
]
```

#### 4. Top SKUs Insights
Get insights about top-performing SKUs.

```http
GET /insights/top-skus
```

**Query Parameters:**
- `month` (required): Month to filter the data
- `top_n` (optional, default=10): Number of top SKUs to return (1-100)

**Response:**
```json
[
    {
        "sku": "ABC123",
        "revenue_per_month": "5000",
        "order_count": 10,
        "month": "january"
    }
]
```

#### 5. ASP Order Count Insights
Get average selling price and order count insights.

```http
GET /insights/asp-order-count
```

**Query Parameters:**
- `filter_by` (optional): Filter by "sku" or "category"

**Response:**
```json
[
    {
        "sku": "ABC123",  // Only included if filtered by SKU
        "category": "clothing",  // Only included if filtered by category
        "average_selling_price": "100",
        "order_count": 5
    }
]
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request (e.g., invalid parameters, missing data)
- 404: Not Found
- 500: Internal Server Error

## Data Validation

The API includes validation for:
- Required fields
- Data types
- Value ranges
- Column existence in the dataset

## Notes

- All monetary values are returned as strings to maintain precision
- Dates are returned in ISO 8601 format
- Filter values are case-insensitive
- The API automatically excludes null values from responses
