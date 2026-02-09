class BigAlgoCompiler:
    """Flattens blocks into a single gate list."""

    def compile_blocks(self, blocks):
        flat_list = []
        for block in blocks:
            flat_list.extend(block)
        return flat_list