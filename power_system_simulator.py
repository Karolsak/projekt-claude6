#!/usr/bin/env python3
"""
Power System ODE Simulator with Tkinter GUI
Implements load frequency control with integral controller
Examples 7.9 and 7.10
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time


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


class PowerSystemSimulatorGUI:
    """Main GUI application for power system simulation"""

    def __init__(self, root):
        self.root = root
        self.root.title("Power System Load Frequency Control Simulator")
        self.root.geometry("1400x900")

        # Default parameters (Example 7.9)
        self.params = {
            'K_ps': tk.DoubleVar(value=104.0),
            't_ps': tk.DoubleVar(value=22.0),
            'R': tk.DoubleVar(value=3.0),
            't_sg': tk.DoubleVar(value=0.3),
            't_t': tk.DoubleVar(value=0.4),
            'ki': tk.DoubleVar(value=0.1),
            'delta_PL': tk.DoubleVar(value=0.48),
            't_sim': tk.DoubleVar(value=50.0),
            'dt': tk.DoubleVar(value=0.01)
        }

        self.solver_type = tk.StringVar(value="RK45")
        self.example_type = tk.StringVar(value="Example 7.9")
        self.with_integral = tk.BooleanVar(value=True)

        self.simulation_running = False
        self.simulation_thread = None

        self.setup_gui()
        self.run_simulation()

    def setup_gui(self):
        """Setup the GUI layout"""
        # Main container with grid
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure grid weights for automatic resizing
        main_container.grid_rowconfigure(0, weight=0)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=0)
        main_container.grid_columnconfigure(1, weight=1)

        # Left panel for controls
        control_panel = ttk.LabelFrame(main_container, text="Simulation Parameters", padding=10)
        control_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

        # Make control panel scrollable for smaller screens
        canvas = tk.Canvas(control_panel, width=350)
        scrollbar = ttk.Scrollbar(control_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Example selection
        ttk.Label(scrollable_frame, text="Select Example:", font=('Arial', 10, 'bold')).pack(pady=5)
        example_frame = ttk.Frame(scrollable_frame)
        example_frame.pack(pady=5)
        ttk.Radiobutton(example_frame, text="Example 7.9", variable=self.example_type,
                       value="Example 7.9", command=self.load_example).pack(side=tk.LEFT)
        ttk.Radiobutton(example_frame, text="Example 7.10", variable=self.example_type,
                       value="Example 7.10", command=self.load_example).pack(side=tk.LEFT)

        # Integral controller checkbox
        ttk.Checkbutton(scrollable_frame, text="With Integral Controller",
                       variable=self.with_integral, command=self.update_integral_control).pack(pady=5)

        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        # Parameter sliders
        self.create_slider(scrollable_frame, "Power System Gain (K_ps)", self.params['K_ps'], 10, 200, 0.1)
        self.create_slider(scrollable_frame, "Power System Time Const (t_ps) [s]", self.params['t_ps'], 1, 50, 0.1)
        self.create_slider(scrollable_frame, "Speed Regulation (R)", self.params['R'], 0.5, 10, 0.1)
        self.create_slider(scrollable_frame, "Governor Time Const (t_sg) [s]", self.params['t_sg'], 0.1, 2, 0.01)
        self.create_slider(scrollable_frame, "Turbine Time Const (t_t) [s]", self.params['t_t'], 0.1, 2, 0.01)
        self.create_slider(scrollable_frame, "Integral Gain (ki)", self.params['ki'], 0.0, 1.0, 0.01)
        self.create_slider(scrollable_frame, "Load Disturbance (ΔP_L) [p.u.]", self.params['delta_PL'], 0.0, 1.0, 0.01)
        self.create_slider(scrollable_frame, "Simulation Time [s]", self.params['t_sim'], 10, 100, 1)
        self.create_slider(scrollable_frame, "Time Step (dt) [s]", self.params['dt'], 0.001, 0.1, 0.001)

        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)

        # Solver selection
        ttk.Label(scrollable_frame, text="ODE Solver:", font=('Arial', 10, 'bold')).pack(pady=5)
        solver_frame = ttk.Frame(scrollable_frame)
        solver_frame.pack(pady=5)
        ttk.Radiobutton(solver_frame, text="RK45", variable=self.solver_type,
                       value="RK45").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(solver_frame, text="Euler", variable=self.solver_type,
                       value="Euler").pack(side=tk.LEFT, padx=5)

        # Simulation control buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=10)

        self.run_button = ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Top right panel for results
        results_panel = ttk.LabelFrame(main_container, text="Simulation Results", padding=10)
        results_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.results_text = tk.Text(results_panel, height=8, width=50, font=('Courier', 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Bottom right panel for plots
        plot_panel = ttk.LabelFrame(main_container, text="Dynamic Visualization", padding=10)
        plot_panel.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Configure plot panel to resize
        plot_panel.grid_rowconfigure(0, weight=1)
        plot_panel.grid_columnconfigure(0, weight=1)

        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 3)
        self.ax4 = self.fig.add_subplot(2, 2, 4)

        self.fig.tight_layout(pad=3.0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)

    def create_slider(self, parent, label, variable, from_, to, resolution):
        """Create a labeled slider"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=3)

        label_widget = ttk.Label(frame, text=label, width=35)
        label_widget.pack(side=tk.LEFT)

        value_label = ttk.Label(frame, text=f"{variable.get():.3f}", width=8)
        value_label.pack(side=tk.RIGHT)

        slider = ttk.Scale(frame, from_=from_, to=to, orient=tk.HORIZONTAL,
                          variable=variable, command=lambda v: self.update_slider_label(variable, value_label))
        slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)

        return slider

    def update_slider_label(self, variable, label):
        """Update slider value label"""
        label.config(text=f"{variable.get():.3f}")

    def load_example(self):
        """Load predefined example parameters"""
        if self.example_type.get() == "Example 7.9":
            # Example 7.9 parameters
            self.params['K_ps'].set(104.0)
            self.params['t_ps'].set(22.0)
            self.params['R'].set(3.0)
            self.params['t_sg'].set(0.3)
            self.params['t_t'].set(0.4)
            self.params['ki'].set(0.1)
            self.params['delta_PL'].set(0.48)
            self.params['t_sim'].set(50.0)
        else:  # Example 7.10
            # Example 7.10 parameters
            self.params['K_ps'].set(100.0)
            self.params['t_ps'].set(20.0)
            self.params['R'].set(2.5)
            self.params['t_sg'].set(0.3)
            self.params['t_t'].set(0.4)
            self.params['ki'].set(0.15)
            self.params['delta_PL'].set(0.02)
            self.params['t_sim'].set(50.0)

    def update_integral_control(self):
        """Update ki based on integral control checkbox"""
        if not self.with_integral.get():
            self.params['ki'].set(0.0)
        else:
            if self.example_type.get() == "Example 7.9":
                self.params['ki'].set(0.1)
            else:
                self.params['ki'].set(0.15)

    def run_simulation(self):
        """Run the simulation"""
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.simulation_running = True

        # Get parameters
        K_ps = self.params['K_ps'].get()
        t_ps = self.params['t_ps'].get()
        R = self.params['R'].get()
        t_sg = self.params['t_sg'].get()
        t_t = self.params['t_t'].get()
        ki = self.params['ki'].get()
        delta_PL = self.params['delta_PL'].get()
        t_sim = self.params['t_sim'].get()
        dt = self.params['dt'].get()

        # Create model
        model = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)

        # Initial conditions (all zeros)
        x0 = np.array([0.0, 0.0, 0.0, 0.0])

        # Select solver
        if self.solver_type.get() == "RK45":
            solver = RK45Solver(model)
        else:
            solver = EulerSolver(model)

        # Solve
        t, x = solver.solve(x0, (0, t_sim), dt)

        # Extract results
        delta_f = x[:, 0]  # Frequency deviation in Hz
        p_g = x[:, 1]      # Governor output
        p_t = x[:, 2]      # Turbine output

        # Calculate steady-state error
        steady_state_error = delta_f[-1]

        # Update results text
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"{'='*60}\n")
        self.results_text.insert(tk.END, f"{self.example_type.get()} Results\n")
        self.results_text.insert(tk.END, f"{'='*60}\n\n")
        self.results_text.insert(tk.END, f"Solver: {self.solver_type.get()}\n")
        self.results_text.insert(tk.END, f"Integral Controller: {'ON' if ki > 0 else 'OFF'}\n\n")
        self.results_text.insert(tk.END, f"System Parameters:\n")
        self.results_text.insert(tk.END, f"  K_ps = {K_ps:.2f}\n")
        self.results_text.insert(tk.END, f"  t_ps = {t_ps:.2f} s\n")
        self.results_text.insert(tk.END, f"  R = {R:.2f}\n")
        self.results_text.insert(tk.END, f"  t_sg = {t_sg:.2f} s\n")
        self.results_text.insert(tk.END, f"  t_t = {t_t:.2f} s\n")
        self.results_text.insert(tk.END, f"  ki = {ki:.3f}\n")
        self.results_text.insert(tk.END, f"  ΔP_L = {delta_PL:.3f} p.u.\n\n")
        self.results_text.insert(tk.END, f"Results:\n")
        self.results_text.insert(tk.END, f"  Peak Frequency Deviation: {np.min(delta_f):.6f} Hz\n")
        self.results_text.insert(tk.END, f"  Steady-State Error: {steady_state_error:.6f} Hz\n")
        self.results_text.insert(tk.END, f"  Settling Time: ~{t[np.argmax(np.abs(delta_f) < 0.01 * np.max(np.abs(delta_f)))]:.2f} s\n")

        # Plot results
        self.plot_results(t, delta_f, p_g, p_t, delta_PL)

        self.simulation_running = False
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def plot_results(self, t, delta_f, p_g, p_t, delta_PL):
        """Plot simulation results"""
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Plot 1: Frequency deviation
        self.ax1.plot(t, delta_f, 'b-', linewidth=2, label='Δf')
        self.ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        self.ax1.set_xlabel('Time (s)', fontsize=9)
        self.ax1.set_ylabel('Frequency Deviation (Hz)', fontsize=9)
        self.ax1.set_title('Frequency Deviation vs Time', fontsize=10, fontweight='bold')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.legend(fontsize=8)

        # Plot 2: Governor output
        self.ax2.plot(t, p_g, 'r-', linewidth=2, label='Governor Output')
        self.ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        self.ax2.set_xlabel('Time (s)', fontsize=9)
        self.ax2.set_ylabel('Governor Output (p.u.)', fontsize=9)
        self.ax2.set_title('Governor Response', fontsize=10, fontweight='bold')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.legend(fontsize=8)

        # Plot 3: Turbine output
        self.ax3.plot(t, p_t, 'g-', linewidth=2, label='Turbine Output')
        self.ax3.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        self.ax3.set_xlabel('Time (s)', fontsize=9)
        self.ax3.set_ylabel('Turbine Output (p.u.)', fontsize=9)
        self.ax3.set_title('Turbine Response', fontsize=10, fontweight='bold')
        self.ax3.grid(True, alpha=0.3)
        self.ax3.legend(fontsize=8)

        # Plot 4: Load disturbance and turbine output comparison
        self.ax4.plot(t, np.ones_like(t) * delta_PL, 'k--', linewidth=2, label='Load Disturbance')
        self.ax4.plot(t, p_t, 'g-', linewidth=2, label='Turbine Output')
        self.ax4.set_xlabel('Time (s)', fontsize=9)
        self.ax4.set_ylabel('Power (p.u.)', fontsize=9)
        self.ax4.set_title('Power Balance', fontsize=10, fontweight='bold')
        self.ax4.grid(True, alpha=0.3)
        self.ax4.legend(fontsize=8)

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()

    def stop_simulation(self):
        """Stop the simulation"""
        self.simulation_running = False
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def on_resize(self, event):
        """Handle window resize event"""
        # Only redraw if the window itself is being resized
        if event.widget == self.root:
            try:
                self.fig.tight_layout(pad=2.0)
                self.canvas.draw_idle()
            except Exception:
                pass  # Ignore resize errors during window transitions


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PowerSystemSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
