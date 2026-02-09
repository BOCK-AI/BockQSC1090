class BlockLibrary:
    """General-purpose modular algorithm blocks."""

    def single_qubit(self, q):
        return [f"X({q})"]

    def rotation(self, q, theta):
        return [f"RX({q},{theta})"]

    def two_qubit(self, gate, a, b):
        return [f"{gate}({a},{b})"]
