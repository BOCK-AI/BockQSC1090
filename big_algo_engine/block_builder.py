class BigAlgoBlockBuilder:
    """
    Creates block-level structures for large algorithms.
    Each block is represented as a small list of gate dictionaries.
    """

    def build_block(self, index=0):
        return [
            {"gate": "H", "qubit": 0, "duration_ns": 20},
            {"gate": "X", "qubit": 1, "duration_ns": 20},
            {"gate": "CNOT", "control": 0, "target": 1, "duration_ns": 200},
            {"gate": "H", "qubit": 0, "duration_ns": 20},
        ]

    def chain_blocks(self, num_blocks=3):
        blocks = []
        for i in range(num_blocks):
            blocks.append(self.build_block(index=i))
        return blocks