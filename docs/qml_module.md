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
