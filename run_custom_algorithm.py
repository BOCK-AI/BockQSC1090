import numpy as np
import argparse

# ============================================================
#  Utility: Apply quantum gates to statevector
# ============================================================

def apply_single_qubit_gate(state, gate, qubit, num_qubits):
    """Applies a 1-qubit gate to the full statevector."""
    I = np.eye(2)
    full_gate = 1

    for q in reversed(range(num_qubits)):
        if q == qubit:
            full_gate = np.kron(full_gate, gate)
        else:
            full_gate = np.kron(full_gate, I)

    return full_gate @ state


def apply_cnot(state, control, target, num_qubits):
    """Apply CNOT gate to statevector."""
    size = 2 ** num_qubits
    new_state = np.copy(state)

    for i in range(size):
        if (i >> control) & 1:  # If control = 1
            flipped = i ^ (1 << target)
            new_state[flipped] = state[i]
            new_state[i] = state[flipped]

    return new_state


# ============================================================
#  Gate Definitions
# ============================================================

H_GATE = (1 / np.sqrt(2)) * np.array([[1, 1],
                                      [1, -1]])

X_GATE = np.array([[0, 1],
                   [1, 0]])

Y_GATE = np.array([[0, -1j],
                   [1j, 0]])

Z_GATE = np.array([[1, 0],
                   [0, -1]])


# ============================================================
#  Load .algo File
# ============================================================

def load_algorithm(filename):
    """Reads a .algo file and returns a list of instructions."""
    operations = []

    try:
        with open(filename, "r", encoding="utf-8") as f:   # FIXED UTF-8 SUPPORT
            lines = f.readlines()
    except Exception as e:
        print(f"\n❌ ERROR reading file '{filename}': {e}")
        exit(1)

    for line in lines:
        line = line.strip()

        # Skip empty lines or comments
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        gate = parts[0].upper()

        if gate == "MEASURE":
            operations.append((gate, []))
        else:
            args = list(map(int, parts[1:]))
            operations.append((gate, args))

    return operations


# ============================================================
#  Execute Algorithm
# ============================================================

def execute_algorithm(ops, num_qubits=10):
    """Simulates the circuit described by the operations list."""

    # Initial state |0000000000>
    state = np.zeros(2 ** num_qubits, dtype=complex)
    state[0] = 1.0

    print("\n🔹 Beginning circuit simulation...\n")

    for (gate, args) in ops:

        if gate == "H":
            q = args[0]
            print(f"Applying H on qubit {q}")
            state = apply_single_qubit_gate(state, H_GATE, q, num_qubits)

        elif gate == "X":
            q = args[0]
            print(f"Applying X on qubit {q}")
            state = apply_single_qubit_gate(state, X_GATE, q, num_qubits)

        elif gate == "Y":
            q = args[0]
            print(f"Applying Y on qubit {q}")
            state = apply_single_qubit_gate(state, Y_GATE, q, num_qubits)

        elif gate == "Z":
            q = args[0]
            print(f"Applying Z on qubit {q}")
            state = apply_single_qubit_gate(state, Z_GATE, q, num_qubits)

        elif gate == "CNOT":
            c, t = args
            print(f"Applying CNOT control={c}, target={t}")
            state = apply_cnot(state, c, t, num_qubits)

        elif gate == "MEASURE":
            print("\n📥 Measuring final quantum state...")
            return measure_state(state)

        else:
            print(f"⚠️ Unknown gate: {gate}")

    print("\n⚠️ No MEASURE found in algorithm. Auto-measuring...")
    return measure_state(state)


# ============================================================
#  Measurement
# ============================================================

def measure_state(state):
    """Simulates measurement of all qubits."""
    probabilities = np.abs(state) ** 2
    outcome = np.random.choice(len(probabilities), p=probabilities)
    bitstring = format(outcome, "010b")
    print(f"\n🎉 Measurement Result: {bitstring}\n")
    return bitstring


# ============================================================
#  MAIN ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Run a .algo quantum program")
    parser.add_argument("--file", type=str, required=True,
                        help="Path to the .algo file")
    args = parser.parse_args()

    print(f"\n🚀 Running algorithm file: {args.file}")

    ops = load_algorithm(args.file)

    print("\n📜 Loaded Operations:")
    for op in ops:
        print("   ", op)

    result = execute_algorithm(ops)

    print(f"\n🏁 Final Output: {result}")


if __name__ == "__main__":
    main()
