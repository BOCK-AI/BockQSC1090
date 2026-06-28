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
