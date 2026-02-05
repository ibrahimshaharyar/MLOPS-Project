import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize FastAPI app
app = FastAPI(
    title="Student Performance Prediction API",
    description="ML-powered student performance prediction with analytics dashboard",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")


# Health check endpoint for monitoring
@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {"status": "healthy", "service": "student-performance-api"}


# Home page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})


# Prediction page (GET - show form)
@app.get("/predict", response_class=HTMLResponse)
async def predict_page(request: Request):
    """Render the prediction form page"""
    return templates.TemplateResponse("predict.html", {"request": request})


# Prediction endpoint (POST - process form)
@app.post("/predict", response_class=HTMLResponse)
async def predict_datapoint(
    request: Request,
    gender: str = Form(...),
    ethnicity: str = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str = Form(...),
    test_preparation_course: str = Form(...),
    writing_score: float = Form(...),
    reading_score: float = Form(...)
):
    """
    Process student data and return math score prediction
    
    Note: reading_score and writing_score are swapped in the form
    to match the CustomData constructor signature
    """
    try:
        # Create CustomData object
        data = CustomData(
            gender=gender,
            race_ethnicity=ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=float(writing_score),  # Note: swapped as in original
            writing_score=float(reading_score)
        )
        
        # Get data as DataFrame
        pred_df = data.get_data_as_data_frame()
        print(pred_df)
        
        # Make prediction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        # Return result
        return templates.TemplateResponse(
            "predict.html",
            {
                "request": request,
                "results": results[0]
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "predict.html",
            {
                "request": request,
                "error": f"Prediction error: {str(e)}"
            }
        )


# Dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the analytics dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


# API Routes for Dashboard Data
@app.get("/api/dashboard/summary")
async def get_dashboard_summary():
    """Get summary statistics for dashboard"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_summary_statistics()


@app.get("/api/dashboard/distributions")
async def get_score_distributions():
    """Get score distribution data for histograms"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_score_distributions()


@app.get("/api/dashboard/gender")
async def get_gender_data():
    """Get gender distribution data"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_gender_distribution()


@app.get("/api/dashboard/race")
async def get_race_data():
    """Get race/ethnicity distribution data"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_race_distribution()


@app.get("/api/dashboard/lunch")
async def get_lunch_data():
    """Get lunch type distribution data"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_lunch_distribution()


@app.get("/api/dashboard/test-prep")
async def get_test_prep_data():
    """Get test preparation course distribution data"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_test_prep_distribution()


@app.get("/api/dashboard/scores-by-gender")
async def get_scores_by_gender():
    """Get scores grouped by gender for box plots"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_scores_by_gender()


@app.get("/api/dashboard/correlation")
async def get_correlation():
    """Get correlation matrix for scores"""
    from app.services.analytics import get_analytics_service
    service = get_analytics_service()
    return service.get_correlation_matrix()


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Set to False in production
    )
