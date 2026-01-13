/**
 * Power Grid Simulation Platform - Frontend JavaScript
 * Handles UI interactions and API communication
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
let loadInput, loadSlider, generationInput, generationSlider;
let runSimulationBtn, resetInputsBtn;
let backendStatus, simulationMode;
let resultsSection, errorMessage, loadingOverlay;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    checkBackendHealth();
    
    // Check backend health every 30 seconds
    setInterval(checkBackendHealth, 30000);
});

/**
 * Initialize DOM element references
 */
function initializeElements() {
    // Input controls
    loadInput = document.getElementById('loadInput');
    loadSlider = document.getElementById('loadSlider');
    generationInput = document.getElementById('generationInput');
    generationSlider = document.getElementById('generationSlider');
    
    // Buttons
    runSimulationBtn = document.getElementById('runSimulation');
    resetInputsBtn = document.getElementById('resetInputs');
    
    // Status elements
    backendStatus = document.getElementById('backendStatus');
    simulationMode = document.getElementById('simulationMode');
    
    // Display elements
    resultsSection = document.getElementById('resultsSection');
    errorMessage = document.getElementById('errorMessage');
    loadingOverlay = document.getElementById('loadingOverlay');
}

/**
 * Setup event listeners for all interactive elements
 */
function setupEventListeners() {
    // Sync input fields with sliders
    loadInput.addEventListener('input', function() {
        loadSlider.value = this.value;
    });
    
    loadSlider.addEventListener('input', function() {
        loadInput.value = this.value;
    });
    
    generationInput.addEventListener('input', function() {
        generationSlider.value = this.value;
    });
    
    generationSlider.addEventListener('input', function() {
        generationInput.value = this.value;
    });
    
    // Button actions
    runSimulationBtn.addEventListener('click', runSimulation);
    resetInputsBtn.addEventListener('click', resetInputs);
    
    // Scenario buttons
    const scenarioBtns = document.querySelectorAll('.scenario-btn');
    scenarioBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const load = this.getAttribute('data-load');
            const gen = this.getAttribute('data-gen');
            setInputValues(load, gen);
        });
    });
}

/**
 * Check backend server health status
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        
        if (response.ok) {
            const data = await response.json();
            updateBackendStatus('online', data.simulation_mode);
        } else {
            updateBackendStatus('offline', '-');
        }
    } catch (error) {
        console.error('Backend health check failed:', error);
        updateBackendStatus('offline', '-');
    }
}

/**
 * Update backend status indicator
 */
function updateBackendStatus(status, mode) {
    backendStatus.textContent = status === 'online' ? 'Online' : 'Offline';
    backendStatus.className = `status-badge ${status}`;
    
    if (mode) {
        simulationMode.textContent = mode;
        simulationMode.className = 'status-badge online';
    }
}

/**
 * Set input values programmatically
 */
function setInputValues(load, generation) {
    loadInput.value = load;
    loadSlider.value = load;
    generationInput.value = generation;
    generationSlider.value = generation;
    
    // Auto-run simulation for scenarios
    runSimulation();
}

/**
 * Reset inputs to default values
 */
function resetInputs() {
    setInputValues(1000, 1000);
    hideError();
    resultsSection.style.display = 'none';
}

/**
 * Validate input values
 */
function validateInputs(load, generation) {
    if (load < 0 || generation < 0) {
        return 'Load and generation must be non-negative values.';
    }
    
    if (load > 100000 || generation > 100000) {
        return 'Values must not exceed 100,000 MW.';
    }
    
    if (isNaN(load) || isNaN(generation)) {
        return 'Please enter valid numeric values.';
    }
    
    return null; // Valid
}

/**
 * Run the grid simulation
 */
async function runSimulation() {
    // Get input values
    const load = parseFloat(loadInput.value);
    const generation = parseFloat(generationInput.value);
    
    // Validate inputs
    const validationError = validateInputs(load, generation);
    if (validationError) {
        showError(validationError);
        return;
    }
    
    hideError();
    showLoading(true);
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                load_mw: load,
                generation_mw: generation
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || errorData.detail || 'Simulation failed');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Simulation error:', error);
        showError(`Failed to run simulation: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * Display simulation results in the UI
 */
function displayResults(result) {
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Update stability banner
    const stabilityBanner = document.getElementById('stabilityBanner');
    const stabilityClass = result.stability_status.toLowerCase();
    stabilityBanner.className = `stability-banner ${stabilityClass}`;
    
    document.getElementById('stabilityIcon').textContent = '●';
    document.getElementById('stabilityText').textContent = result.stability_status;
    document.getElementById('warningMessage').textContent = result.warning;
    
    // Update metrics
    document.getElementById('powerImbalance').textContent = 
        `${result.power_imbalance_mw >= 0 ? '+' : ''}${result.power_imbalance_mw.toFixed(2)} MW`;
    
    document.getElementById('frequency').textContent = 
        `${result.system_frequency_hz.toFixed(4)} Hz`;
    
    document.getElementById('frequencyDeviation').textContent = 
        `${result.frequency_deviation_hz >= 0 ? '+' : ''}${result.frequency_deviation_hz.toFixed(4)} Hz deviation`;
    
    document.getElementById('voltage').textContent = 
        `${result.voltage_pu.toFixed(4)} pu`;
    
    document.getElementById('efficiency').textContent = 
        `${result.efficiency_percent.toFixed(1)}%`;
    
    // Update detailed information
    document.getElementById('resultLoad').textContent = 
        `${result.load_mw.toFixed(2)} MW`;
    
    document.getElementById('resultGeneration').textContent = 
        `${result.generation_mw.toFixed(2)} MW`;
    
    document.getElementById('stabilityIndex').textContent = 
        `${result.stability_index.toFixed(2)}`;
    
    document.getElementById('timestamp').textContent = 
        formatTimestamp(result.timestamp);
    
    document.getElementById('resultMode').textContent = 
        result.simulation_mode;
}

/**
 * Format timestamp for display
 */
function formatTimestamp(timestamp) {
    try {
        const date = new Date(timestamp);
        return date.toLocaleString();
    } catch (error) {
        return timestamp;
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
    runSimulationBtn.disabled = show;
}

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function(event) {
    // Enter key to run simulation
    if (event.key === 'Enter' && !runSimulationBtn.disabled) {
        runSimulation();
    }
    
    // Escape key to close results
    if (event.key === 'Escape') {
        resultsSection.style.display = 'none';
    }
});

/**
 * Format number with thousand separators
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Console message for developers
 */
console.log('%cPower Grid Simulation Platform', 'font-size: 20px; font-weight: bold; color: #2563eb;');
console.log('%cVersion 1.0.0', 'font-size: 12px; color: #64748b;');
console.log('%cAPI Base URL:', 'font-weight: bold;', API_BASE_URL);
