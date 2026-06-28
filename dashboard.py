import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="10-Qubit Processor Dashboard", layout="wide")

# ----------------------------------------------------------
# Helper: Safe JSON loader
# ----------------------------------------------------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

# ----------------------------------------------------------
# Helper: Search auto in cwd, pipeline_output/, fabrication_output/
# ----------------------------------------------------------
def smart_load(filename):
    search_paths = [
        filename,
        os.path.join("pipeline_output", filename),
        os.path.join("fabrication_output", filename)
    ]
    for p in search_paths:
        if os.path.exists(p):
            return load_json(p)
    return None

# ----------------------------------------------------------------------------------------
# Quantum Algorithm Runner Backend
# ----------------------------------------------------------------------------------------

def apply_single_qubit_gate(state, gate, qubit, num_qubits):
    I = np.eye(2)
    full_gate = 1
    for q in reversed(range(num_qubits)):
        full_gate = np.kron(full_gate, gate if q == qubit else I)
    return full_gate @ state

def apply_cnot(state, control, target, num_qubits):
    size = 2 ** num_qubits
    new_state = np.copy(state)
    for i in range(size):
        if (i >> control) & 1:
            flipped = i ^ (1 << target)
            new_state[flipped] = state[i]
            new_state[i] = state[flipped]
    return new_state

# Standard gates
H_GATE = (1/np.sqrt(2))*np.array([[1,1],[1,-1]])
X_GATE = np.array([[0,1],[1,0]])
Y_GATE = np.array([[0,-1j],[1j,0]])
Z_GATE = np.array([[1,0],[0,-1]])

def parse_algo_text(text):
    ops = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        gate = parts[0].upper()
        args = list(map(int, parts[1:])) if len(parts) > 1 else []
        ops.append((gate, args))
    return ops

def execute_ops(ops, num_qubits=10):
    state = np.zeros(2**num_qubits, dtype=complex)
    state[0] = 1  # start in |000...0>
    log = []

    for gate, args in ops:

        if gate == "H":
            q = args[0]
            log.append(f"H {q}")
            state = apply_single_qubit_gate(state, H_GATE, q, num_qubits)

        elif gate == "X":
            q = args[0]
            log.append(f"X {q}")
            state = apply_single_qubit_gate(state, X_GATE, q, num_qubits)

        elif gate == "Y":
            q = args[0]
            log.append(f"Y {q}")
            state = apply_single_qubit_gate(state, Y_GATE, q, num_qubits)

        elif gate == "Z":
            q = args[0]
            log.append(f"Z {q}")
            state = apply_single_qubit_gate(state, Z_GATE, q, num_qubits)

        elif gate == "CNOT":
            c, t = args
            log.append(f"CNOT {c} {t}")
            state = apply_cnot(state, c, t, num_qubits)

        elif gate == "MEASURE":
            log.append("MEASURE")
            probabilities = np.abs(state)**2
            outcome = np.random.choice(len(probabilities), p=probabilities)
            bitstring = format(outcome, f"0{num_qubits}b")
            return bitstring, log

    # Auto measure at end if none is present
    probabilities = np.abs(state)**2
    outcome = np.random.choice(len(probabilities), p=probabilities)
    bitstring = format(outcome, f"0{num_qubits}b")
    return bitstring, log


# ----------------------------------------------------------
# UI Title
# ----------------------------------------------------------
st.title("🔭 10-Qubit Quantum Processor Dashboard")
st.write("A clean, stable, production-ready monitoring and simulation UI.")

# ----------------------------------------------------------
# Tabs
# ----------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Design",
    "🧪 Simulations",
    "⚡ Gate Operations",
    "🛠 Verification",
    "🧮 Run Custom Algorithm"
])


# =================================================================
# 📐 TAB 1 — DESIGN
# =================================================================
with tab1:
    st.header("📐 Quantum Processor Design")

    design = smart_load("design_results.json")
    metadata = smart_load("10qubit_processor_v1_metadata.json")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Design Metadata")
        if metadata:
            st.json(metadata)
        else:
            st.info("Metadata not generated yet. Run pipeline.")

    with col2:
        st.subheader("Design Structure")
        if design:
            st.json(design)
        else:
            st.info("Design results missing. Run pipeline.")

    # Frequency plot
    if design and "qubit_parameters" in design:
        try:
            st.subheader("Qubit Frequencies (GHz)")
            freqs = [q["frequency_01"] for q in design["qubit_parameters"].values()]
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(range(len(freqs)), freqs)
            ax.set_xlabel("Qubit Index")
            ax.set_ylabel("GHz")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)
        except Exception:
            st.info("Frequency data not available.")


