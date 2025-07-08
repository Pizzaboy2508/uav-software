# Motor Propeller Thrust Simulation and Analysis

## Overview

This project provides a Python script to simulate and analyze the thrust performance of electric motor and propeller combinations for RC aircraft and drones. The script uses both theoretical modeling and real experimental data to calibrate its predictions, making it suitable for engineering analysis and reporting.

## Methodology

### 1. Theoretical Thrust Model
The script estimates static thrust using the following empirical formula:

```
T = C * D^4 * P * n^2
```
- **T**: Thrust (lbf, pounds-force)
- **C**: Empirical constant (default: 4.392e-8 for imperial units)
- **D**: Propeller diameter (inches)
- **P**: Propeller pitch (inches)
- **n**: Propeller rotational speed (revolutions per second)

The formula assumes ideal propeller conditions and does not account for all real-world losses.

### 2. Simulation Inputs
For each motor/propeller combination, the following parameters are required (all in SI or imperial units as noted):
- **Kv Rating** (RPM/V)
- **Imax (A)**: Maximum current
- **Vmax (V)**: Maximum voltage
- **Diameter** (inches)
- **Pitch** (inches)

The script simulates a range of throttle values (10% to 100%) to generate thrust vs. power curves.

### 3. Calibration with Experimental Data
To improve accuracy, the script calibrates the theoretical model using real measured thrust data:
- For the first 5 valid data points (where both measured thrust and power are available), the script computes the ratio of measured thrust to simulated thrust.
- The **correction factor** is the average of these ratios and is applied to all simulated thrust values.
- This ensures the simulation is empirically anchored to your real-world test data.

### 4. Output
- The script generates a plot of **Thrust (g)** vs **Power (W)** for each motor/propeller combination.
- Each curve is labeled with the motor model and Kv rating.
- The correction factor used is printed for traceability.

## Usage Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Data**
   - Place your `Motor_Propeller.csv` file in the project directory.
   - The CSV should include at least the following columns:
     - `Model`, `Kv Rating`, `Imax (A)`, `Vmax (V)`, `Diameter`, `Pitch`, `Pmax (W)`, `Thrust (g)`
   - Measured thrust and power are used for calibration; other rows are simulated only.

3. **Run the Simulation**
   ```bash
   python motor_prop_plot.py
   ```
   - The script will print the correction factor and display the plot.

## Engineering Notes
- **Empirical Correction:** The correction factor is essential for matching theory to practice. Always use measured data for calibration when available.
- **Units:** Ensure all inputs are in the correct units (diameter/pitch in inches, thrust in grams, power in watts).
- **Limitations:** The model assumes static thrust and does not account for inflight effects, air density changes, or detailed propeller/motor efficiency curves.
- **Reporting:** The script and methodology are suitable for inclusion in engineering reports. The calibration step should be described in your methods section, and the correction factor should be reported for transparency.

## Example CSV Format
| Model           | Kv Rating | Imax (A) | Vmax (V) | Diameter | Pitch | Pmax (W) | Thrust (g) |
|-----------------|-----------|----------|----------|----------|-------|----------|------------|
| Example Motor 1 | 1000      | 15.6     | 11.1     | 10       | 4.7   | 173      | 885        |
| ...             | ...       | ...      | ...      | ...      | ...   | ...      | ...        |

## License
This project is provided for educational and engineering analysis purposes. 