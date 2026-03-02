# big_algo_engine/block_builder.py

class BigAlgoBlockBuilder:

    def build_single_block(self):
        """
        Returns one block of 4 gates.
        Format:
        { "gates": [ {...}, {...} ] }
        """
        return {
            "gates": [
                {"gate": "H", "qubit": 0, "duration_ns": 20},
                {"gate": "X", "qubit": 1, "duration_ns": 20},
                {"gate": "CNOT", "control": 0, "target": 1, "duration_ns": 200},
                {"gate": "H", "qubit": 0, "duration_ns": 20},
            ]
        }

    def chain_blocks(self, num_blocks=3):
        blocks = []
        for _ in range(num_blocks):
            blocks.append(self.build_single_block())
        return blocks  # list of dict blocks