# Backend Bridge (Python FastAPI)

## Overview
This directory contains the Python FastAPI backend server that bridges the web interface with the MATLAB simulation engine. The backend provides REST API endpoints for running simulations and includes a fallback mode for when MATLAB is not available.

## Files
- **main.py** - FastAPI server with REST endpoints
- **matlab_engine.py** - MATLAB Engine connection module with fallback simulation
- **requirements.txt** - Python package dependencies
- **README.md** - This documentation file

## Prerequisites
- Python 3.8 or later (tested with Python 3.12)
- pip package manager

## Installation

### Step 1: Create Virtual Environment (Recommended)
```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install MATLAB Engine for Python (Optional)
If you have MATLAB 2023b installed and want to use it:

```bash
# Navigate to MATLAB Engine setup directory
# On Windows:
cd "C:\Program Files\MATLAB\R2023b\extern\engines\python"

# On Linux/Mac:
cd /usr/local/MATLAB/R2023b/extern/engines/python

# Install MATLAB Engine
python setup.py install
```

**Note:** The backend works without MATLAB installed. It will automatically use a Python fallback simulation that implements the same logic as the MATLAB function.

## Running the Server

### Start the Backend Server
```bash
cd backend
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

### Server Startup Messages
You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

If MATLAB is not available, you'll see:
```
WARNING:  MATLAB Engine for Python not installed. Using fallback simulation mode.
```

This is normal and the system will work correctly using the Python fallback.

## API Endpoints

### 1. Root Endpoint
**GET** `/`

Returns API information and available endpoints.

```bash
curl http://localhost:8000/
```

### 2. Health Check
**GET** `/health`

Check server status and MATLAB availability.

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "matlab_available": false,
  "simulation_mode": "PYTHON_FALLBACK"
}
```

### 3. Run Simulation
**POST** `/api/simulate`

Run a grid simulation with specified load and generation values.

**Request Body:**
```json
{
  "load_mw": 1000,
  "generation_mw": 1050
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"load_mw": 1000, "generation_mw": 1050}'
```

**Response:**
```json
{
  "timestamp": "2024-01-13T18:30:00.123456",
  "load_mw": 1000.0,
  "generation_mw": 1050.0,
  "power_imbalance_mw": 50.0,
  "system_frequency_hz": 60.005,
  "frequency_deviation_hz": 0.005,
  "voltage_pu": 1.0025,
  "stability_status": "STABLE",
  "stability_index": 1.0,
  "efficiency_percent": 95.24,
  "warning": "System operating within normal parameters.",
  "simulation_mode": "PYTHON_FALLBACK"
}
```

### 4. System Status
**GET** `/api/status`

Get detailed system status information.

```bash
curl http://localhost:8000/api/status
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the Swagger UI interface.

## Testing the Backend

### Manual Testing with curl

1. **Test Health Check:**
```bash
curl http://localhost:8000/health
```

2. **Test Balanced System:**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"load_mw": 1000, "generation_mw": 1000}'
```

3. **Test Excess Generation (Warning):**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"load_mw": 1000, "generation_mw": 1080}'
```

4. **Test Critical Imbalance:**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"load_mw": 1000, "generation_mw": 1150}'
```

### Testing with Python

```python
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Run simulation
data = {
    'load_mw': 1000,
    'generation_mw': 1050
}
response = requests.post('http://localhost:8000/api/simulate', json=data)
print(response.json())
```

## Simulation Modes

The backend supports two simulation modes:

### 1. MATLAB Mode
- Uses MATLAB Engine for Python
- Calls the actual MATLAB `grid_simulation.m` function
- Requires MATLAB 2023b installed
- Indicated by `"simulation_mode": "MATLAB"` in responses

### 2. Python Fallback Mode
- Pure Python implementation
- No MATLAB required
- Implements identical logic to MATLAB function
- Automatically used when MATLAB is not available
- Indicated by `"simulation_mode": "PYTHON_FALLBACK"` in responses

Both modes produce equivalent results and follow the same simulation logic.

## Input Validation

The API validates all inputs:
- Load and generation must be non-negative numbers
- Values must not exceed 100,000 MW (100 GW)
- Invalid inputs return HTTP 400 with error details

## Error Handling

The API provides clear error messages:

**Invalid Input (400):**
```json
{
  "error": "Value must be non-negative",
  "status_code": 400
}
```

**Server Error (500):**
```json
{
  "error": "Simulation failed: <details>",
  "status_code": 500
}
```

## CORS Configuration

The backend is configured to accept requests from any origin (`allow_origins=["*"]`). 

For production deployment, update the CORS settings in `main.py`:
```python
allow_origins=["http://yourdomain.com", "https://yourdomain.com"]
```

## Connecting to MATLAB

When MATLAB is available, the backend:
1. Starts a MATLAB Engine session on startup
2. Adds the `../matlab` directory to the MATLAB path
3. Calls `grid_simulation.m` for each API request
4. Converts MATLAB struct results to JSON
5. Closes the MATLAB session on shutdown

## Performance Notes

- **MATLAB Mode**: First simulation may take 10-15 seconds due to MATLAB startup
- **Python Fallback**: Instant response (<10ms)
- The MATLAB Engine stays running between requests for faster subsequent simulations

## Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
# Use a different port
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Module Import Errors
Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### MATLAB Connection Issues
If MATLAB Engine fails to connect:
1. Verify MATLAB Engine for Python is installed
2. Check MATLAB license is valid
3. Ensure no other MATLAB instances are running
4. The system will automatically fall back to Python mode

### CORS Errors from Frontend
If the web interface can't connect:
1. Ensure backend is running on the expected port
2. Check CORS configuration in `main.py`
3. Verify network/firewall settings

## Development Tips

### Enable Auto-Reload
The server automatically reloads when code changes (using `--reload` flag):
```bash
uvicorn main:app --reload
```

### View Logs
The server logs all requests and simulation results. Increase verbosity if needed:
```bash
uvicorn main:app --log-level debug
```

### Test MATLAB Connection
To test MATLAB Engine connection separately:
```python
from matlab_engine import initialize_matlab_engine, is_matlab_available

if initialize_matlab_engine():
    print("MATLAB Engine connected successfully!")
else:
    print("MATLAB not available, using fallback mode")
```

## Next Steps

After verifying the backend works correctly:
1. Test all endpoints using Swagger UI at http://localhost:8000/docs
2. Verify simulation results match expected values
3. Proceed to Phase 3: Web Interface
4. Connect the web frontend to these API endpoints
