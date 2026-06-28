import time

class QuantumGateImplementation:
    """
    Converts logical gates into hardware-level pulse objects.
    Used by both small circuits and big-algorithm compiler.
    """

    def __init__(self):
        self.default_duration = {
            "H": 20e-9,
            "X": 20e-9,
            "Y": 20e-9,
            "Z": 20e-9,
            "CNOT": 200e-9,
        }

    def gate_to_pulses(self, gate):
        """
        Convert a gate dict into 1 or more Pulse objects.
        Gate example:
            {"gate": "H", "qubit": 0, "duration_ns": 20}
            {"gate": "CNOT", "control": 0, "target": 1, "duration_ns": 200}
        """
        from pulse_engine.pulse import Pulse

        g = gate["gate"]

        if g in ("H", "X", "Y", "Z"):
            q = gate["qubit"]
            duration_s = gate["duration_ns"] * 1e-9

            return [
                Pulse(
                    name=f"{g}_{q}",
                    duration=duration_s,
                    channel=f"d{q}",
                    amplitude=1.0,
                    phase=0.0,
                )
            ]

        elif g == "CNOT":
            ctrl = gate["control"]
            tgt = gate["target"]
            duration_s = gate["duration_ns"] * 1e-9

            return [
                Pulse(
                    name=f"CNOT_ctrl_{ctrl}",
                    duration=duration_s,
                    channel=f"d{ctrl}",
                    amplitude=1.0,
                    phase=0.0,
                ),
                Pulse(
                    name=f"CNOT_tgt_{tgt}",
                    duration=duration_s,
                    channel=f"d{tgt}",
                    amplitude=1.0,
                    phase=0.0,
                ),
            ]

        else:
            raise ValueError(f"Unsupported gate: {g}")


    def compile_circuit(self, circuit_str):
        """
        Still used by old pipeline. Keeps compatibility.
        """
        ops = circuit_str.split(";")
        gates = []
        total_ns = 0

        for op in ops:
            op = op.strip()
            if not op:
                continue

            name = op.split("(")[0]
            params = op.split("(")[1].split(")")[0]

            if "," in params:
                ctrl, tgt = map(int, params.split(","))
                gates.append({
                    "gate": "CNOT",
                    "control": ctrl,
                    "target": tgt,
                    "duration_ns": 200,
                })
                total_ns += 200

            else:
                q = int(params)
                gates.append({
                    "gate": name,
                    "qubit": q,
                    "duration_ns": 20,
                })
                total_ns += 20

        return {
            "timestamp": time.ctime(),
            "circuit": circuit_str,
            "gates": gates,
            "total_duration_ns": total_ns,
        }

if __name__ == "__main__":
    print("✅ Quantum Gates module loaded successfully.")