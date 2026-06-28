# Big Algorithm Engine

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

---

## API Reference: `algorithm_runner.py`

### Classes

#### `class AlgorithmRunner`
No documentation provided.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`parse_text(self, text)`**: No documentation provided.


---

## API Reference: `big_algo_compiler.py`

### Classes

#### `class BigAlgoCompiler`
No documentation provided.

**Methods:**

- **`compile_blocks(self, blocks)`**: Flatten block list into a single gate list.


---

## API Reference: `block_builder.py`

### Classes

#### `class BigAlgoBlockBuilder`
No documentation provided.

**Methods:**

- **`build_single_block(self)`**: Returns one block of 4 gates.
- **`chain_blocks(self, num_blocks)`**: No documentation provided.


---

## API Reference: `gate_validator.py`

### Classes

#### `class GateValidator`
Simple rule-based validator for big algorithm gate lists.
Ensures:
  - allowed gates only
  - qubit indices are valid (0–9 by default)
  - duration exists

**Methods:**

- **`__init__(self, max_qubits, allowed_gates)`**: No documentation provided.
- **`validate(self, gate_list)`**: No documentation provided.


---

## API Reference: `run_big_algorithm.py`

### Functions

#### `def main()`
No documentation provided.

