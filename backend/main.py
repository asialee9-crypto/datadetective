from services.investigation import generate_investigation_report

from pydantic import BaseModel
from typing import Any
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.encoders import jsonable_encoder

from io import BytesIO
from typing import Literal
import os

import pandas as pd

from services.data_profiler import profile_dataset
from services.hypothesis import generate_hypotheses
from services.investigator import investigate_hypothesis

# Create FastAPI application
app = FastAPI(
    title="DataDetective API",
    description="AI-powered data science investigation platform",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI

# Allow DataDetective React frontend to access FastAPI

default_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",
]

configured_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins + configured_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# -----------------------------------------
# PYDANTIC MODELS
# -----------------------------------------

class InvestigationReportRequest(BaseModel):
    hypothesis: str
    statistical_results: dict[str, Any]

# Maximum CSV file size: 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024


# Homepage endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to DataDetective!",
        "status": "running"
    }


# Dataset upload endpoint
@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    # Step 1: Validate file type
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    # Step 2: Read uploaded file
    content = await file.read(MAX_FILE_SIZE + 1)

    # Step 3: Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 5 MB."
        )

    # Step 4: Read CSV using pandas
    try:
        df = pd.read_csv(BytesIO(content))
        import json

# Prepare data for frontend visualizations
        chart_df = df.head(500).copy()

# Replace missing values with JSON-compatible nulls
        chart_data = json.loads(
        chart_df.to_json(orient="records")
)
            
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file."
        )

    # Step 5: Check for empty dataset
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The dataset is empty."
        )

    # Step 6: Limit dataset dimensions
    if len(df) > 100_000 or len(df.columns) > 100:
        raise HTTPException(
            status_code=400,
            detail="Dataset exceeds supported row or column limits."
        )

    # Step 7: Collect dataset information
    dataset_info = {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "chart_data": chart_data,
        "column_names": df.columns.tolist(),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values": {
            column: int(count)
            for column, count in df.isnull().sum().items()
        },
        "preview": df.head(5).to_dict(orient="records")
    }

# Generate a detailed statistical profile
    dataset_profile = profile_dataset(df)

# Add the profile to the API response
    dataset_info["profile"] = dataset_profile

    return jsonable_encoder(dataset_info)

@app.post("/generate-hypotheses")
async def generate_dataset_hypotheses(
    file: UploadFile = File(...)
):

    # Validate file extension
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    # Limit uploaded file size
    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 5 MB limit."
        )

    # Read the dataset
    try:
        df = pd.read_csv(BytesIO(content))

    except (
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
        UnicodeDecodeError
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file."
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty."
        )

    if len(df) > 100_000 or len(df.columns) > 100:
        raise HTTPException(
            status_code=400,
            detail="Dataset exceeds supported dimensions."
        )

    # Generate the dataset profile
    profile = profile_dataset(df)

    # Generate AI hypotheses
    try:
        hypotheses = generate_hypotheses(profile)

    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to contact the AI model."
        )

    return {
        "filename": file.filename,
        "dataset_rows": len(df),
        "dataset_columns": len(df.columns),
        "hypotheses": hypotheses["hypotheses"]
    }

# -----------------------------------------
# STEP 7: STATISTICAL INVESTIGATION ENDPOINT
# -----------------------------------------

@app.post("/investigate")
async def investigate(
    hypothesis: str = Form(...),
    column1: str = Form(...),
    column2: str = Form(...),
    recommended_test: Literal[
        "pearson_correlation",
        "chi_square",
        "welch_t_test"
    ] = Form(...),
    file: UploadFile = File(...)
):

    # STEP 1: Validate the uploaded file
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    # STEP 2: Read the CSV file
    content = await file.read(MAX_FILE_SIZE + 1)

    # STEP 3: Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 5 MB limit."
        )

    # STEP 4: Convert CSV into a pandas DataFrame
    try:
        df = pd.read_csv(BytesIO(content))

    except (
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
        UnicodeDecodeError
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file."
        )

    # STEP 5: Check whether the dataset is empty
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty."
        )

    # STEP 6: Check dataset dimensions
    if len(df) > 100_000 or len(df.columns) > 100:
        raise HTTPException(
            status_code=400,
            detail="Dataset exceeds supported dimensions."
        )

    # STEP 7: Organize the hypothesis information
    hypothesis_data = {
        "hypothesis": hypothesis,
        "columns": [column1, column2],
        "recommended_test": recommended_test
    }

    # STEP 8: Run the statistical investigation
    try:
        result = investigate_hypothesis(
            df,
            hypothesis_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Investigation failed."
        )

    # STEP 9: Return the results
    return result

# -----------------------------------------
# AI INVESTIGATION REPORT ENDPOINT
# -----------------------------------------

@app.post("/investigation/report")
async def create_investigation_report(
    request: InvestigationReportRequest
):

    report = generate_investigation_report(
        hypothesis=request.hypothesis,
        statistical_results=request.statistical_results
    )

    return {
        "hypothesis": request.hypothesis,
        "statistical_results": request.statistical_results,
        "report": report
    }
