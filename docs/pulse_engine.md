# Pulse Engine

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
3. **DRAG (`drag_pulse`)**: Derivative Removal by Adiabatic Gate. Adds a derivative component to the out-of-phase quadrature to suppress transitions to the $|2\rangle$ state in weakly anharmonic transmons.
4. **Flat-top (`flat_top_pulse`)**: Used for longer operations, such as cross-resonance two-qubit gates or readout pulses.

## Compilation and Scheduling

### Gate to Pulse Conversion (`pulse_sequence.py`)
The `circuit_to_pulses()` function acts as the low-level compiler. It takes a dictionary representation of a logical gate (e.g., `{"gate": "X", "qubit": 0}`) and maps it to the corresponding calibrated `Pulse` object using the `GATE_LIBRARY`. For two-qubit gates like `CNOT`, it generates multiple concurrent pulses on both the control and target channels.

### Timing and Conflict Resolution (`scheduler.py`)
The `PulseScheduler` iterates through the list of generated pulses and assigns absolute start and end times. It tracks the occupancy of each channel, ensuring that overlapping pulses on the same qubit are serialized and respecting the system's clock resolution (typically 1ns).

## Waveform Synthesis

Finally, the `WaveformBuilder` (`waveform_builder.py`) takes the scheduled pulses and evaluates their `waveform` functions over the specified duration at a standard sampling rate (e.g., 2 GSa/s), producing the raw digital arrays that would be sent to the Arbitrary Waveform Generators (AWGs).
