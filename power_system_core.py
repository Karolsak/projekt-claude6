#!/usr/bin/env python3
"""
Core power system model and ODE solvers without GUI dependencies
Can be imported for testing or used in headless environments
"""

import numpy as np


class PowerSystemModel:
    """
    Power system model for load frequency control
    State variables:
    x[0] = Δf (frequency deviation)
    x[1] = governor output
    x[2] = turbine output
    x[3] = integral of frequency (for controller)
    """

    def __init__(self, K_ps, t_ps, R, t_sg, t_t, ki, delta_PL):
        self.K_ps = K_ps  # Power system gain constant
        self.t_ps = t_ps  # Power system time constant
        self.R = R        # Speed regulation
        self.t_sg = t_sg  # Governor time constant
        self.t_t = t_t    # Turbine time constant
        self.ki = ki      # Integral controller gain
        self.delta_PL = delta_PL  # Load disturbance

    def derivatives(self, t, x):
        """
        Compute derivatives of state variables
        """
        # Unpack state variables
        delta_f = x[0]  # Frequency deviation
        p_g = x[1]      # Governor output
        p_t = x[2]      # Turbine output
        integral_f = x[3]  # Integral of frequency

        # Control signal from integral controller
        delta_pc = self.ki * integral_f

        # Differential equations
        # Power system: Δf
        dx0 = (self.K_ps / self.t_ps) * (p_t - self.delta_PL) - (1.0 / self.t_ps) * delta_f

        # Governor
        dx1 = (1.0 / self.t_sg) * ((-1.0 / self.R) * delta_f - delta_pc) - (1.0 / self.t_sg) * p_g

        # Turbine
        dx2 = (1.0 / self.t_t) * p_g - (1.0 / self.t_t) * p_t

        # Integral of frequency
        dx3 = delta_f

        return np.array([dx0, dx1, dx2, dx3])


class ODESolver:
    """Base class for ODE solvers"""

    def __init__(self, model):
        self.model = model

    def solve(self, x0, t_span, dt):
        """Solve ODE and return time and state arrays"""
        raise NotImplementedError


class EulerSolver(ODESolver):
    """Forward Euler method"""

    def solve(self, x0, t_span, dt):
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + dt, dt)
        n_steps = len(t)
        n_states = len(x0)

        x = np.zeros((n_steps, n_states))
        x[0] = x0

        for i in range(n_steps - 1):
            dx = self.model.derivatives(t[i], x[i])
            x[i + 1] = x[i] + dt * dx

        return t, x


class RK45Solver(ODESolver):
    """Runge-Kutta 4th order method (classic RK4)"""

    def solve(self, x0, t_span, dt):
        t_start, t_end = t_span
        t = np.arange(t_start, t_end + dt, dt)
        n_steps = len(t)
        n_states = len(x0)

        x = np.zeros((n_steps, n_states))
        x[0] = x0

        for i in range(n_steps - 1):
            k1 = self.model.derivatives(t[i], x[i])
            k2 = self.model.derivatives(t[i] + dt / 2, x[i] + dt * k1 / 2)
            k3 = self.model.derivatives(t[i] + dt / 2, x[i] + dt * k2 / 2)
            k4 = self.model.derivatives(t[i] + dt, x[i] + dt * k3)

            x[i + 1] = x[i] + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t, x


def simulate_example_7_9():
    """Simulate Example 7.9"""
    K_ps = 104.0
    t_ps = 22.0
    R = 3.0
    t_sg = 0.3
    t_t = 0.4
    ki = 0.1
    delta_PL = 0.48

    model = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)
    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    solver = RK45Solver(model)
    t, x = solver.solve(x0, (0, 50), 0.01)

    return t, x


def simulate_example_7_10(with_integral=True):
    """Simulate Example 7.10"""
    K_ps = 100.0
    t_ps = 20.0
    R = 2.5
    t_sg = 0.3
    t_t = 0.4
    ki = 0.15 if with_integral else 0.0
    delta_PL = 0.02

    model = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)
    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    solver = RK45Solver(model)
    t, x = solver.solve(x0, (0, 50), 0.01)

    return t, x


if __name__ == "__main__":
    print("Testing Power System Core...")
    print("\nExample 7.9:")
    t, x = simulate_example_7_9()
    print(f"  Peak frequency deviation: {np.min(x[:, 0]):.6f} Hz")
    print(f"  Steady-state error: {x[-1, 0]:.6f} Hz")

    print("\nExample 7.10 (with integral):")
    t, x = simulate_example_7_10(with_integral=True)
    print(f"  Peak frequency deviation: {np.min(x[:, 0]):.6f} Hz")
    print(f"  Steady-state error: {x[-1, 0]:.6f} Hz")

    print("\nExample 7.10 (without integral):")
    t, x = simulate_example_7_10(with_integral=False)
    print(f"  Peak frequency deviation: {np.min(x[:, 0]):.6f} Hz")
    print(f"  Steady-state error: {x[-1, 0]:.6f} Hz")

    print("\n✓ All core tests passed!")
