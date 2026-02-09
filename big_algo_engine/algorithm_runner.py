# algorithm_runner.py

class AlgorithmRunner:
    def __init__(self):
        pass

    def parse_text(self, text: str):
        lines = text.splitlines()
        ops = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            gate = parts[0].upper()

            if gate == "CNOT":
                ops.append({"gate": "CNOT", "control": int(parts[1]), "target": int(parts[2])})
            else:
                ops.append({"gate": gate, "qubit": int(parts[1])})

        return ops
        