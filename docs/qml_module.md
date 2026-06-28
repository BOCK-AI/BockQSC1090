# Quantum Machine Learning (QML)

The QML modules at the root of the project demonstrate the conceptual integration of classical data preprocessing, quantum feature encoding, and classical post-processing (clustering).

## `qml_demo.py`

This script serves as an early-stage prototype for a hybrid quantum-classical workflow. 
It processes a small 2D classical dataset by mapping continuous values to rotation angles for `RX` and `RY` quantum gates.

**Workflow:**
1. **Classical Data Prep**: Extracts 2D coordinate points.
2. **Quantum Encoding**: Maps $x_1$ and $x_2$ to $	heta_1$ and $	heta_2$ respectively, generating a theoretical circuit of `RX` and `RY` operations.
3. **Measurement Sampling**: *Note: This script currently generates synthetic/random bitstrings rather than performing actual statevector simulation of the rotation gates.* It outputs frequency statistics to simulate a shot-based measurement process.

## `qml_clustering_variations.py`

This script demonstrates classical post-processing of quantum measurement outcomes. It takes theoretical "feature vectors" (representing the output probability distributions of a quantum circuit) and applies a nearest-centroid clustering algorithm. 

It includes tests for robustness against noise by applying Gaussian perturbations (`variation_1`) and moving averages (`variation_2`) to the base features before clustering.

---

## API Reference: `qml_clustering_variations.py`

### Functions

#### `def cluster(features)`
No documentation provided.


---

## API Reference: `qml_demo.py`

QML Demo – Early-Stage Prototype

This script introduces a minimal hybrid quantum–classical workflow.
It performs:
1. Classical data preparation
2. Parameter-based quantum-style encoding
3. Fake 2-qubit measurement sampling
4. Probability extraction for each data point

Note:
This is an early placeholder version without real quantum simulation.

### Classes

#### `class QMLDemo`
No documentation provided.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`encode_data(self, point)`**: Maps a 2D classical data point to simple rotation-style parameters.
- **`sample_measurement(self)`**: Generates a random 2-qubit measurement outcome as a placeholder.
- **`measurement_statistics(self)`**: Collects frequency statistics for all 2-qubit outcomes.
- **`run(self)`**: Executes the early-stage QML pipeline:

