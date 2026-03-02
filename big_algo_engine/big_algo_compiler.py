# big_algo_engine/big_algo_compiler.py

class BigAlgoCompiler:

    def compile_blocks(self, blocks):
        """
        Flatten block list into a single gate list.
        Input:  blocks = [ { "gates": [...] }, ... ]
        Output: [ {...}, {...}, ... ]
        """
        final_gate_list = []

        for block in blocks:
            final_gate_list.extend(block["gates"])

        return final_gate_list