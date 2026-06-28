"""
10-Qubit Quantum Processor — Full Pipeline Runner (Production Version)
---------------------------------------------------------------------

This pipeline runs:
1. Design generation (main_10qubit_design.py)
2. KLayout processing (klayout_quantum_processor.py)
3. System simulations (quantum_processor_simulation.py)
4. Gate operations + calibration (quantum_gates.py)
5. Verification tests (quantum_processor_verification.py)

All outputs are saved to the correct folders for dashboard visualization.

Author: QPU Development Team
"""

import os
import sys
import subprocess

os.makedirs("pipeline_output", exist_ok=True)
os.makedirs("fabrication_output", exist_ok=True)

print("\n🚀 Starting 10-Qubit Processor Pipeline...\n")


# ------------------------------------------------------------
# Helper function to execute scripts safely
# ------------------------------------------------------------
def run_step(label, command):
    print(f"\n🔹 Running {label}...")
    cmd_list = command.split()
    if cmd_list[0] == "python":
        cmd_list[0] = sys.executable
    result = subprocess.run(cmd_list)
    
    if result.returncode != 0:
        print(f"❌ ERROR: {label} failed.")
        sys.exit(1)

    print(f"✅ Finished {label}")


# ------------------------------------------------------------
# 1. DESIGN GENERATION
# ------------------------------------------------------------
run_step("core/main_10qubit_design.py", "python core/main_10qubit_design.py")


# ------------------------------------------------------------
# 2. KLAYOUT PROCESSING
# ------------------------------------------------------------
run_step("core/klayout_quantum_processor.py", "python core/klayout_quantum_processor.py")


# ------------------------------------------------------------
# 3. SYSTEM SIMULATIONS
# ------------------------------------------------------------
run_step("core/quantum_processor_simulation.py", "python core/quantum_processor_simulation.py")


# ------------------------------------------------------------
# 4. QUANTUM GATE OPERATIONS (NEW production version)
# ------------------------------------------------------------
run_step("core/quantum_gates.py", "python core/quantum_gates.py")


# ------------------------------------------------------------
# 5. VERIFICATION SUITE
# ------------------------------------------------------------
run_step("core/quantum_processor_verification.py", "python core/quantum_processor_verification.py")


print("\n🎉 Pipeline completed successfully!\n")


# ------------------------------------------------------------
# Summary of generated files
# ------------------------------------------------------------
print("📁 Generated Files Summary:")
print("- pipeline_output/design_results.json")
print("- pipeline_output/10qubit_processor_v1_metadata.json")
print("- fabrication_output/10qubit_processor_fab.gds")
print("- fabrication_output/fabrication_report.txt")
print("- gate_calibration_Q0.json")
print("- randomized_benchmarking_Q0.json")
print("- compiled_circuit.json")

print("\n📊 Verification files:")
print("- verification_report_*.json")
print("- verification_summary_*.txt")

print("\n🎯 Dashboard Ready! Run:")
print("   streamlit run dashboard.py\n")
