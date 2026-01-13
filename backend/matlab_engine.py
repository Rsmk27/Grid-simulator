"""
MATLAB Engine Connection Module

This module handles connection to MATLAB Engine and provides
a fallback simulation mode when MATLAB is not available.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global MATLAB engine instance
_matlab_engine = None
_matlab_available = False


def initialize_matlab_engine(matlab_path: Optional[str] = None) -> bool:
    """
    Initialize the MATLAB Engine connection.
    
    Args:
        matlab_path: Optional path to MATLAB installation
        
    Returns:
        bool: True if MATLAB Engine is successfully initialized, False otherwise
    """
    global _matlab_engine, _matlab_available
    
    try:
        import matlab.engine
        logger.info("Attempting to start MATLAB Engine...")
        
        if matlab_path:
            _matlab_engine = matlab.engine.start_matlab(f"-sd {matlab_path}")
        else:
            _matlab_engine = matlab.engine.start_matlab()
        
        # Add the matlab directory to MATLAB path
        try:
            _matlab_engine.addpath('../matlab', nargout=0)
            logger.info("Added matlab directory to MATLAB path")
        except Exception as e:
            logger.warning(f"Could not add matlab directory to path: {e}")
        
        _matlab_available = True
        logger.info("MATLAB Engine started successfully")
        return True
        
    except ImportError:
        logger.warning("MATLAB Engine for Python not installed. Using fallback simulation mode.")
        _matlab_available = False
        return False
    except Exception as e:
        logger.error(f"Failed to start MATLAB Engine: {e}")
        logger.warning("Using fallback simulation mode.")
        _matlab_available = False
        return False


def is_matlab_available() -> bool:
    """Check if MATLAB Engine is available."""
    return _matlab_available


def get_matlab_engine():
    """Get the MATLAB Engine instance."""
    if not _matlab_available:
        raise RuntimeError("MATLAB Engine is not available")
    return _matlab_engine


def shutdown_matlab_engine():
    """Shutdown the MATLAB Engine."""
    global _matlab_engine, _matlab_available
    
    if _matlab_engine is not None:
        try:
            _matlab_engine.quit()
            logger.info("MATLAB Engine shut down successfully")
        except Exception as e:
            logger.error(f"Error shutting down MATLAB Engine: {e}")
        finally:
            _matlab_engine = None
            _matlab_available = False


def run_matlab_simulation(load_mw: float, generation_mw: float) -> Dict[str, Any]:
    """
    Run the grid simulation using MATLAB Engine.
    
    Args:
        load_mw: Load in megawatts
        generation_mw: Generation in megawatts
        
    Returns:
        dict: Simulation results
    """
    if not _matlab_available or _matlab_engine is None:
        raise RuntimeError("MATLAB Engine is not available")
    
    try:
        # Call MATLAB function
        result = _matlab_engine.grid_simulation(float(load_mw), float(generation_mw))
        
        # Convert MATLAB struct to Python dict
        result_dict = {
            'timestamp': str(datetime.now().isoformat()),
            'load_mw': float(result['load_mw']),
            'generation_mw': float(result['generation_mw']),
            'power_imbalance_mw': float(result['power_imbalance_mw']),
            'system_frequency_hz': float(result['system_frequency_hz']),
            'frequency_deviation_hz': float(result['frequency_deviation_hz']),
            'voltage_pu': float(result['voltage_pu']),
            'stability_status': str(result['stability_status']),
            'stability_index': float(result['stability_index']),
            'efficiency_percent': float(result['efficiency_percent']),
            'warning': str(result['warning']),
            'simulation_mode': 'MATLAB'
        }
        
        return result_dict
        
    except Exception as e:
        logger.error(f"Error running MATLAB simulation: {e}")
        raise


def run_fallback_simulation(load_mw: float, generation_mw: float) -> Dict[str, Any]:
    """
    Run a Python-based fallback simulation when MATLAB is not available.
    This implements the same logic as the MATLAB function.
    
    Args:
        load_mw: Load in megawatts
        generation_mw: Generation in megawatts
        
    Returns:
        dict: Simulation results
    """
    # Input validation
    if load_mw < 0 or generation_mw < 0:
        raise ValueError("Load and generation must be non-negative")
    
    # Constants
    NOMINAL_FREQUENCY = 60.0  # Hz
    FREQUENCY_SENSITIVITY = 0.0001  # Hz per MW imbalance
    STABILITY_THRESHOLD = 50  # MW threshold for stable operation
    VOLTAGE_BASE = 1.0  # per unit
    VOLTAGE_SENSITIVITY = 0.00005  # pu per MW imbalance
    
    # Calculate power imbalance
    power_imbalance = generation_mw - load_mw
    
    # Calculate frequency deviation
    frequency_deviation = power_imbalance * FREQUENCY_SENSITIVITY
    system_frequency = NOMINAL_FREQUENCY + frequency_deviation
    
    # Calculate voltage stability
    voltage_pu = VOLTAGE_BASE + (power_imbalance * VOLTAGE_SENSITIVITY)
    voltage_pu = max(0.85, min(1.15, voltage_pu))
    
    # Determine stability status
    if abs(power_imbalance) <= STABILITY_THRESHOLD:
        stability_status = 'STABLE'
        stability_index = 1.0
    elif abs(power_imbalance) <= STABILITY_THRESHOLD * 2:
        stability_status = 'WARNING'
        stability_index = 0.5
    else:
        stability_status = 'CRITICAL'
        stability_index = 0.0
    
    # Calculate efficiency
    if generation_mw > 0:
        efficiency = min(load_mw / generation_mw * 100, 100)
    else:
        efficiency = 0
    
    # Generate warning message
    if stability_status == 'CRITICAL':
        if power_imbalance > 0:
            warning = 'CRITICAL: Excess generation detected. Reduce generation or increase load.'
        else:
            warning = 'CRITICAL: Load exceeds generation. Increase generation or shed load.'
    elif stability_status == 'WARNING':
        warning = 'WARNING: Power imbalance detected. System approaching instability.'
    else:
        warning = 'System operating within normal parameters.'
    
    # Build result dictionary
    result = {
        'timestamp': datetime.now().isoformat(),
        'load_mw': load_mw,
        'generation_mw': generation_mw,
        'power_imbalance_mw': power_imbalance,
        'system_frequency_hz': system_frequency,
        'frequency_deviation_hz': frequency_deviation,
        'voltage_pu': voltage_pu,
        'stability_status': stability_status,
        'stability_index': stability_index,
        'efficiency_percent': efficiency,
        'warning': warning,
        'simulation_mode': 'PYTHON_FALLBACK'
    }
    
    return result


def run_simulation(load_mw: float, generation_mw: float) -> Dict[str, Any]:
    """
    Run the grid simulation using MATLAB if available, otherwise use fallback.
    
    Args:
        load_mw: Load in megawatts
        generation_mw: Generation in megawatts
        
    Returns:
        dict: Simulation results
    """
    if _matlab_available:
        try:
            return run_matlab_simulation(load_mw, generation_mw)
        except Exception as e:
            logger.error(f"MATLAB simulation failed, falling back to Python: {e}")
            return run_fallback_simulation(load_mw, generation_mw)
    else:
        return run_fallback_simulation(load_mw, generation_mw)
