import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path

# === 1. List of CSV files ===
csv_files = ["Parafina1.csv", "Parafina2.csv","Parafina3.csv"]  # Add more filenames here

# === 2. Define sinusoidal model ===
def wave_model(x, A, k, phi, C):
    return A * np.sin(k * x + phi) + C

# === 3. Prepare for individual plots ===
num_files = len(csv_files)
fig, axes = plt.subplots(num_files, 1, figsize=(10, 4 * num_files), sharex=True)

# === 4. Combined plot setup ===
plt.figure(figsize=(10, 6))
plt.title("Sinusoide Combinada")
plt.xlabel("Posicao (m)")
plt.ylabel("Força (N)")
plt.grid(True)

# === 5. Process each file ===
for i, filename in enumerate(csv_files):
    df = pd.read_csv(filename)
    x_cm = df["position_cm"].values
    F_N = df["force_N"].values
    x_m = x_cm / 100  # convert to meters
    
    # Fit sinusoidal model
    params, _ = curve_fit(wave_model, x_m, F_N)
    A, k, phi, C = params

    # Print results
    #print(f"\n📄 File: {Path(filename).stem}")
    print(f"\n {Path(filename).stem}")
    print(f"  F(x) = {A:.2f} * sin({k:.4f} * x + {phi:.2f}) + {C:.2f}")
    print(f"  Amplitude A      = {A:.2f} N")
    #print(f"  Wave number k    = {k:.4f} rad/m")
    #print(f"  Phase shift φ    = {phi:.2f} rad")
    #print(f"  Offset C         = {C:.2f} N")

    # Generate smooth fit
    x_fit = np.linspace(x_m.min(), x_m.max(), 1000)
    F_fit = wave_model(x_fit, A, k, phi, C)

    # === Individual subplot ===
    ax = axes[i] if num_files > 1 else axes
    ax.plot(x_m, F_N, 'o', label=f"{Path(filename).stem}")
    ax.plot(x_fit, F_fit, '-', label=f"{Path(filename).stem}", color="red")
    ax.set_ylabel("Força (N)")
    ax.set_title(f"{Path(filename).stem}")
    ax.grid(True)
    ax.legend()

    # === Add to combined plot ===
    plt.plot(x_fit, F_fit, '-', label=f"{Path(filename).stem}")
    plt.plot(x_m, F_N, 'o', alpha=0.4)

# === 6. Finalize combined plot ===
plt.legend()
plt.tight_layout()
plt.show()

# === 7. Show individual plots ===
fig.tight_layout()