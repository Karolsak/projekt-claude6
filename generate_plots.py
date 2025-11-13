#!/usr/bin/env python3
"""
Generate plots for power system examples without GUI
Saves plots to files for documentation and analysis
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from power_system_core import PowerSystemModel, RK45Solver, EulerSolver


def plot_example_7_9():
    """Generate plots for Example 7.9"""
    print("Generating plots for Example 7.9...")

    # Example 7.9 parameters
    K_ps = 104.0
    t_ps = 22.0
    R = 3.0
    t_sg = 0.3
    t_t = 0.4
    ki = 0.1
    delta_PL = 0.48

    # Create model and solve
    model = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)
    x0 = np.array([0.0, 0.0, 0.0, 0.0])
    solver = RK45Solver(model)
    t, x = solver.solve(x0, (0, 50), 0.01)

    # Extract results
    delta_f = x[:, 0]
    p_g = x[:, 1]
    p_t = x[:, 2]

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Example 7.9: Power System Response with Integral Control', fontsize=14, fontweight='bold')

    # Plot 1: Frequency deviation
    axes[0, 0].plot(t, delta_f, 'b-', linewidth=2)
    axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0, 0].set_xlabel('Time (s)', fontsize=10)
    axes[0, 0].set_ylabel('Frequency Deviation (Hz)', fontsize=10)
    axes[0, 0].set_title('Frequency Deviation vs Time', fontsize=11, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].text(0.02, 0.98, f'Steady-state error: {delta_f[-1]:.6f} Hz\nPeak deviation: {np.min(delta_f):.6f} Hz',
                    transform=axes[0, 0].transAxes, fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Plot 2: Governor output
    axes[0, 1].plot(t, p_g, 'r-', linewidth=2)
    axes[0, 1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0, 1].set_xlabel('Time (s)', fontsize=10)
    axes[0, 1].set_ylabel('Governor Output (p.u.)', fontsize=10)
    axes[0, 1].set_title('Governor Response', fontsize=11, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Turbine output
    axes[1, 0].plot(t, p_t, 'g-', linewidth=2)
    axes[1, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1, 0].set_xlabel('Time (s)', fontsize=10)
    axes[1, 0].set_ylabel('Turbine Output (p.u.)', fontsize=10)
    axes[1, 0].set_title('Turbine Response', fontsize=11, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Power balance
    axes[1, 1].plot(t, np.ones_like(t) * delta_PL, 'k--', linewidth=2, label='Load Disturbance')
    axes[1, 1].plot(t, p_t, 'g-', linewidth=2, label='Turbine Output')
    axes[1, 1].set_xlabel('Time (s)', fontsize=10)
    axes[1, 1].set_ylabel('Power (p.u.)', fontsize=10)
    axes[1, 1].set_title('Power Balance', fontsize=11, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('example_7_9_results.png', dpi=300, bbox_inches='tight')
    print("  Saved: example_7_9_results.png")
    plt.close()


def plot_example_7_10():
    """Generate plots for Example 7.10"""
    print("Generating plots for Example 7.10...")

    # Example 7.10 parameters
    K_ps = 100.0
    t_ps = 20.0
    R = 2.5
    t_sg = 0.3
    t_t = 0.4
    ki_with = 0.15
    ki_without = 0.0
    delta_PL = 0.02

    # Simulate with integral control
    model_with = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki_with, delta_PL)
    x0 = np.array([0.0, 0.0, 0.0, 0.0])
    solver = RK45Solver(model_with)
    t_with, x_with = solver.solve(x0, (0, 50), 0.01)

    # Simulate without integral control
    model_without = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki_without, delta_PL)
    solver = RK45Solver(model_without)
    t_without, x_without = solver.solve(x0, (0, 50), 0.01)

    # Extract results
    delta_f_with = x_with[:, 0]
    delta_f_without = x_without[:, 0]
    p_g_with = x_with[:, 1]
    p_g_without = x_without[:, 1]
    p_t_with = x_with[:, 2]
    p_t_without = x_without[:, 2]

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Example 7.10: Comparison With and Without Integral Control', fontsize=14, fontweight='bold')

    # Plot 1: Frequency deviation comparison
    axes[0, 0].plot(t_with, delta_f_with, 'b-', linewidth=2, label='With Integral Control (ki=0.15)')
    axes[0, 0].plot(t_without, delta_f_without, 'r--', linewidth=2, label='Without Integral Control (ki=0)')
    axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0, 0].set_xlabel('Time (s)', fontsize=10)
    axes[0, 0].set_ylabel('Frequency Deviation (Hz)', fontsize=10)
    axes[0, 0].set_title('Frequency Deviation Comparison', fontsize=11, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend(fontsize=8)

    # Plot 2: Steady-state error comparison
    axes[0, 1].bar(['With Integral\n(ki=0.15)', 'Without Integral\n(ki=0)'],
                   [abs(delta_f_with[-1]), abs(delta_f_without[-1])],
                   color=['blue', 'red'], alpha=0.7)
    axes[0, 1].set_ylabel('Steady-State Error (Hz)', fontsize=10)
    axes[0, 1].set_title('Steady-State Error Comparison', fontsize=11, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate([abs(delta_f_with[-1]), abs(delta_f_without[-1])]):
        axes[0, 1].text(i, v + 0.001, f'{v:.6f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Plot 3: Governor output comparison
    axes[1, 0].plot(t_with, p_g_with, 'b-', linewidth=2, label='With Integral Control')
    axes[1, 0].plot(t_without, p_g_without, 'r--', linewidth=2, label='Without Integral Control')
    axes[1, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[1, 0].set_xlabel('Time (s)', fontsize=10)
    axes[1, 0].set_ylabel('Governor Output (p.u.)', fontsize=10)
    axes[1, 0].set_title('Governor Response Comparison', fontsize=11, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend(fontsize=8)

    # Plot 4: Turbine output comparison
    axes[1, 1].plot(t_with, p_t_with, 'b-', linewidth=2, label='With Integral Control')
    axes[1, 1].plot(t_without, p_t_without, 'r--', linewidth=2, label='Without Integral Control')
    axes[1, 1].plot(t_with, np.ones_like(t_with) * delta_PL, 'k:', linewidth=2, label='Load Disturbance')
    axes[1, 1].set_xlabel('Time (s)', fontsize=10)
    axes[1, 1].set_ylabel('Turbine Output (p.u.)', fontsize=10)
    axes[1, 1].set_title('Turbine Response Comparison', fontsize=11, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('example_7_10_results.png', dpi=300, bbox_inches='tight')
    print("  Saved: example_7_10_results.png")
    plt.close()


def plot_solver_comparison():
    """Compare RK45 and Euler solvers"""
    print("Generating solver comparison plots...")

    # Use Example 7.9 parameters
    K_ps = 104.0
    t_ps = 22.0
    R = 3.0
    t_sg = 0.3
    t_t = 0.4
    ki = 0.1
    delta_PL = 0.48

    model = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)
    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    # Solve with RK45
    solver_rk45 = RK45Solver(model)
    t_rk45, x_rk45 = solver_rk45.solve(x0, (0, 50), 0.01)

    # Solve with Euler
    solver_euler = EulerSolver(model)
    t_euler, x_euler = solver_euler.solve(x0, (0, 50), 0.01)

    # Create comparison plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    fig.suptitle('ODE Solver Comparison (Example 7.9)', fontsize=14, fontweight='bold')

    ax.plot(t_rk45, x_rk45[:, 0], 'b-', linewidth=2, label='RK45 (4th order)')
    ax.plot(t_euler, x_euler[:, 0], 'r--', linewidth=2, label='Euler (1st order)')
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Frequency Deviation (Hz)', fontsize=11)
    ax.set_title('Frequency Deviation: RK45 vs Euler', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Add inset for close-up view
    axins = ax.inset_axes([0.5, 0.5, 0.47, 0.47])
    axins.plot(t_rk45, x_rk45[:, 0], 'b-', linewidth=2)
    axins.plot(t_euler, x_euler[:, 0], 'r--', linewidth=2)
    axins.set_xlim(0, 5)
    axins.set_ylim(-2, 0)
    axins.grid(True, alpha=0.3)
    axins.set_title('Close-up (0-5s)', fontsize=9)

    plt.tight_layout()
    plt.savefig('solver_comparison.png', dpi=300, bbox_inches='tight')
    print("  Saved: solver_comparison.png")
    plt.close()


def main():
    """Generate all plots"""
    print("="*60)
    print("Power System Simulator - Plot Generation")
    print("="*60)
    print()

    plot_example_7_9()
    plot_example_7_10()
    plot_solver_comparison()

    print()
    print("="*60)
    print("All plots generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  - example_7_9_results.png")
    print("  - example_7_10_results.png")
    print("  - solver_comparison.png")
    print("="*60)


if __name__ == "__main__":
    main()
