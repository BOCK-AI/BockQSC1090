# Algorithm Blocks

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

---

## API Reference: `blocks.py`

### Classes

#### `class BlockLibrary`
General-purpose modular algorithm blocks.

**Methods:**

- **`single_qubit(self, q)`**: No documentation provided.
- **`rotation(self, q, theta)`**: No documentation provided.
- **`two_qubit(self, gate, a, b)`**: No documentation provided.


---

## API Reference: `block_composer.py`

### Classes

#### `class BlockComposer`
No documentation provided.

**Methods:**

- **`chain(self, blocks)`**: No documentation provided.
- **`repeat(self, block, times)`**: No documentation provided.


---

## API Reference: `circuit_builder.py`

### Classes

#### `class CircuitBuilder`
No documentation provided.

**Methods:**

- **`build(self, gate_list)`**: No documentation provided.

