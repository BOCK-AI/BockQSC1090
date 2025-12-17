import random

class MeasurementEngine:
    def __init__(self, readout_error=0.03):
        """
        readout_error: probability of flipping the measured bit
        """
        self.readout_error = readout_error

    def measure_qubit(self, qubit_id):
        """
        Mock measurement of a qubit.
        Returns 0 or 1.
        """
        # Ideal outcome (random for now)
        result = random.choice([0, 1])

        # Apply readout error
        if random.random() < self.readout_error:
            result = 1 - result

        return result

    def measure_all(self, num_qubits):
        """
        Measure all qubits.
        """
        return {f"Q{q}": self.measure_qubit(q) for q in range(num_qubits)}
