# Simulation and Verification

The project includes a robust suite of scripts designed to mimic the characterization and benchmarking procedures used on physical quantum hardware.

## `quantum_processor_simulation.py`

This script simulates the foundational physical properties of the 10-qubit processor. It outputs:
- **`circuit_parameters.json`**: Physical constants for each qubit, including transition frequencies, anharmonicity ($lpha$), Josephson energy ($E_j$), charging energy ($E_c$), and coherence times ($T_1$, $T_2^*$).
- **Gate Fidelities**: Generates estimated fidelities for single-qubit and two-qubit operations, outputting to `single_qubit_gates.json` and `two_qubit_gates.json`.
- **System Benchmarks**: Aggregates the data to calculate high-level metrics, such as a synthetic Quantum Volume (QV) of 64.

## `quantum_processor_verification.py`

This acts as a comprehensive acceptance testing suite. It runs 7 categories of simulated hardware checks:
1. **Hardware Connectivity**: Verifies control electronics and RF synchronization.
2. **Qubit Characterization**: Checks $T_1$ and $T_2$ times against acceptable thresholds.
3. **Gate Performance**: Verifies that X, Y, Z, H, and CNOT fidelities meet the >99% target.
4. **System Timing**: Checks pulse jitter and alignment.
5. **Crosstalk Suppression**: Verifies isolation between coupling channels.
6. **System Integration**: Assesses overall throughput and error-correction readiness.
7. **Performance Benchmarks**: Verifies Randomized Benchmarking (RB) decay rates and Quantum Volume.

The script produces detailed timestamped JSON reports (`verification_report_*.json`) and text summaries (`verification_summary_*.txt`).

> [!WARNING]
> **Synthetic Data Notice**: Both the simulation and verification scripts currently utilize NumPy's random number generators (`np.random`) to produce statistically realistic outputs that mimic actual hardware distributions. They do not currently perform quantum mechanical physics simulations (e.g., via Lindblad master equations).

---

## API Reference: `quantum_processor_simulation.py`

Quantum Processor Simulation (Modern Lightweight Version)
=========================================================
Replaces Qiskit-Metal + SciPy simulation with a pure-Numpy
approximate physics model that produces IDENTICAL-style outputs
to the original company simulation.

This version:
- Creates realistic qubit parameters
- Generates single-qubit and two-qubit fidelities
- Produces readout fidelity metrics
- Computes benchmark metrics (Quantum Volume, RB)
- Saves 6 JSON output files exactly like the original system

Fully pipeline-compatible.

### Functions

#### `def save_json(filename, data)`
No documentation provided.

#### `def generate_circuit_parameters()`
No documentation provided.

#### `def simulate_single_qubit_gates()`
No documentation provided.

#### `def simulate_two_qubit_gates()`
No documentation provided.

#### `def simulate_readout_performance()`
No documentation provided.

#### `def generate_system_benchmarks(single, two, readout)`
No documentation provided.


---

## API Reference: `quantum_processor_verification.py`

Quantum Processor Verification and Testing Suite
===============================================
This module provides comprehensive verification and testing capabilities for the
10-qubit quantum processor, including hardware validation, performance testing,
and system integration verification.

Author: QPU Development Team
Date: August 2025

### Classes

#### `class QuantumProcessorVerification`
Comprehensive verification and testing class

**Methods:**

- **`__init__(self)`**: Initialize verification suite
- **`convert_numpy_bool(self, obj)`**: Convert numpy bool types to native Python bool for JSON serialization
- **`run_full_verification_suite(self)`**: Execute complete verification test suite
- **`verify_hardware_connectivity(self)`**: Verify hardware connectivity and basic functionality
- **`verify_qubit_parameters(self)`**: Verify individual qubit parameters meet specifications
- **`verify_gate_performance(self)`**: Verify quantum gate performance meets specifications
- **`verify_system_timing(self)`**: Verify system timing and synchronization
- **`verify_crosstalk_suppression(self)`**: Verify crosstalk and interference suppression
- **`verify_system_integration(self)`**: Verify end-to-end system integration
- **`run_performance_benchmarks(self)`**: Run standard quantum computing benchmarks
- **`generate_verification_report(self, verification_duration)`**: Generate comprehensive verification report

### Functions

#### `def main()`
Main verification execution function

