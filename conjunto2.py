import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import argparse

parser = argparse.ArgumentParser(description="Analyze sinusoidal force data from CSV files.")
parser.add_argument("files", nargs="+", help="List of CSV files to process")
args = parser.parse_args()
csv_files = args.files
# === 1. List of CSV files ===
#csv_files = ["Parafina1.csv", "Parafina2.csv","Parafina3.csv"]  # Add more filenames here
mass = 0.412  # kg

# === 2. Define sinusoidal model ===
def wave_model(x, A, k, phi, C):
    return A * np.sin(k * x + phi) + C

# === 3. Process each file ===
for filename in csv_files:
    df = pd.read_csv(filename)
    x_cm = df["position_cm"].values
    F_N = df["force_N"].values
    x_m = x_cm / 100  # convert to meters

    # Fit sinusoidal model
    params, _ = curve_fit(wave_model, x_m, F_N)
    A, k, phi, C = params
    k_eff = abs(A * k)
    omega = np.sqrt(k_eff / mass)
    f = omega / (2 * np.pi)
    T = 2 * np.pi / omega
    delta_U = 0.5 * k_eff * A**2
    F_max = A

    # === 4. Print results ===
    print(f"\n📄 File: {filename}")
    print(f"  F(x) = {A:.2f} * sin({k:.4f} * x + {phi:.2f}) + {C:.2f}")
    print("  Formulas:")
    print("    k_eff = |A * k|")
    print("    ω = sqrt(k_eff / m)")
    print("    f = ω / (2π)")
    print("    T = 2π / ω")
    print("    ΔU = 0.5 * k_eff * A^2")
    print("    F_max = A")
    print("  Values:")
    print(f"    Effective spring constant k_eff = {k_eff:.2f} N/m")
    print(f"    Angular frequency ω = {omega:.2f} rad/s")
    print(f"    Natural frequency f = {f:.2f} Hz")
    print(f"    Natural period T = {T:.3f} s")
    print(f"    Potential energy ΔU = {delta_U:.4f} J")
    print(f"    Maximum force F_max = {F_max:.2f} N")

    # === 5. Plot force vs position ===
    x_fit = np.linspace(x_m.min(), x_m.max(), 1000)
    F_fit = wave_model(x_fit, A, k, phi, C)

    plt.figure(figsize=(8, 4))
    plt.plot(x_m, F_N, 'o', label="Measured Force")
    plt.plot(x_fit, F_fit, '-', label="Fitted Wave", color="red")
    plt.xlabel("Position (m)")
    plt.ylabel("Force (N)")
    plt.title(f"{filename} — Force vs Position")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # === 6. Plot oscillator energy over time ===
    t = np.linspace(0, T, 500)
    E_t = 0.5 * k_eff * A**2 * np.sin(omega * t)**2

    plt.figure(figsize=(8, 3))
    plt.plot(t, E_t, color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Energy (J)")
    plt.title(f"{filename} — Oscillator Energy Over Time")
    plt.grid(True)
    plt.tight_layout()
    