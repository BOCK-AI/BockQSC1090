# big_algo_engine/gate_validator.py

class GateValidator:
    """
    Simple rule-based validator for big algorithm gate lists.
    Ensures:
      - allowed gates only
      - qubit indices are valid (0–9 by default)
      - duration exists
    """

    def __init__(self, max_qubits=10, allowed_gates=None):
        self.max_qubits = max_qubits
        self.allowed_gates = allowed_gates or ["H", "X", "CNOT"]

    def validate(self, gate_list):
        validated = []
        for g in gate_list:

            # Gate name check
            gate_name = g["gate"]
            if gate_name not in self.allowed_gates:
                raise ValueError(f"Invalid gate: {gate_name}")

            # Duration check
            if "duration_ns" not in g:
                raise ValueError(f"Missing duration for: {g}")

            # Qubit index check
            if gate_name == "CNOT":
                if g["control"] >= self.max_qubits or g["target"] >= self.max_qubits:
                    raise ValueError(f"CNOT qubit index out of range: {g}")
            else:
                if g["qubit"] >= self.max_qubits:
                    raise ValueError(f"Qubit index out of range: {g}")

            validated.append(g)

        return validated