# =================================================================
# 🧪 TAB 2 — SIMULATIONS
# =================================================================
with tab2:
    st.header("🧪 System Simulation Outputs")

    sim_files = {
        "Circuit Parameters": "circuit_parameters.json",
        "Single-Qubit Gate Simulation": "single_qubit_gates.json",
        "Two-Qubit Gate Simulation": "two_qubit_gates.json",
        "Readout Performance": "readout_performance.json",
        "System Benchmarks": "system_benchmarks.json"
    }

    for title, filename in sim_files.items():
        st.subheader(f"📊 {title}")
        data = smart_load(filename)

        if data:
            st.json(data)

            # Plot qubit frequency map
            if title == "System Benchmarks" and "frequencies" in data:
                fig, ax = plt.subplots(figsize=(7, 3))
                ax.plot(data["frequencies"], marker="o")
                ax.set_title("System Benchmark: Qubit Frequency Map")
                ax.set_xlabel("Qubit Index")
                ax.set_ylabel("GHz")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

        else:
            st.info(f"{filename} will appear after running pipeline.")


# =================================================================
# ⚡ TAB 3 — GATE OPERATIONS
# =================================================================
with tab3:
    st.header("⚡ Quantum Gate Analysis")

    calib = smart_load("gate_calibration_Q0.json")
    rb = smart_load("randomized_benchmarking_Q0.json")
    seq = smart_load("compiled_circuit.json")

    # Calibration
    st.subheader("Single-Qubit Calibration (Q0)")
    if calib:
        st.json(calib)
    else:
        st.info("Calibration results not found.")

    # RB
    st.subheader("Randomized Benchmarking")
    if rb:
        st.json(rb)
        if "depths" in rb and "survival_probabilities" in rb:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(rb["depths"], rb["survival_probabilities"], marker="o")
            ax.set_xlabel("Circuit Depth")
            ax.set_ylabel("Survival Probability")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.info("RB results missing.")

    # Circuit compilation timeline
    st.subheader("Compiled Circuit Timeline")
    if seq:
        gates = seq.get("gate_sequence", seq.get("gates"))
        if gates:
            st.json(gates)
            durations = [g.get("duration_ns", 20) for g in gates]
            fig, ax = plt.subplots(figsize=(7, 3))
            ax.bar(range(len(durations)), durations)
            ax.set_xlabel("Gate Index")
            ax.set_ylabel("Duration (ns)")
            ax.set_title("Gate Timeline")
            ax.grid(True, alpha=0.2)
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Circuit file found but contains no gate list.")
    else:
        st.info("compiled_circuit.json missing.")


# =================================================================
# 🛠 TAB 4 — VERIFICATION
# =================================================================
with tab4:
    st.header("🛠 Verification Reports")

    reports = sorted([f for f in os.listdir(".") if f.startswith("verification_report")])
    summaries = sorted([f for f in os.listdir(".") if f.startswith("verification_summary")])

    if reports:
        st.subheader("Latest Verification Report")
        st.json(load_json(reports[-1]))
    else:
        st.info("No verification reports yet.")

    if summaries:
        st.subheader("Summary Log")
        with open(summaries[-1], "r") as f:
            st.code(f.read())
    else:
        st.info("No verification summaries yet.")


# =================================================================
# 🧮 TAB 5 — CUSTOM ALGORITHM RUNNER
# =================================================================
with tab5:
    st.header("🧮 Run Custom Quantum Algorithm (.algo)")

    default_algo = """# Example Bell State
H 0
CNOT 0 1
MEASURE
"""

    algo_text = st.text_area("Write your .algo code here:", default_algo, height=250)
    uploaded = st.file_uploader("Or upload a .algo file:", type=["algo"])

    if uploaded:
        algo_text = uploaded.read().decode("utf-8")

    if st.button("Run Algorithm"):
        try:
            ops = parse_algo_text(algo_text)

            st.subheader("Parsed Instructions")
            st.json(ops)

            result, log = execute_ops(ops)

            st.subheader("Execution Log")
            st.text("\n".join(log))

            st.subheader("Final Measurement Result")
            st.success(result)

        except Exception as e:
            st.error(f"Execution error: {e}")


# =================================================================
# FOOTER
# =================================================================
st.markdown("---")
st.write("Dashboard — Built for 10-Qubit Quantum Processor Development")
