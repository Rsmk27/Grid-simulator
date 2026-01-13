% TEST_SIMULATION - Test script for grid_simulation function
%
% This script tests the grid_simulation function with various scenarios
% to verify correct operation.

clear all;
close all;
clc;

fprintf('=== Testing Grid Simulation Function ===\n\n');

%% Test Case 1: Balanced System
fprintf('Test 1: Balanced System (Load = Generation)\n');
result1 = grid_simulation(1000, 1000);
display_result(result1);

%% Test Case 2: Excess Generation
fprintf('\nTest 2: Slight Excess Generation (Stable)\n');
result2 = grid_simulation(1000, 1020);
display_result(result2);

%% Test Case 3: Excess Load
fprintf('\nTest 3: Slight Excess Load (Stable)\n');
result3 = grid_simulation(1050, 1000);
display_result(result3);

%% Test Case 4: Warning - Large Imbalance
fprintf('\nTest 4: Large Imbalance (Warning)\n');
result4 = grid_simulation(1000, 1080);
display_result(result4);

%% Test Case 5: Critical - Very Large Imbalance
fprintf('\nTest 5: Critical Imbalance\n');
result5 = grid_simulation(1000, 1150);
display_result(result5);

%% Test Case 6: Low Load Scenario
fprintf('\nTest 6: Low Load Scenario\n');
result6 = grid_simulation(100, 105);
display_result(result6);

%% Test Case 7: High Load Scenario
fprintf('\nTest 7: High Load Scenario\n');
result7 = grid_simulation(5000, 5000);
display_result(result7);

%% Test Case 8: Zero Load
fprintf('\nTest 8: Zero Load\n');
result8 = grid_simulation(0, 100);
display_result(result8);

fprintf('\n=== All Tests Completed ===\n');

%% Helper function to display results
function display_result(result)
    fprintf('  Load: %.2f MW\n', result.load_mw);
    fprintf('  Generation: %.2f MW\n', result.generation_mw);
    fprintf('  Power Imbalance: %.2f MW\n', result.power_imbalance_mw);
    fprintf('  System Frequency: %.4f Hz\n', result.system_frequency_hz);
    fprintf('  Voltage: %.4f pu\n', result.voltage_pu);
    fprintf('  Stability: %s (Index: %.2f)\n', result.stability_status, result.stability_index);
    fprintf('  Efficiency: %.2f%%\n', result.efficiency_percent);
    fprintf('  Status: %s\n', result.warning);
end
