# ==========================================================
# 10-Qubit Processor Design — STUB VERSION (No Qiskit Metal)
# ==========================================================

import numpy as np
import json

print("🟦 Starting 10-Qubit Processor Design (STUB MODE)")
print("   Qiskit Metal not available — generating fake design data...\n")

# -------------------------------
# Generate FAKE qubit frequencies
# -------------------------------
# Around 5 GHz with slight randomness
qubit_freqs = 5 + np.random.randn(10) * 0.05    # ~5 ± 0.05 GHz

# -------------------------------
# Generate FAKE coupling strengths
# -------------------------------
# 9 couplings for a linear chain queue (like Q0–Q1, Q1–Q2, ...)
coupling_strengths = np.abs(np.random.randn(9)) * 0.01   # ~0.01 GHz

# -------------------------------
# Generate FAKE readout resonator frequencies
# -------------------------------
readout_freqs = 6 + np.random.randn(10) * 0.05  # ~6 ± 0.05 GHz

# -------------------------------
# Generate FAKE anharmonicities
# -------------------------------
anharmonicities = -0.3 + np.random.randn(10) * 0.01  # ~ -0.3 GHz

# -------------------------------
# Package into JSON dictionary
# -------------------------------
output_data = {
    "qubit_frequencies_GHz": qubit_freqs.tolist(),
    "coupling_strengths_GHz": coupling_strengths.tolist(),
    "readout_resonator_freqs_GHz": readout_freqs.tolist(),
    "anharmonicity_GHz": anharmonicities.tolist(),
    "design_mode": "STUB",
    "note": "This is a stub version for testing the pipeline without Qiskit Metal."
}

# -------------------------------
# Save the fake design results
# -------------------------------
output_filename = "design_results_stub.json"
with open(output_filename, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"✅ Design STUB complete! Saved output to {output_filename}")
print("   You may now continue the pipeline.")
