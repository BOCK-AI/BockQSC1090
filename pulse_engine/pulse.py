from dataclasses import dataclass
from typing import Callable, Optional
import math

Waveform = Callable[[float], float]

@dataclass
class Pulse:
    name: str
    duration: float        # seconds
    amplitude: float = 1.0
    phase: float = 0.0     # radians
    waveform: Optional[Waveform] = None
    channel: str = "d0"

    def sample(self, t: float) -> float:
        if self.waveform:
            # waveform expects normalized time 0..1
            x = max(0.0, min(1.0, t / max(1e-12, self.duration)))
            w = self.waveform(x)
        else:
            w = 1.0
        return self.amplitude * w * math.cos(self.phase)

def constant_wave(x: float) -> float:
    return 1.0

def gaussian_wave(x: float, sigma: float = 0.15) -> float:
    return math.exp(-(x - 0.5) ** 2 / (2 * sigma ** 2))
