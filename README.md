# Power Grid Simulation Platform

A complete web-based smart grid digital twin platform for simulating power grid operations. This system demonstrates the integration of MATLAB simulation engines with modern web technologies to create an interactive grid monitoring and control interface.

## 🎯 Project Overview

This platform provides a working end-to-end system consisting of:
- **MATLAB 2023b Simulation Layer**: Core grid simulation with power balance calculations
- **Python FastAPI Backend**: REST API bridge between MATLAB and web interface
- **Modern Web Frontend**: Interactive dashboard for control and visualization

## ✨ Features

- ⚡ Real-time power grid simulation
- 📊 Live visualization of system metrics
- 🎛️ Interactive load and generation controls
- 🔄 Automatic fallback when MATLAB is unavailable
- 🎯 Pre-configured test scenarios
- 📱 Fully responsive design
- 🔒 Input validation and error handling
- 📈 Stability analysis and warnings

## 🏗️ System Architecture

```
┌─────────────────┐
│  Web Frontend   │  (HTML/CSS/JavaScript)
│  Port: 8080     │  - User Interface
└────────┬────────┘  - Input Controls
         │           - Results Display
         │ HTTP/JSON
         ▼
┌─────────────────┐
│  FastAPI Backend│  (Python)
│  Port: 8000     │  - REST API Endpoints
└────────┬────────┘  - MATLAB Engine Bridge
         │           - Fallback Simulation
         │ MATLAB Engine API
         ▼
┌─────────────────┐
│  MATLAB Engine  │  (MATLAB 2023b)
│                 │  - Grid Simulation Logic
└─────────────────┘  - Scientific Computing
```

## 📁 Project Structure

```
Grid-simulator/
├── matlab/                      # MATLAB Simulation Core (Phase 1)
│   ├── grid_simulation.m       # Main simulation function
│   ├── test_simulation.m       # Test script
│   └── README.md               # MATLAB documentation
│
├── backend/                     # Python FastAPI Backend (Phase 2)
│   ├── main.py                 # FastAPI server
│   ├── matlab_engine.py        # MATLAB Engine connection
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Backend documentation
│
├── frontend/                    # Web Interface (Phase 3)
│   ├── index.html              # Main HTML page
│   ├── styles.css              # Styling
│   ├── script.js               # JavaScript logic
│   └── README.md               # Frontend documentation
│
├── README.md                    # This file (main documentation)
└── .gitignore                  # Git ignore rules
```

## 🚀 Quick Start Guide

### Prerequisites

- **MATLAB 2023b** (optional - system works with Python fallback)
- **Python 3.8+** (tested with Python 3.12)
- **Modern Web Browser** (Chrome, Firefox, Safari, or Edge)

### Step 1: MATLAB Setup (Optional)

If you have MATLAB 2023b:

```bash
# Test MATLAB simulation locally
cd matlab
# Open MATLAB and run:
# >> test_simulation
```

To enable Python-MATLAB integration:
```bash
# Navigate to MATLAB Engine for Python directory
cd "C:\Program Files\MATLAB\R2023b\extern\engines\python"  # Windows
# or
cd /usr/local/MATLAB/R2023b/extern/engines/python           # Linux/Mac

# Install MATLAB Engine
python setup.py install
```

**📝 Note**: The system works perfectly without MATLAB using Python fallback mode!

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend will start on **http://localhost:8000**

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Start a simple HTTP server
python3 -m http.server 8080
```

The frontend will be available at **http://localhost:8080**

### Step 4: Access the Application

1. Open your web browser
2. Go to **http://localhost:8080**
3. Check that "Backend Status" shows "Online"
4. Enter load and generation values
5. Click "Run Simulation"
6. View the results!

## 📖 Detailed Documentation

Each component has detailed documentation in its respective directory:

- **[MATLAB Documentation](matlab/README.md)** - Simulation function details, testing, and MATLAB Engine setup
- **[Backend Documentation](backend/README.md)** - API endpoints, configuration, and troubleshooting
- **[Frontend Documentation](frontend/README.md)** - UI features, customization, and browser compatibility

## 🧪 Testing the System

### Complete System Test

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

3. **Open Browser**:
   - Navigate to http://localhost:8080
   - Verify backend status shows "Online"

4. **Test Scenarios**:
   - Click "Balanced" scenario → Should show STABLE
   - Click "Critical Surplus" → Should show CRITICAL with red warning
   - Enter custom values and run simulation
   - Verify results update correctly

### API Testing

Test the backend API directly:

```bash
# Health check
curl http://localhost:8000/health

# Run simulation
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"load_mw": 1000, "generation_mw": 1050}'
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Understanding Simulation Results

