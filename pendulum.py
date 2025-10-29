import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
m = 1.0     # pendulum mass
M = 2.0     # base mass
l = 1.0     # pendulum length
g = 9.81    # gravity

def dynamics(t, y):
    x, dx, theta, dtheta = y

    # Matrix form: A * [ddx, ddtheta] = b
    A = np.array([
        [M + m, m * l * np.cos(theta)],
        [m * l * np.cos(theta), m * l**2]
    ])
    b = np.array([
        m * l * dtheta**2 * np.sin(theta),
        -m * g * l * np.sin(theta)
    ])
    ddx, ddtheta = np.linalg.solve(A, b)

    return [dx, ddx, dtheta, ddtheta]

# Initial conditions: [x, dx, theta, dtheta]
y0 = [0.0, 0.0, np.pi / 4, 0.0]
t_span = (0, 10)
t_eval = np.linspace(*t_span, 1000)

sol = solve_ivp(dynamics, t_span, y0, t_eval=t_eval)

# Plotting
plt.plot(sol.t, sol.y[2])  # theta vs time
plt.xlabel("Time [s]")
plt.ylabel("Pendulum angle [rad]")
plt.title("Sliding Base Pendulum")
plt.grid()
plt.show()


from matplotlib.animation import FuncAnimation

# Extract positions
x = sol.y[0]
theta = sol.y[2]
x_bob = x + l * np.sin(theta)
y_bob = -l * np.cos(theta)

fig, ax = plt.subplots()
ax.set_xlim(min(x_bob) - l, max(x_bob) + l)
ax.set_ylim(-1.2 * l, 0.2 * l)
ax.set_aspect('equal')
ax.grid()

base_line, = ax.plot([], [], 'k-', lw=4)
rod_line, = ax.plot([], [], 'o-', lw=2, color='blue')

def update(frame):
    base_x = x[frame]
    bob_x = x_bob[frame]
    bob_y = y_bob[frame]

    base_line.set_data([base_x - 0.5, base_x + 0.5], [0, 0])
    rod_line.set_data([base_x, bob_x], [0, bob_y])
    return base_line, rod_line

ani = FuncAnimation(fig, update, frames=len(sol.t), interval=20, blit=True)
plt.title("Sliding Base Pendulum Animation")
plt.show()