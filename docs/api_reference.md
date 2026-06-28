# API Reference

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
