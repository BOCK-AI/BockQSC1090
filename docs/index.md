# BockQSC1090 Documentation

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
