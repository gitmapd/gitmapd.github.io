import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# === 1. Load CSV data ===
df = pd.read_csv("Parafina1.csv")
x_cm = df["position_cm"].values
F_N = df["force_N"].values

# === 2. Convert position to meters ===
x_m = x_cm / 100

# === 3. Define sinusoidal model ===
def sinusoidal_model(x, A, k, phi, C):
    return A * np.sin(k * x + phi) + C

# === 4. Fit sinusoidal model ===
params, _ = curve_fit(sinusoidal_model, x_m, F_N)
A, k, phi, C = params

# === 5. Define fitted wave function ===
def wave_function(x):
    return A * np.sin(k * x + phi) + C

# === 6. Estimate effective spring constant from sinusoid ===
k_eff = abs(A * k)

# === 7. Compute dynamics ===
mass_kg = 412 / 1000  # convert grams to kg
omega = np.sqrt(k_eff / mass_kg)
period = 2 * np.pi / omega
frequency = omega / (2 * np.pi)

# === 8. Estimate elastic constant from Hooke's law ===
# Select region near equilibrium (adjust range if needed)
mask = (x_m > 0.0) & (x_m < 0.1)
x_linear = x_m[mask]
F_linear = F_N[mask]

def linear_model(x, k):
    return -k * x

k_fit, _ = curve_fit(linear_model, x_linear, F_linear)
k_hooke = k_fit[0]

# === 9. Print results ===
#print("Fitted sinusoidal parameters:")
print(f"  Amplitude A       = {A:.2f} N")
print(f"  Wave number k     = {k:.4f} rad/m")
#print(f"  Phase shift φ     = {phi:.2f} rad")
#print(f"  Offset C          = {C:.2f} N")
#print("\nDerived quantities from sinusoidal fit:")
#print(f"  Effective k_eff   = {k_eff:.2f} N/m")
print(f"  Frequencia Angular = {omega:.2f} rad/s")
print(f"  Periodo Natural T  = {period:.3f} s")
print(f"  Frequencia Natural = {frequency:.2f} Hz")
#print("\nElastic constant from Hooke's law fit:")
print(f"  Constant Elastica = {k_hooke:.2f} N/m")
print(f"Modelo sinusoidal: F(x) = {A:.2f} * sin({k:.4f} * x + {phi:.2f}) + {C:.2f}")
# === 10. Plot original data, sinusoidal fit, and linear fit region ===
# Generate smooth x values for the fitted wave
x_fit = np.linspace(x_m.min(), x_m.max(), 1000)
F_fit = wave_function(x_fit)

# Generate linear fit values
F_linear_fit = linear_model(x_linear, k_hooke)

plt.figure(figsize=(10, 5))

# Plot measured data
plt.plot(x_m, F_N, 'o', label="Força Medida", alpha=0.5)

# Plot fitted sinusoidal wave
plt.plot(x_fit, F_fit, '-', label="Onda Sinusoidal", color="red")

# Plot linear fit near equilibrium
plt.plot(x_linear, F_linear_fit, '--', label="Equilibrio", color="green")

plt.xlabel("Posicao (m)")
plt.ylabel("Força (N)")
plt.title("Força vs Posicao")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()