# MATLAB Simulation Core

## Overview
This directory contains the MATLAB simulation engine for the Power Grid Simulation Platform. The core simulation function models basic power grid behavior including power balance, frequency regulation, and stability assessment.

## Files
- **grid_simulation.m** - Main simulation function
- **test_simulation.m** - Test script to verify simulation functionality
- **README.md** - This documentation file

## Prerequisites
- MATLAB 2023b or later
- No additional toolboxes required for basic functionality

## Testing the Simulation Locally

### Step 1: Navigate to MATLAB Directory
```matlab
cd /path/to/Grid-simulator/matlab
```

### Step 2: Run Test Script
```matlab
test_simulation
```

This will execute multiple test scenarios and display results for:
- Balanced system operation
- Excess generation scenarios
- Excess load scenarios
- Warning and critical conditions
- Various load levels

### Step 3: Manual Testing
You can also test the function manually:

```matlab
% Example: Test with 1000 MW load and 1050 MW generation
result = grid_simulation(1000, 1050);

% Display the complete result structure
disp(result);

% Access specific fields
fprintf('Stability Status: %s\n', result.stability_status);
fprintf('System Frequency: %.4f Hz\n', result.system_frequency_hz);
fprintf('Voltage: %.4f pu\n', result.voltage_pu);
```

## Simulation Function Details

### Function Signature
```matlab
result = grid_simulation(load_mw, generation_mw)
```

### Inputs
- **load_mw**: Total system load in megawatts (MW) - must be non-negative
- **generation_mw**: Total system generation in megawatts (MW) - must be non-negative

### Output Structure
The function returns a structure with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| timestamp | datetime | Time of simulation |
| load_mw | double | Input load value |
| generation_mw | double | Input generation value |
| power_imbalance_mw | double | Difference between generation and load |
| system_frequency_hz | double | Calculated system frequency |
| frequency_deviation_hz | double | Deviation from nominal 60 Hz |
| voltage_pu | double | Voltage in per-unit (pu) |
| stability_status | string | 'STABLE', 'WARNING', or 'CRITICAL' |
| stability_index | double | Numerical stability indicator (0-1) |
| efficiency_percent | double | System efficiency percentage |
| warning | string | Descriptive warning or status message |

### Stability Criteria
- **STABLE**: Power imbalance ≤ 50 MW
- **WARNING**: Power imbalance between 50-100 MW
- **CRITICAL**: Power imbalance > 100 MW

## Preparing for External Access

### Installing MATLAB Engine for Python

To enable Python to call MATLAB functions, you need to install the MATLAB Engine API for Python.

#### Step 1: Locate MATLAB Installation
Find your MATLAB installation directory (e.g., `C:\Program Files\MATLAB\R2023b` on Windows or `/usr/local/MATLAB/R2023b` on Linux/Mac).

#### Step 2: Navigate to Engine Setup Directory
```bash
# On Windows
cd "C:\Program Files\MATLAB\R2023b\extern\engines\python"

# On Linux/Mac
cd /usr/local/MATLAB/R2023b/extern/engines/python
```

#### Step 3: Install the Engine
```bash
# Install for current user
python setup.py install --user

# Or install system-wide (may require admin/sudo)
sudo python setup.py install
```

#### Step 4: Verify Installation
```python
# Test in Python
import matlab.engine
eng = matlab.engine.start_matlab()
print("MATLAB Engine successfully connected!")
eng.quit()
```

### Alternative: Using MATLAB Compiler
If you prefer not to use MATLAB Engine, you can:
1. Compile MATLAB functions to standalone executables
2. Use MATLAB Runtime for deployment
3. Call compiled functions from Python using subprocess

## Expected Behavior

### Normal Operation
```matlab
result = grid_simulation(1000, 1000);
% Result shows STABLE status, frequency ~60 Hz, voltage ~1.0 pu
```

### Excess Generation
```matlab
result = grid_simulation(1000, 1100);
% Result shows frequency > 60 Hz, stability may show WARNING
```

### Excess Load
```matlab
result = grid_simulation(1100, 1000);
% Result shows frequency < 60 Hz, stability may show WARNING
```

## Extending the Simulation

This is a simplified model. You can extend it by:
- Adding multiple buses/nodes
- Implementing real power flow equations
- Adding renewable energy sources with variability
- Including energy storage systems
- Adding detailed generator dynamics
- Implementing fault scenarios
- Adding economic dispatch calculations

## Troubleshooting

### Error: "Undefined function or variable"
- Ensure you're in the correct directory: `cd /path/to/matlab`
- Verify the file `grid_simulation.m` exists

### Error: "Invalid input"
- Check that both load and generation values are provided
- Ensure values are numeric and non-negative

### MATLAB Engine Connection Issues
- Verify MATLAB Engine for Python is installed correctly
- Check Python version compatibility (Python 3.8-3.11 for MATLAB 2023b)
- Ensure MATLAB license is valid and not in use by another session

## Next Steps
After verifying the MATLAB simulation works correctly:
1. Install MATLAB Engine for Python (see above)
2. Proceed to Phase 2: Backend Bridge (Python)
3. Test the Python-MATLAB connection before building the full API
