class BlockComposer:
    def chain(self, blocks):
        out = []
        for b in blocks:
            out.extend(b)
        return out

    def repeat(self, block, times):
        out = []
        for _ in range(times):
            out.extend(block)
        return out
