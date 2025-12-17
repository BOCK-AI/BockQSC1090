class Channel:
    def __init__(self, name: str):
        self.name = name

class DriveChannel(Channel): pass
class MeasureChannel(Channel): pass
class FluxChannel(Channel): pass
