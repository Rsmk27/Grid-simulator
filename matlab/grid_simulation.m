function result = grid_simulation(load_mw, generation_mw)
    % GRID_SIMULATION - Basic power grid simulation function
    %
    % This function simulates a simplified power grid by calculating:
    % - Power balance (generation vs load)
    % - System stability status
    % - Frequency deviation
    % - Voltage stability indicator
    %
    % Inputs:
    %   load_mw       - Total system load in MW (scalar)
    %   generation_mw - Total system generation in MW (scalar)
    %
    % Output:
    %   result - Structure containing simulation results
    %
    % Example:
    %   result = grid_simulation(1000, 1050);
    %   disp(result);
    
    % Input validation
    if nargin < 2
        error('grid_simulation:InvalidInput', 'Both load_mw and generation_mw are required');
    end
    
    if ~isnumeric(load_mw) || ~isnumeric(generation_mw)
        error('grid_simulation:InvalidType', 'Inputs must be numeric');
    end
    
    if load_mw < 0 || generation_mw < 0
        error('grid_simulation:InvalidValue', 'Inputs must be non-negative');
    end
    
    % Constants
    NOMINAL_FREQUENCY = 60.0; % Hz
    FREQUENCY_SENSITIVITY = 0.0001; % Hz per MW imbalance
    STABILITY_THRESHOLD = 50; % MW threshold for stable operation
    VOLTAGE_BASE = 1.0; % per unit
    VOLTAGE_SENSITIVITY = 0.00005; % pu per MW imbalance
    
    % Calculate power imbalance
    power_imbalance = generation_mw - load_mw;
    
    % Calculate frequency deviation
    % Positive imbalance (excess generation) -> higher frequency
    % Negative imbalance (excess load) -> lower frequency
    frequency_deviation = power_imbalance * FREQUENCY_SENSITIVITY;
    system_frequency = NOMINAL_FREQUENCY + frequency_deviation;
    
    % Calculate voltage stability (simplified model)
    % Assumes voltage drops with power deficit, rises with surplus
    voltage_pu = VOLTAGE_BASE + (power_imbalance * VOLTAGE_SENSITIVITY);
    voltage_pu = max(0.85, min(1.15, voltage_pu)); % Clamp between 0.85 and 1.15 pu
    
    % Determine stability status
    if abs(power_imbalance) <= STABILITY_THRESHOLD
        stability_status = 'STABLE';
        stability_index = 1.0;
    elseif abs(power_imbalance) <= STABILITY_THRESHOLD * 2
        stability_status = 'WARNING';
        stability_index = 0.5;
    else
        stability_status = 'CRITICAL';
        stability_index = 0.0;
    end
    
    % Calculate efficiency (simple model)
    if generation_mw > 0
        efficiency = min(load_mw / generation_mw * 100, 100);
    else
        efficiency = 0;
    end
    
    % Build result structure
    result = struct();
    result.timestamp = datetime('now');
    result.load_mw = load_mw;
    result.generation_mw = generation_mw;
    result.power_imbalance_mw = power_imbalance;
    result.system_frequency_hz = system_frequency;
    result.frequency_deviation_hz = frequency_deviation;
    result.voltage_pu = voltage_pu;
    result.stability_status = stability_status;
    result.stability_index = stability_index;
    result.efficiency_percent = efficiency;
    
    % Add warnings/recommendations
    if strcmp(stability_status, 'CRITICAL')
        if power_imbalance > 0
            result.warning = 'CRITICAL: Excess generation detected. Reduce generation or increase load.';
        else
            result.warning = 'CRITICAL: Load exceeds generation. Increase generation or shed load.';
        end
    elseif strcmp(stability_status, 'WARNING')
        result.warning = 'WARNING: Power imbalance detected. System approaching instability.';
    else
        result.warning = 'System operating within normal parameters.';
    end
    
end
