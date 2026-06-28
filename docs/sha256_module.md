# SHA-256 Quantum Circuit

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

---

## API Reference: `run_sha256.py`

### Functions

#### `def main()`
No documentation provided.


---

## API Reference: `sha256_blocks.py`

### Classes

#### `class SHA256BlockBuilder`
No documentation provided.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`build_one_round(self, round_index)`**: SHA-256 has:
- **`build_sha256(self, rounds)`**: No documentation provided.


---

## API Reference: `sha256_compiler.py`

### Classes

#### `class SHA256Compiler`
No documentation provided.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`compile_sha_blocks(self, block_list)`**: No documentation provided.

