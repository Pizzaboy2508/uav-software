import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("Motor_Propeller.csv")
df.columns = df.columns.str.strip()

# Convert numeric columns
df["Kv Rating"] = pd.to_numeric(df["Kv Rating"], errors='coerce')
df["Imax (A)"] = pd.to_numeric(df["Imax (A)"], errors='coerce')
df["Vmax (V)"] = pd.to_numeric(df["Vmax (V)"], errors='coerce')
df["Pmax (W)"] = pd.to_numeric(df["Pmax (W)"], errors='coerce')
df["Diameter"] = pd.to_numeric(df["Diameter"], errors='coerce')
df["Pitch"] = pd.to_numeric(df["Pitch"], errors='coerce')
df["Thrust (g)"] = pd.to_numeric(df["Thrust (g)"], errors='coerce')

df = df.dropna(subset=["Diameter", "Pitch", "Kv Rating", "Imax (A)", "Vmax (V)"])

# --- Calculate correction factor using first 5 valid measured thrusts ---
C = 4.392e-8  # empirical constant (imperial units)
correction_ratios = []
reference_rows = df.dropna(subset=["Pmax (W)", "Thrust (g)"]).head(5)
for _, row in reference_rows.iterrows():
    kv = row["Kv Rating"]
    vmax = row["Vmax (V)"]
    imax = row["Imax (A)"]
    diameter = row["Diameter"]
    pitch = row["Pitch"]
    power = row["Pmax (W)"]
    measured_thrust = row["Thrust (g)"]
    throttle = power / (vmax * imax) if vmax * imax > 0 else 1.0
    throttle = np.clip(throttle, 0.1, 1.0)
    rpm = kv * vmax * throttle
    n = rpm / 60
    thrust_lbf = C * (diameter**4) * pitch * (n**2)
    thrust_g = thrust_lbf * 453.592
    if thrust_g > 0:
        correction_ratios.append(measured_thrust / thrust_g)
correction_factor = np.mean(correction_ratios) if correction_ratios else 1.0
print(f"Correction factor (average of first 5): {correction_factor:.3f}")

# --- Efficiency Plot ---
throttle_range = np.linspace(0.1, 1.0, 50)
plt.figure(figsize=(10, 6))

for _, row in df.iterrows():
    kv = row["Kv Rating"]
    vmax = row["Vmax (V)"]
    imax = row["Imax (A)"]
    diameter = row["Diameter"]
    pitch = row["Pitch"]
    model = row["Model"]

    thrusts = []
    powers = []
    efficiencies = []

    for throttle in throttle_range:
        voltage = vmax
        current = imax * throttle
        power = voltage * current
        rpm = kv * voltage * throttle
        n = rpm / 60
        thrust_lbf = C * (diameter**4) * pitch * (n**2)
        thrust_g = thrust_lbf * 453.592 * correction_factor
        thrusts.append(thrust_g)
        powers.append(power)
        efficiencies.append(thrust_g / power if power > 0 else 0)

    plt.plot(thrusts, efficiencies, label=f"{model} (Kv={kv:.0f})")

plt.title("Efficiency (Thrust/Power) vs Thrust")
plt.xlabel("Thrust (g)")
plt.ylabel("Efficiency (g/W)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show() 