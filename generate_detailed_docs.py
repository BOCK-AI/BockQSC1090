import os

docs_dir = "docs"
os.makedirs(docs_dir, exist_ok=True)

docs = {
    "index.md": """# BockQSC1090 Documentation

Welcome to the comprehensive documentation for the **BockQSC1090** project, a full-stack quantum system compiler designed for a 10-qubit superconducting processor.

This repository serves as a complete development package for designing, simulating, and executing quantum algorithms on a custom hardware specification. The project traverses the entire quantum computing stack—from the physical layout of the processor chip in GDSII format, up through pulse-level control, operating system resource management, job scheduling, and finally to high-level quantum algorithms and a custom Domain Specific Language (DSL).

## Core Capabilities

1. **Physical Chip Design**: Automated generation of 10-qubit transmon layouts with readout resonators and nearest-neighbor coupling buses using `gdstk`.
2. **Pulse-Level Control**: Translation of quantum logic gates into microwave pulse envelopes (Gaussian, DRAG, Flat-top) and time-domain waveform synthesis.
3. **Execution Pipeline**: An OS layer that schedules and coordinates the execution of quantum circuits, complete with simulated measurement sampling.
4. **Job Management**: A queue-based job manager that allows for asynchronous submission and status tracking of quantum tasks.
5. **Algorithm Library**: Pre-built components for foundational quantum algorithms (Grover's, QFT, Simon's, Phase Estimation, etc.).
6. **Big Algorithm Engine**: A compiler and scheduler for executing complex `.algo` programs composed of thousands of gates.
7. **Interactive Dashboard**: A Streamlit-based web interface for real-time monitoring of qubit metrics, calibration data, and interactive algorithm execution.

## Table of Contents

### System Overview
- [Architecture](architecture.md)
- [Getting Started](getting_started.md)

### The Quantum Stack
- [Hardware Layer](hardware_layer.md)
- [Pulse Engine](pulse_engine.md)
- [OS Layer](os_layer.md)
- [Job Layer](job_layer.md)

### Algorithms and Applications
- [Algorithm Blocks](algorithm_blocks.md)
- [Big Algorithm Engine](big_algo_engine.md)
- [Quantum Machine Learning](qml_module.md)
- [SHA-256 Quantum Circuit](sha256_module.md)

### Tools and Diagnostics
- [Simulation & Verification](simulation_verification.md)
- [Dashboard](dashboard.md)
- [Configuration](configuration.md)
- [API Reference](api_reference.md)

### Project Meta
- [Changelog](changelog.md)
- [Project Handoff](project_handoff.md)
""",
    "architecture.md": """# Architecture

The BockQSC1090 project is structured as a classical-quantum software stack, abstracting the complexities of quantum hardware into manageable, modular layers. The architecture follows a strict top-down execution flow, allowing high-level algorithms to be seamlessly compiled down to physical microwave pulses.

## Layer Diagram

```mermaid
graph TD
    subgraph Application Layer
        D[Dashboard]
        QML[QML Module]
        SHA[SHA-256 Benchmark]
    end

    subgraph Algorithm Layer
        BAE[Big Algo Engine]
        AB[Algorithm Blocks]
    end

    subgraph Execution Layer
        J[Job Layer]
        O[OS Layer]
    end

    subgraph Hardware Abstraction
        P[Pulse Engine]
        S[Simulation & Verification]
    end

    subgraph Physical Design
        H[Hardware Layer]
    end

    D --> BAE
    QML --> BAE
    SHA --> BAE
    
    BAE --> J
    AB --> BAE
    
    J --> O
    O --> P
    
    P --> H
    S --> H
```

## Layer Descriptions

### 1. Application Layer
The top-most layer provides user-facing interfaces and benchmark suites. The **Dashboard** offers a GUI for interactive testing, while the **QML** and **SHA-256** modules serve as complex, multi-round stress tests for the compiler and execution pipeline.

### 2. Algorithm Layer
The **Big Algorithm Engine** processes custom `.algo` files, acting as the primary DSL parser. It flattens hierarchical operations and validates them against the hardware's supported gate set. The **Algorithm Blocks** library provides modular, reusable quantum subroutines (e.g., QFT, Grover diffusers) that can be chained together.

### 3. Execution Layer
The **Job Layer** manages a queue of pending quantum circuits, abstracting the QPU as a remote resource. The **OS Layer** coordinates the actual lifecycle of a circuit: it receives a job, triggers compilation, requests pulse scheduling, and invokes the execution engine.

### 4. Hardware Abstraction (Pulse Engine)
The **Pulse Engine** bridges the gap between discrete logic gates and continuous physical signals. It maps logical operations to specific microwave envelopes (Gaussian, DRAG) defined in calibration files, schedules them to avoid crosstalk and channel overlap, and synthesizes the final time-domain waveforms.

### 5. Physical Design (Hardware Layer)
The **Hardware Layer** defines the physical topology of the 10-qubit processor. It exports standard GDSII files for fabrication and generates the baseline physical parameters (capacitances, inductances, anharmonicities) used by the downstream simulation layers.
""",
    "getting_started.md": """# Getting Started

This guide will help you install the BockQSC1090 package and run your first quantum pipeline.

## Prerequisites

- **Python**: Version 3.10 or higher is required.
- **Git**: For cloning the repository.
- **Virtual Environment** (Recommended): We strongly recommend using `venv` or `conda` to isolate the project dependencies.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BOCK-AI/BockQSC1090.git
   cd BockQSC1090
   ```

2. **Install the package in editable mode**:
   This will install all required dependencies (such as `numpy`, `streamlit`, `gdstk`, and `matplotlib`).
   ```bash
   pip install -e .
   ```

3. **Initialize the workspace**:
   The project requires several output directories to store generated GDS files, JSON reports, and logs. Run the setup script to create these:
   ```bash
   python scripts/setup_env.py
   ```
   *Expected Output:*
   ```text
   Setting up BockQSC1090 environment...
   Ensured directory exists: output/
   Ensured directory exists: fabrication_output/
   ...
   Environment setup complete.
   ```

## Running the End-to-End Pipeline

To verify that the installation was successful and to generate the baseline datasets required by the dashboard, run the main pipeline script. This script executes the hardware design, simulation, gate generation, and verification suites in sequence.

```bash
python run_pipeline.py
```

*Expected Output:*
The script will output progress logs as it moves through the stages. Upon completion, it will list the generated files, including `10qubit_processor_v1.gds`, `circuit_parameters.json`, and the verification summaries.

## Launching the Dashboard

Once the pipeline has generated the necessary data, you can explore the results interactively via the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

This will open a local web server (typically at `http://localhost:8501`) where you can:
- View the 10-qubit processor design metadata and qubit frequencies.
- Analyze simulated gate fidelities and randomized benchmarking results.
- Write and execute custom `.algo` quantum programs in the browser.
""",
    "hardware_layer.md": """# Hardware Layer

The Hardware Layer is responsible for the physical definition and layout generation of the 10-qubit superconducting processor. The primary script for this layer is `main_10qubit_design.py`.

## Processor Topology

The processor features 10 transmon qubits arranged in a 2x5 rectangular grid. This topology was chosen to balance connectivity with manageable crosstalk. 

- **Qubits**: 10 transmons (Q0 through Q9).
- **Couplers**: 13 nearest-neighbor capacitive coupling buses.
- **Readout**: 10 dedicated $\lambda/4$ coplanar waveguide (CPW) resonators, one for each qubit.

### Qubit Addressing
```text
Q0 -- Q1 -- Q2 -- Q3 -- Q4
|     |     |     |     |
Q5 -- Q6 -- Q7 -- Q8 -- Q9
```

## GDSII Layout Generation (`gdstk`)

The `TenQubitProcessor` class procedurally generates a simplified representation of the processor layout and exports it to a standard GDSII file (`10qubit_processor_v1.gds`) using the `gdstk` library.

The layout comprises three main layers:
- **Layer 1 (Qubits)**: Defines the rectangular transmon capacitor pads.
- **Layer 2 (Couplers)**: Defines the `FlexPath` structures connecting nearest-neighbor qubits.
- **Layer 3 (Resonators)**: Defines the geometric bounds of the readout resonators.

## Physical Parameter Estimation

Before export, the script performs a preliminary system analysis (`analyze_system()`). This calculates the Euclidean distance between coupled qubits and provides a rough estimate of the coupling strength (in MHz). These estimates, along with the coordinate data, are exported to `pipeline_output/design_results.json` for consumption by the simulation layer.

## Fabrication Output

The `klayout_quantum_processor.py` script acts as a bridge for foundry preparation. While currently utilizing placeholder Design Rule Checks (DRC), it serves to wrap the generated GDS file with standard foundry reporting metadata, outputting the final artifacts to the `fabrication_output/` directory.
""",
    "pulse_engine.md": """# Pulse Engine

The Pulse Engine (`pulse_engine/`) is the translation layer that bridges discrete quantum logic gates and the continuous microwave control signals required to manipulate superconducting qubits.

## Pulse Representation

At the core of the engine is the `Pulse` dataclass (`pulse.py`). A pulse is defined by:
- `duration`: The length of the pulse in seconds.
- `amplitude`: The normalized drive amplitude (0.0 to 1.0).
- `phase`: The phase offset in radians.
- `channel`: The target hardware control line (e.g., `d0` for the drive line of Qubit 0).
- `waveform`: A callable function that generates the actual time-domain envelope array.

## Pulse Shapes (`pulse_shapes.py`)

The engine supports several standard envelope shapes for qubit control:
1. **Constant Wave (`constant_wave`)**: A flat rectangular pulse, primarily used for simple measurement tones or Z-rotations via flux bias.
2. **Gaussian (`gaussian_pulse`)**: The standard envelope for single-qubit XY rotations, minimizing spectral leakage.
3. **DRAG (`drag_pulse`)**: Derivative Removal by Adiabatic Gate. Adds a derivative component to the out-of-phase quadrature to suppress transitions to the $|2\\rangle$ state in weakly anharmonic transmons.
4. **Flat-top (`flat_top_pulse`)**: Used for longer operations, such as cross-resonance two-qubit gates or readout pulses.

## Compilation and Scheduling

### Gate to Pulse Conversion (`pulse_sequence.py`)
The `circuit_to_pulses()` function acts as the low-level compiler. It takes a dictionary representation of a logical gate (e.g., `{"gate": "X", "qubit": 0}`) and maps it to the corresponding calibrated `Pulse` object using the `GATE_LIBRARY`. For two-qubit gates like `CNOT`, it generates multiple concurrent pulses on both the control and target channels.

### Timing and Conflict Resolution (`scheduler.py`)
The `PulseScheduler` iterates through the list of generated pulses and assigns absolute start and end times. It tracks the occupancy of each channel, ensuring that overlapping pulses on the same qubit are serialized and respecting the system's clock resolution (typically 1ns).

## Waveform Synthesis

Finally, the `WaveformBuilder` (`waveform_builder.py`) takes the scheduled pulses and evaluates their `waveform` functions over the specified duration at a standard sampling rate (e.g., 2 GSa/s), producing the raw digital arrays that would be sent to the Arbitrary Waveform Generators (AWGs).
""",
    "os_layer.md": """# OS Layer

The OS Layer (`qpu_os.py`) acts as the central nervous system of the BockQSC1090 framework. It orchestrates the entire lifecycle of a quantum program, abstracting the complexities of compilation and pulse generation away from the user.

## The `QPUOS` Class

The `QPUOS` class relies on dependency injection, accepting instances of three critical subsystems upon initialization:
1. **Gate Engine**: Handles the parsing of string-based circuits and higher-level logical compilation.
2. **Scheduler**: Handles the time-domain scheduling of physical pulses.
3. **Executor**: Simulates the execution of the final waveform and produces measurement results.

## Execution Pipeline

When a circuit is submitted to the OS via `run_circuit()`, it undergoes the following automated pipeline:

1. **Logical Compilation**: The input circuit string (e.g., `"H(0); CNOT(0,1)"`) is parsed into an intermediate representation—a list of gate dictionaries.
2. **Pulse Translation**: The gate dictionaries are converted into hardware-level `Pulse` objects.
3. **Scheduling**: The pulses are assigned precise start and end times, resolving any channel conflicts.
4. **Waveform Export**: The scheduled pulses are serialized and saved to `compiled_waveforms.json`. This mimics the process of loading instructions into AWG memory.
5. **Execution**: The `Executor` is invoked to "run" the waveforms, ultimately returning a classical bitstring representing the measurement outcome.

## Extensibility

The OS layer is designed to be highly modular. By swapping out the injected `executor` (which currently uses a mock software simulator), the exact same OS layer can interface directly with physical dilution refrigerator control electronics without changing the upper-level algorithm code.
""",
    "job_layer.md": """# Job Layer

The Job Layer (`job_layer/`) provides a robust queuing system for managing quantum workloads. Because quantum processors are scarce, single-threaded resources, circuits cannot be executed simultaneously; they must be queued, prioritized, and executed sequentially.

## Components

### `Job` Object (`job.py`)
Every submitted circuit is wrapped in a `Job` dataclass. A job possesses:
- A unique UUID (`id`).
- The source `circuit` string.
- A `status` tracking its lifecycle (`CREATED`, `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`).
- Timestamps for submission and completion.
- The final execution `result`.

### `JobQueue` and `JobStore`
- **`JobQueue`**: A FIFO queue (using `collections.deque`) that holds jobs awaiting execution.
- **`JobStore`**: An in-memory dictionary that stores the canonical state of all jobs, allowing for fast retrieval by UUID.

### `JobManager` (`job_manager.py`)
The `JobManager` is the primary interface for this layer. It accepts incoming circuit strings, wraps them in `Job` objects, and places them in the queue. 

**Key Methods:**
- `submit_job(circuit_str)`: Creates and queues a new job, returning the UUID.
- `run_next()`: Pops the oldest job from the queue, passes it to the `QPUOS` for execution, updates the job's status to `COMPLETED`, and stores the result.
- `get_status(job_id)`: Retrieves the current status and results of a specific job.

## Usage Example

```python
from qpu_os import QPUOS
from job_layer.job_manager import JobManager

# Initialize dependencies...
os_layer = QPUOS(gate_engine, scheduler, executor)
manager = JobManager(os_layer)

# Asynchronous submission
job_id = manager.submit_job("H(0); X(1)")

# Process queue
finished_id, result = manager.run_next()
print(f"Job {finished_id} finished with result: {result}")
```
""",
    "algorithm_blocks.md": """# Algorithm Blocks

The `algorithm_blocks/` directory serves as a standard library of fundamental quantum routines. Instead of writing monolithic circuits from scratch, users can compose complex applications using these verified, reusable blocks.

## Design Philosophy

The Algorithm Blocks are implemented in pure Python using NumPy arrays for statevector simulation. They demonstrate the mathematical underpinnings of quantum advantage without requiring compilation down to the pulse level.

## Available Blocks

1. **Grover's Algorithm** (`grover.py`): Implements amplitude amplification to search an unstructured database with quadratic speedup. Includes customizable oracles and the standard Grover diffusion operator.
2. **Quantum Fourier Transform** (`qft.py`): Implements the QFT, the cornerstone of phase estimation and Shor's algorithm, transitioning computational basis states into the Fourier basis.
3. **Bernstein-Vazirani** (`bernstein_vazirani.py`): Determines a hidden binary string in a single query, demonstrating quantum parallelism.
4. **Deutsch-Jozsa** (`deutsch_jozsa.py`): Determines whether a hidden boolean function is constant or balanced in a single query.
5. **Simon's Algorithm** (`simon.py`): Finds the hidden period of a function that is guaranteed to be 2-to-1.
6. **Quantum Phase Estimation** (`phase_estimation.py`): Estimates the eigenvalue phase of a given unitary operator, a critical subroutine for quantum chemistry and factorization.

*(Note: Earlier documentation erroneously mentioned Variational Quantum Eigensolver (VQE) and Quantum Approximate Optimization Algorithm (QAOA) blocks using PennyLane. These were exploratory concepts that are not currently implemented in the standard blocks library.)*

## Integration with the Pipeline

Currently, the `algorithm_blocks/` are standalone mathematical demonstrations. The `block_composer.py` and `blocks.py` files contain experimental string-based gate representations intended to bridge these mathematical concepts to the `Big Algorithm Engine`, though this integration remains a work in progress.
""",
    "big_algo_engine.md": """# Big Algorithm Engine

The Big Algorithm Engine (`big_algo_engine/`) is designed to handle the orchestration, parsing, and compilation of large-scale quantum programs that exceed the complexity of simple string-based circuit definitions.

## The `.algo` Domain Specific Language

To support complex programs, BockQSC1090 introduces the `.algo` file format—a simple, line-by-line DSL for defining quantum operations. 

**Syntax Example (`test.algo`):**
```text
# Initialize Superposition
H 0
H 1

# Apply Entanglement
CNOT 0 1

# Measurement
MEASURE
```

## Engine Components

1. **`AlgoParser` (`parser.py`)**: 
   Reads `.algo` files, strips comments, and converts the text instructions into an intermediate list of Python tuples (e.g., `("H", [0])`). It includes bounds checking to ensure target qubits exist on the 10-qubit hardware.

2. **`AlgoCompiler` (`compiler.py`)**: 
   Takes the parsed intermediate representation and compiles it into the standard gate dictionary format required by the OS Layer (e.g., `{"gate": "H", "qubit": 0, "duration_ns": 20}`).

3. **`AlgoScheduler` (`scheduler.py`)**: 
   Provides a greedy scheduling algorithm that attempts to pack non-overlapping gates into parallel execution time slots to minimize total circuit depth.

4. **`BigAlgoEngine` (`engine.py`)**: 
   The main orchestrator class. It exposes a `run_algorithm(filepath)` method that chains the Parser, Compiler, and the QPU OS layer together into a single seamless function call.

## Standalone Execution

You can bypass the OS layer and run `.algo` files directly using the standalone NumPy statevector simulator:

```bash
python run_custom_algorithm.py --file test.algo
```
This will output a step-by-step trace of the gate applications and the final simulated measurement bitstring.
""",
    "qml_module.md": """# Quantum Machine Learning (QML)

The QML modules at the root of the project demonstrate the conceptual integration of classical data preprocessing, quantum feature encoding, and classical post-processing (clustering).

## `qml_demo.py`

This script serves as an early-stage prototype for a hybrid quantum-classical workflow. 
It processes a small 2D classical dataset by mapping continuous values to rotation angles for `RX` and `RY` quantum gates.

**Workflow:**
1. **Classical Data Prep**: Extracts 2D coordinate points.
2. **Quantum Encoding**: Maps $x_1$ and $x_2$ to $\theta_1$ and $\theta_2$ respectively, generating a theoretical circuit of `RX` and `RY` operations.
3. **Measurement Sampling**: *Note: This script currently generates synthetic/random bitstrings rather than performing actual statevector simulation of the rotation gates.* It outputs frequency statistics to simulate a shot-based measurement process.

## `qml_clustering_variations.py`

This script demonstrates classical post-processing of quantum measurement outcomes. It takes theoretical "feature vectors" (representing the output probability distributions of a quantum circuit) and applies a nearest-centroid clustering algorithm. 

It includes tests for robustness against noise by applying Gaussian perturbations (`variation_1`) and moving averages (`variation_2`) to the base features before clustering.
""",
    "sha256_module.md": """# SHA-256 Quantum Circuit

The `sha256/` directory contains a highly experimental quantum-inspired implementation of SHA-256 compression functions. 

## Purpose

This module is **not** designed to provide a quantum advantage for cryptographic hashing, nor does it implement a full Grover-based preimage attack. Instead, it serves as a **structural stress test** for the BockQSC1090 compiler, scheduler, and OS layer.

By attempting to map complex classical bitwise operations (like `Ch`, `Maj`, and $\Sigma$) into sequences of quantum gates (H, X, CNOT), it generates massive, deeply-nested circuits.

## Implementation Details (`sha256_circuit.py`)

The script defines classical NumPy implementations of quantum-analogous operations:
- **`ch_function()`**: The "Choice" function.
- **`maj_function()`**: The "Majority" function.
- **`sigma0()` / `sigma1()`**: Rotational shifts.
- **`sha256_round()`**: A single round of compression.

## The Stress Test (`run_sha256.py`)

The `run_sha256.py` script utilizes the `SHA256BlockBuilder` to generate 64 identical algorithmic rounds. It flattens these rounds into a single massive gate list and pushes it through the `QPUOS` pipeline. This tests the system's ability to handle memory management, deep scheduling, and large waveform JSON serialization without crashing.
""",
    "simulation_verification.md": """# Simulation and Verification

The project includes a robust suite of scripts designed to mimic the characterization and benchmarking procedures used on physical quantum hardware.

## `quantum_processor_simulation.py`

This script simulates the foundational physical properties of the 10-qubit processor. It outputs:
- **`circuit_parameters.json`**: Physical constants for each qubit, including transition frequencies, anharmonicity ($\alpha$), Josephson energy ($E_j$), charging energy ($E_c$), and coherence times ($T_1$, $T_2^*$).
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
""",
    "dashboard.md": """# Dashboard

The BockQSC1090 framework includes a fully-featured, browser-based graphical interface built using **Streamlit**. It provides visualization of the processor's architecture, calibration data, and interactive execution capabilities.

## Launching the Dashboard

From the root directory of the project, ensure you have generated the baseline data by running `python run_pipeline.py`, then start the server:

```bash
streamlit run dashboard.py
```
Navigate to `http://localhost:8501` in your web browser.

## Dashboard Tabs

### 1. 📐 Design
Reads the `design_results.json` and `10qubit_processor_v1_metadata.json` files generated by the hardware layer. It displays the physical coordinates of the qubits and plots an interactive bar chart of the simulated qubit frequencies.

### 2. 🧪 Simulations
Displays the raw outputs of the `quantum_processor_simulation.py` script. Includes a line graph mapping the frequency distribution across the 10-qubit processor.

### 3. ⚡ Gate Operations
Visualizes calibration data and Randomized Benchmarking (RB) results. Includes a scatter plot of RB survival probabilities exponentially decaying against circuit depth, and a bar chart detailing the exact nanosecond durations of the scheduled gate timeline.

### 4. 🛠 Verification
Provides a quick-reference view of the latest automated verification reports, highlighting which subsystems passed or failed their quality control checks.

### 5. 🧮 Run Custom Algorithm
An interactive IDE built into the browser. You can type or paste custom `.algo` DSL scripts directly into a text area. Clicking "Run Algorithm" executes the script using the pure NumPy statevector simulator in the backend, printing the operation log and the final collapsed bitstring result directly to the UI.
""",
    "api_reference.md": """# API Reference

BockQSC1090 relies on clean, class-based encapsulation. Below are the primary interfaces for interacting with the core components programmatically.

## `qpu_os.QPUOS`
The main orchestrator.
- **`__init__(gate_engine, scheduler, executor)`**: Injects the required subsystems.
- **`run_circuit(circuit_str)`**: Compiles, schedules, and executes a string-based circuit. Returns the measurement result.
- **`run_gate_list(gate_list)`**: Bypasses the string compiler and directly schedules/executes a list of gate dictionaries.

## `job_layer.job_manager.JobManager`
Queue management.
- **`__init__(os_layer)`**: Initializes with a QPUOS instance.
- **`submit_job(circuit_str)`**: Queues a job and returns its UUID.
- **`run_next()`**: Executes the oldest queued job. Returns a tuple: `(job_id, result)`.
- **`get_status(job_id)`**: Returns the status string (e.g., `'COMPLETED'`).

## `pulse_engine.pulse.Pulse`
The physical pulse dataclass.
- **Attributes**: `name` (str), `duration` (float seconds), `amplitude` (float 0-1), `phase` (float radians), `waveform` (callable), `channel` (str).

## `big_algo_engine.engine.BigAlgoEngine`
High-level `.algo` execution.
- **`__init__(os_layer)`**: Initializes the engine.
- **`run_algorithm(filepath)`**: Parses the `.algo` file at the given path, compiles it, and executes it via the OS layer.

*For complete implementation details, parameters, and return types, please refer to the standard Python docstrings located within the source code files.*
""",
    "configuration.md": """# Configuration

The `config/` directory manages system-wide variables and physical parameters. While some of these files are currently placeholder architectures intended for future expansion, they define the expected data structures for hardware integration.

## 1. `qubit_params.json`
Defines the baseline physical realities of the 10 transmons.
- **`frequency_ghz`**: The 0-1 transition frequency (typically 4.5 - 5.5 GHz).
- **`anharmonicity_mhz`**: The energy difference between the 1-2 and 0-1 transitions (typically ~ -220 MHz).
- **`T1_us`**: Relaxation time in microseconds.
- **`T2_us`**: Dephasing time in microseconds.
- **`coupling_strength_mhz`**: Capacitive coupling strength to nearest neighbors.

## 2. `system_config.json`
Defines operational parameters for the execution pipeline.
- **`backend`**: Identifies whether to use `"simulator"` or physical hardware.
- **`optimization_level`**: Targets for circuit depth reduction (e.g., 0-3).
- **`error_mitigation`**: Boolean flag for applying readout or gate mitigation strategies.
- **`shots`**: The number of statistical runs per circuit execution.

## 3. `calibration_schedule.json`
Outlines maintenance tasks required for physical hardware.
Defines routines such as `qubit_frequency_cal` and `T1_measurement`, specifying the required `interval_hours` between runs and tracking the `last_run` timestamp.

## 4. `config_loader.py`
A Python utility class (`ConfigLoader`) that provides a simple key-based interface for securely parsing and loading the JSON configuration files into Python dictionaries.
""",
    "changelog.md": """# Changelog

All notable changes to the BockQSC1090 project are documented here.

## [v1.0.0] - Handoff Release (June 2026)

### Added
- Comprehensive `docs/` directory detailing the entire software stack.
- Modern `setuptools` based `setup.py` and dedicated `scripts/setup_env.py`.

### Changed
- **Dependency Overhaul**: Removed deprecated `qiskit-metal` and unused dependencies (pandas, seaborn, plotly). Pinned modern versions of `numpy`, `matplotlib`, and `streamlit`.
- **Hardware Layer Migration**: Transitioned `main_10qubit_design.py` from the end-of-life `gdspy` library to the modern `gdstk` library, updating all geometric rendering APIs.
- **Pipeline Execution**: Replaced unsafe `os.system()` calls with `subprocess.run()` in `run_pipeline.py`.

### Fixed
- **CRITICAL**: Fixed a mathematical bug in `dashboard.py` where the `Z_GATE` was defined as the Identity matrix `[[1,0],[0,1]]` instead of `[[1,0],[0,-1]]`.
- **CRITICAL**: Fixed a `KeyError` crash in `pulse_engine/pulse_sequence.py` by properly parsing `control` and `target` keys for `CNOT` gates.
- Fixed a string formatting bug in `run_custom_algorithm.py` that caused measurement bitstrings to render incorrectly. Added missing qubit bounds checking (0-9).
- Repaired bare `except:` clauses causing silent failures in the dashboard data loaders.

---

## [Pre-v1.0.0] - Historic Milestones

### March 2026
- Integrated OS layer, Job system, and Big Algorithm pipeline into a cohesive flow.
- Added the SHA-256 quantum-inspired benchmark module.

### February 2026
- Initial implementation of the OS layer and Job layer (queue management).
- Created the Algorithm Blocks library and the Big Algorithm Engine for `.algo` parsing.
- Added exploratory Quantum Machine Learning (QML) scripts.

### December 2025
- Replaced initial software stubs with real implementations.
- Developed the Streamlit dashboard and custom algorithm execution engine.
- Integrated pulse execution and measurement translation.

### August 2025
- Initial upload of the repository.
- Created the 10-qubit GDS design generator and the verification/benchmarking framework.
""",
    "project_handoff.md": """# Project Handoff Notes

This document contains critical operational notes and highlights known limitations for the development team taking ownership of the BockQSC1090 repository.

## System Status
The repository has been successfully modernized, documented, and vetted. It is in a **stable, handoff-ready state**. The installation scripts work, the execution pipeline runs without crashing, and the Streamlit dashboard renders successfully.

## Known Limitations & Technical Debt

Please be aware of the following architectural shortcuts and placeholders that remain in the codebase:

1. **Synthetic Simulation Data**
   - **Issue**: The `quantum_processor_simulation.py` and `quantum_processor_verification.py` scripts do not utilize Lindblad master equations or actual Hamiltonian evolution. They use `numpy.random` to generate physically plausible, but entirely synthetic, benchmarking data (e.g., T1 times, gate fidelities).
   - **Next Steps**: Integrate a real quantum dynamics simulator (such as QuTiP) to model the true behavior based on the `circuit_parameters.json`.

2. **Placeholder DRC Checks**
   - **Issue**: The `klayout_quantum_processor.py` script attempts to bridge to KLayout for Design Rule Checking. However, the current DRC checks simply print "Passed" to the console without performing actual geometric verification on the GDS file.
   - **Next Steps**: Implement actual `pya` geometry routines to verify junction sizes and line spacing.

3. **QML Module Abstraction**
   - **Issue**: The `qml_demo.py` script translates classical data into theoretical rotation angles, but it bypasses the statevector simulator entirely and emits purely random measurement bitstrings. 
   - **Next Steps**: Connect the QML demo to the `QPUOS` or `run_custom_algorithm` statevector backend to accurately simulate the parameterized circuits.

4. **Algorithm Blocks String Format**
   - **Issue**: The `algorithm_blocks/blocks.py` library returns string-based representations of gates (e.g., `"H(0)"`), whereas the rest of the execution pipeline (OS Layer, Pulse Engine) expects Python dictionaries (e.g., `{"gate": "H", "qubit": 0}`).
   - **Next Steps**: Refactor the block composer to emit dictionaries natively, allowing the foundational algorithms (Grover, QFT) to be routed directly into the `BigAlgoCompiler`.

## Final Remarks
The modernization effort completed in v1.0.0 resolved all critical runtime crashes and dependency deprecations (specifically the removal of `gdspy` and `qiskit-metal`). The architecture is sound, and the pipeline is highly modular, making it well-prepared for the transition from software simulation to physical AWG hardware control.
"""
}

for filename, content in docs.items():
    with open(os.path.join(docs_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print("Highly detailed documentation successfully generated.")
