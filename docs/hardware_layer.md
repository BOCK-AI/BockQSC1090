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
