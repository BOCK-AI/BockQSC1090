"""
QML Demo – Early-Stage Prototype

This script introduces a minimal hybrid quantum–classical workflow.
It performs:
1. Classical data preparation
2. Parameter-based quantum-style encoding
3. Fake 2-qubit measurement sampling
4. Probability extraction for each data point

Note:
This is an early placeholder version without real quantum simulation.
"""

import random
import json

# Small sample dataset (2D points)
data_points = [
    [0.1, 0.2],
    [1.0, 1.2],
    [0.15, 0.25]
]


class QMLDemo:
    def __init__(self):
        self.num_qubits = 2
        self.shots = 201
        self.encoding_method = "rotation_based"

    def encode_data(self, point):
        """
        Maps a 2D classical data point to simple rotation-style parameters.
        This does not simulate quantum gates; it only prepares a structure
        for future integration.
        """
        x1, x2 = point
        theta1 = x1 * 3.14
        theta2 = x2 * 3.14

        encoded_ops = [
            {"gate": "RX", "qubit": 0, "angle": theta1},
            {"gate": "RY", "qubit": 1, "angle": theta2}
        ]

        return encoded_ops

    def sample_measurement(self):
        """
        Generates a random 2-qubit measurement outcome as a placeholder.
        Used until a proper simulator or pulse execution is integrated.
        """
        b0 = random.choice([0, 1])
        b1 = random.choice([0, 1])
        return f"{b0}{b1}"

    def measurement_statistics(self):
        """
        Collects frequency statistics for all 2-qubit outcomes.
        Produces simple probability-like values.
        """
        counts = {"00": 0, "01": 0, "10": 0, "11": 0}

        for _ in range(self.shots):
            outcome = self.sample_measurement()
            counts[outcome] += 1

        # Convert counts to probabilities
        for key in counts:
            counts[key] /= self.shots

        return counts

    def run(self):
        """
        Executes the early-stage QML pipeline:
        - encode classical data
        - generate placeholder measurement statistics
        - return structured outputs
        """
        results = []

        for point in data_points:
            encoded = self.encode_data(point)
            meas = self.measurement_statistics()

            results.append({
                "input_data": point,
                "encoded_ops": encoded,
                "measurement_stats": meas
            })

        print("\nQML Demo Output:")
        for r in results:
            print(json.dumps(r))

        return results


if __name__ == "__main__":
    qml = QMLDemo()
    qml.run()
