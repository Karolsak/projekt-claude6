# Power System Load Frequency Control Simulator

A comprehensive Python Tkinter application for simulating power system load frequency control with integral controller action.

## Features

### Dynamic Simulation
- **Real-time ODE Solvers**: Choose between RK45 (Runge-Kutta 4th order) and Euler methods
- **Interactive Parameter Control**: Adjust all system parameters dynamically using sliders
- **Automatic Window Resizing**: GUI adapts to different window sizes

### Visualization
- **Dynamic Graphs**: Real-time plotting of:
  - Frequency deviation (Δf) vs time
  - Governor output response
  - Turbine output response
  - Power balance comparison
- **Results Display**: Comprehensive simulation statistics including:
  - Peak frequency deviation
  - Steady-state error
  - Settling time

### Examples Implemented

#### Example 7.9
An isolated control area with:
- Power system gain constant: K_ps = 104
- Power system time constant: t_ps = 22 s
- Speed regulation: R = 3
- Governor time constant: t_sg = 0.3 s
- Turbine time constant: t_t = 0.4 s
- Integral controller gain: ki = 0.1
- Step-load change: 0.48 p.u.

#### Example 7.10
An isolated control area with:
- Power system gain constant: K_ps = 100
- Power system time constant: t_ps = 20 s
- Speed regulation: R = 2.5
- Governor time constant: t_sg = 0.3 s
- Turbine time constant: t_t = 0.4 s
- Integral controller gain: ki = 0.15
- Step-load disturbance: 2% (0.02 p.u.)
- Compare with and without integral control

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (usually comes with Python)
- numpy
- matplotlib

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Simulator
```bash
python3 power_system_simulator.py
```

### GUI Controls

1. **Example Selection**:
   - Choose between Example 7.9 and Example 7.10
   - Automatically loads preset parameters

2. **Integral Controller**:
   - Toggle ON/OFF to compare system behavior with and without integral control

3. **Parameter Sliders**:
   - **K_ps**: Power system gain constant (10 - 200)
   - **t_ps**: Power system time constant (1 - 50 s)
   - **R**: Speed regulation (0.5 - 10)
   - **t_sg**: Governor time constant (0.1 - 2 s)
   - **t_t**: Turbine time constant (0.1 - 2 s)
   - **ki**: Integral controller gain (0 - 1)
   - **ΔP_L**: Load disturbance (0 - 1 p.u.)
   - **Simulation Time**: Duration of simulation (10 - 100 s)
   - **dt**: Time step for solver (0.001 - 0.1 s)

4. **ODE Solver Selection**:
   - **RK45**: 4th order Runge-Kutta (more accurate)
   - **Euler**: Forward Euler method (faster but less accurate)

5. **Simulation Control**:
   - **Run Simulation**: Execute simulation with current parameters
   - **Stop**: Halt ongoing simulation

## System Model

The power system model implements load frequency control with the following components:

### State Variables
- **x[0]**: Δf - Frequency deviation (Hz)
- **x[1]**: Governor output (p.u.)
- **x[2]**: Turbine output (p.u.)
- **x[3]**: Integral of frequency (for controller)

### Differential Equations

1. **Power System**:
   ```
   dΔf/dt = (K_ps/t_ps) * (p_t - ΔP_L) - (1/t_ps) * Δf
   ```

2. **Governor**:
   ```
   dp_g/dt = (1/t_sg) * ((-1/R) * Δf - Δp_c) - (1/t_sg) * p_g
   ```

3. **Turbine**:
   ```
   dp_t/dt = (1/t_t) * p_g - (1/t_t) * p_t
   ```

4. **Integral Controller**:
   ```
   d(integral_f)/dt = Δf
   Δp_c = ki * integral_f
   ```

## ODE Solvers

### RK45 (Runge-Kutta 4th Order)
Classic 4th order Runge-Kutta method providing high accuracy with moderate computational cost.

### Euler Method
Simple forward Euler method - faster but requires smaller time steps for accuracy.

## Results Interpretation

### Frequency Deviation Plot
Shows how the system frequency deviates from nominal (50 Hz) following a load disturbance. With integral control, the steady-state error should approach zero.

### Governor Response
Displays the governor's corrective action in response to frequency deviation.

### Turbine Response
Shows how the turbine output changes to match the load disturbance.

### Power Balance
Compares the load disturbance with the turbine output, illustrating how the system compensates for the disturbance.

## Key Observations

1. **With Integral Control (ki > 0)**:
   - Steady-state frequency error approaches zero
   - System takes longer to settle
   - Better frequency regulation

2. **Without Integral Control (ki = 0)**:
   - Non-zero steady-state frequency error
   - Faster settling time
   - Proportional error to load disturbance

## Troubleshooting

### Import Errors
If you encounter import errors for tkinter:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: tkinter should be included with Python

### Display Issues
If plots don't display correctly, try:
- Resizing the window
- Clicking "Run Simulation" again
- Adjusting your system's DPI settings

## Technical Notes

- Default time step (dt = 0.01 s) provides good balance between accuracy and speed
- RK45 solver is recommended for most simulations
- Smaller time steps improve accuracy but increase computation time
- All parameters can be adjusted in real-time without restarting the application

## License

This simulator is provided for educational purposes.

## Author

Created for power system analysis and education, implementing Examples 7.9 and 7.10 from power system control theory.
