"""
FastAPI Backend Server for Power Grid Simulation Platform

This server provides REST API endpoints to run grid simulations
and retrieve results. It connects to MATLAB Engine when available.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import logging
from contextlib import asynccontextmanager

from matlab_engine import (
    initialize_matlab_engine,
    shutdown_matlab_engine,
    is_matlab_available,
    run_simulation
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for request/response validation
class SimulationRequest(BaseModel):
    """Request model for simulation endpoint"""
    load_mw: float = Field(..., ge=0, description="System load in megawatts (MW)")
    generation_mw: float = Field(..., ge=0, description="System generation in megawatts (MW)")
    
    @field_validator('load_mw', 'generation_mw')
    @classmethod
    def validate_reasonable_values(cls, v):
        if v > 100000:  # 100 GW seems like a reasonable upper limit
            raise ValueError('Value exceeds reasonable limit (100,000 MW)')
        return v


class SimulationResponse(BaseModel):
    """Response model for simulation endpoint"""
    timestamp: str
    load_mw: float
    generation_mw: float
    power_imbalance_mw: float
    system_frequency_hz: float
    frequency_deviation_hz: float
    voltage_pu: float
    stability_status: str
    stability_index: float
    efficiency_percent: float
    warning: str
    simulation_mode: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    matlab_available: bool
    simulation_mode: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Initialize MATLAB Engine
    logger.info("Starting up FastAPI server...")
    initialize_matlab_engine()
    
    yield
    
    # Shutdown: Close MATLAB Engine
    logger.info("Shutting down FastAPI server...")
    shutdown_matlab_engine()


# Create FastAPI application
app = FastAPI(
    title="Power Grid Simulation API",
    description="REST API for simulating power grid operations",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow requests from web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Power Grid Simulation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "simulate": "/api/simulate",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns server status and MATLAB availability.
    """
    matlab_status = is_matlab_available()
    
    return {
        "status": "healthy",
        "matlab_available": matlab_status,
        "simulation_mode": "MATLAB" if matlab_status else "PYTHON_FALLBACK"
    }


@app.post("/api/simulate", response_model=SimulationResponse)
async def simulate_grid(request: SimulationRequest):
    """
    Run a grid simulation with specified load and generation values.
    
    Args:
        request: SimulationRequest containing load_mw and generation_mw
        
    Returns:
        SimulationResponse with simulation results
        
    Raises:
        HTTPException: If simulation fails
    """
    try:
        logger.info(f"Running simulation: Load={request.load_mw} MW, Generation={request.generation_mw} MW")
        
        # Run the simulation
        result = run_simulation(request.load_mw, request.generation_mw)
        
        logger.info(f"Simulation completed: Status={result['stability_status']}")
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}"
        )


@app.get("/api/status")
async def get_system_status():
    """
    Get detailed system status information.
    """
    return {
        "server": "running",
        "matlab_engine": {
            "available": is_matlab_available(),
            "mode": "MATLAB" if is_matlab_available() else "PYTHON_FALLBACK"
        },
        "api_version": "1.0.0"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
