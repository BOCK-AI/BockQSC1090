# sha256_compiler.py

class SHA256Compiler:
    def __init__(self):
        pass

    def compile_sha_blocks(self, block_list):
        flat_gate_list = []
        for block in block_list:
            for gate in block:
                flat_gate_list.append(gate)
        return flat_gate_list