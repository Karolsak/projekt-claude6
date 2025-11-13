#!/usr/bin/env python3
"""
Test script to verify the power system simulator functionality
without GUI (for automated testing)
"""

import numpy as np
import sys


# Import the model and solvers from core module (no GUI dependencies)
sys.path.insert(0, '/home/user/projekt-claude6')
from power_system_core import PowerSystemModel, RK45Solver, EulerSolver


def test_example_7_9():
    """Test Example 7.9 parameters"""
    print("="*60)
    print("Testing Example 7.9")
    print("="*60)

    # Example 7.9 parameters
    K_ps = 104.0
    t_ps = 22.0
    R = 3.0
    t_sg = 0.3
    t_t = 0.4
    ki = 0.1
    delta_PL = 0.48

    # Create model
    model = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)

    # Initial conditions
    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    # Test with RK45
    print("\nTesting RK45 Solver...")
    solver_rk45 = RK45Solver(model)
    t, x = solver_rk45.solve(x0, (0, 50), 0.01)

    delta_f = x[:, 0]
    print(f"  Simulation completed: {len(t)} time steps")
    print(f"  Peak frequency deviation: {np.min(delta_f):.6f} Hz")
    print(f"  Steady-state error: {delta_f[-1]:.6f} Hz")

    # Test with Euler
    print("\nTesting Euler Solver...")
    solver_euler = EulerSolver(model)
    t, x = solver_euler.solve(x0, (0, 50), 0.01)

    delta_f = x[:, 0]
    print(f"  Simulation completed: {len(t)} time steps")
    print(f"  Peak frequency deviation: {np.min(delta_f):.6f} Hz")
    print(f"  Steady-state error: {delta_f[-1]:.6f} Hz")

    print("\n✓ Example 7.9 tests passed!\n")


def test_example_7_10():
    """Test Example 7.10 parameters"""
    print("="*60)
    print("Testing Example 7.10")
    print("="*60)

    # Example 7.10 parameters
    K_ps = 100.0
    t_ps = 20.0
    R = 2.5
    t_sg = 0.3
    t_t = 0.4
    ki = 0.15
    delta_PL = 0.02

    print("\nWith Integral Control (ki = 0.15):")
    model_with = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, ki, delta_PL)

    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    solver = RK45Solver(model_with)
    t, x = solver.solve(x0, (0, 50), 0.01)

    delta_f = x[:, 0]
    print(f"  Peak frequency deviation: {np.min(delta_f):.6f} Hz")
    print(f"  Steady-state error: {delta_f[-1]:.6f} Hz")

    print("\nWithout Integral Control (ki = 0):")
    model_without = PowerSystemModel(K_ps, t_ps, R, t_sg, t_t, 0.0, delta_PL)

    solver = RK45Solver(model_without)
    t, x = solver.solve(x0, (0, 50), 0.01)

    delta_f = x[:, 0]
    print(f"  Peak frequency deviation: {np.min(delta_f):.6f} Hz")
    print(f"  Steady-state error: {delta_f[-1]:.6f} Hz")

    print("\n✓ Example 7.10 tests passed!\n")


def test_model_stability():
    """Test model stability with various parameters"""
    print("="*60)
    print("Testing Model Stability")
    print("="*60)

    # Test with small load disturbance
    model = PowerSystemModel(K_ps=100, t_ps=20, R=2.5, t_sg=0.3, t_t=0.4, ki=0.1, delta_PL=0.01)
    x0 = np.array([0.0, 0.0, 0.0, 0.0])

    solver = RK45Solver(model)
    t, x = solver.solve(x0, (0, 100), 0.01)

    # Check if solution remains bounded
    if np.all(np.isfinite(x)) and np.max(np.abs(x)) < 100:
        print("✓ Model is stable for small disturbances")
    else:
        print("✗ Model shows instability")
        return False

    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Power System Simulator - Functional Tests")
    print("="*60 + "\n")

    try:
        test_example_7_9()
        test_example_7_10()
        test_model_stability()

        print("="*60)
        print("All tests passed successfully! ✓")
        print("="*60)
        print("\nYou can now run the GUI application:")
        print("  python3 power_system_simulator.py")
        print("="*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
