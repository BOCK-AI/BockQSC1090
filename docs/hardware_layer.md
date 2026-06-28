# Hardware Layer

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

---

## API Reference: `klayout_quantum_processor.py`

KLayout Processing Script (Updated for Modern Design Flow)
==========================================================

This version is compatible with:
- Modern Python
- gdspy-generated GDS files
- Optional KLayout installation (safe fallback)

It preserves the company’s expected behavior and outputs.

### Functions

#### `def load_gds_safely(filepath)`
Loads GDS using pya, if available.

#### `def run_drc_checks()`
Dummy DRC checks — same output as original pipeline.
Note: These are placeholders and do not perform actual geometric rule checking.

#### `def export_fabrication(layout, output_dir)`
Export final fabrication GDS and report.

#### `def main()`
No documentation provided.


---

## API Reference: `main_10qubit_design.py`

Modernized main_10qubit_design.py using gdspy + qiskit (simplified shapes).
Keeps original class/method names and outputs:
- 10qubit_processor_v1.gds
- pipeline_output/design_results.json
- pipeline_output/10qubit_processor_v1_metadata.json
- design_report.txt

### Classes

#### `class TenQubitProcessor`
10Q Processor replacement using gdspy (simplified shapes).

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`create_qubit_layout(self)`**: Create 10-qubit layout (2x5). Coordinates in mm.
- **`create_coupling_network(self)`**: Create nearest-neighbor couplers (store metadata only).
- **`create_readout_resonators(self)`**: Add readout positions (metadata).
- **`analyze_system(self)`**: Placeholder analysis: compute simple estimated parameters.
- **`export_design(self, filename)`**: Write GDS using gdstk and save JSON metadata — simplified shapes.
- **`generate_report(self)`**: No documentation provided.

### Functions

#### `def main()`
No documentation provided.