### Stability Status

| Status | Imbalance | Color | Meaning |
|--------|-----------|-------|---------|
| **STABLE** | ≤ 50 MW | 🟢 Green | Normal operation |
| **WARNING** | 50-100 MW | 🟡 Yellow | Approaching instability |
| **CRITICAL** | > 100 MW | 🔴 Red | Immediate action required |

### Key Metrics

- **Power Imbalance**: Difference between generation and load
  - Positive (+): Excess generation
  - Negative (-): Insufficient generation
  
- **System Frequency**: Normally 60.00 Hz
  - Higher: Excess generation
  - Lower: Power deficit
  
- **Voltage**: Nominal 1.0 per-unit (pu)
  - Range: 0.85 - 1.15 pu
  
- **Efficiency**: Load/Generation ratio
  - 100% when perfectly balanced
  - Lower indicates wasted capacity

## 🔧 Configuration

### Backend Port

Edit `backend/main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Change port here
```

### Frontend API URL

Edit `frontend/script.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';  // Change URL here
```

## 🐛 Troubleshooting

### Backend Won't Start

**Error: "Address already in use"**
```bash
# Find process using port 8000
lsof -i :8000          # Mac/Linux
netstat -ano | find "8000"  # Windows

# Kill the process or use a different port
uvicorn main:app --port 8001
```

**Error: "Module not found"**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Can't Connect to Backend

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check API_BASE_URL in `frontend/script.js`
3. Ensure CORS is enabled in backend (it is by default)
4. Try using a local server instead of opening HTML directly

### MATLAB Connection Issues

If MATLAB Engine fails:
- System automatically uses Python fallback (no action needed!)
- Check MATLAB Engine for Python installation
- Verify MATLAB license is valid
- Ensure no other MATLAB sessions are running

## 🔒 Security Considerations

For development (current setup):
- ✅ CORS allows all origins
- ✅ No authentication required
- ✅ Runs on localhost only

For production deployment:
- 🔐 Configure specific CORS origins
- 🔐 Add authentication/authorization
- 🔐 Use HTTPS for all connections
- 🔐 Implement rate limiting
- 🔐 Add input sanitization
- 🔐 Set up proper firewall rules

## 📈 Extending the Platform

This is a starter version. You can extend it by:

### MATLAB Simulation
- Add multiple bus/node networks
- Implement real power flow equations
- Add renewable energy sources (solar, wind)
- Include energy storage systems
- Add generator dynamics models
- Implement fault scenarios

### Backend API
- Add historical data storage (database)
- Implement WebSocket for real-time updates
- Add user authentication
- Create simulation scheduling
- Add data export features (CSV, JSON)

### Frontend Interface
- Add real-time charts and graphs
- Implement network topology visualization
- Add historical trend analysis
- Create mobile app version
- Add multi-language support
- Implement dark mode theme

## 🎓 Learning Resources

### MATLAB Resources
- [MATLAB Power System Analysis](https://www.mathworks.com/solutions/power-electronics-control.html)
- [MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)

### FastAPI Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Web Development
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 🤝 Contributing

This is a starter platform designed for expansion. When adding features:

1. Maintain the modular structure
2. Update relevant README files
3. Test all changes thoroughly
4. Ensure backward compatibility
5. Document new features

## 📝 Version History

- **v1.0.0** (Initial Release)
  - MATLAB simulation engine
  - Python FastAPI backend with fallback mode
  - Web-based frontend interface
  - Pre-configured test scenarios
  - Comprehensive documentation

## 📄 License

This project is provided as-is for educational and development purposes.

## 🙋 Support

For issues or questions:
1. Check the relevant README file (MATLAB, Backend, or Frontend)
2. Review the Troubleshooting section
3. Check browser console for errors (F12)
4. Verify all prerequisites are installed

## 🎉 Success Indicators

You have successfully set up the platform when:

✅ Backend shows "Started server" message  
✅ Frontend loads in browser  
✅ Backend status shows "Online"  
✅ Simulation mode is displayed (MATLAB or PYTHON_FALLBACK)  
✅ Running a simulation returns results  
✅ Results display correctly with stability status  
✅ Quick scenarios work properly  

## 🚀 Next Steps

Now that you have a working platform:

1. **Familiarize Yourself**: Test all scenarios and features
2. **Customize**: Adjust colors, add scenarios, modify ranges
3. **Extend**: Add new simulation features or UI components
4. **Deploy**: Set up for production with proper security
5. **Scale**: Add databases, user management, advanced features

---

**Built with ❤️ using MATLAB 2023b, FastAPI, and Modern Web Technologies**
