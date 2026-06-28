# OS Layer

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

---

## API Reference: `qpu_os.py`

### Classes

#### `class QPUOS`
OS-layer controlling the full execution path:

    circuit OR precompiled gate-list
        → compile
        → schedule
        → waveform json
        → execute pulses

Works for:
- small circuits
- large SHA256-style algorithms (gate lists)
- job manager

**Methods:**

- **`__init__(self, gate_engine, scheduler, executor)`**: No documentation provided.
- **`run_circuit(self, circuit_str)`**: No documentation provided.
- **`run_gate_list(self, gate_list)`**: No documentation provided.


---

## API Reference: `quantum_gates.py`

### Classes

#### `class QuantumGateImplementation`
Converts logical gates into hardware-level pulse objects.
Used by both small circuits and big-algorithm compiler.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`gate_to_pulses(self, gate)`**: Convert a gate dict into 1 or more Pulse objects.
- **`compile_circuit(self, circuit_str)`**: Still used by old pipeline. Keeps compatibility.

