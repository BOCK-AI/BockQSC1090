import numpy as np
from .scheduler import ScheduledPulse

def build_waveform(sp: ScheduledPulse, sample_rate=1e9):
    n_samples = max(1, int(sp.pulse.duration * sample_rate))
    times = np.linspace(0, sp.pulse.duration, n_samples, endpoint=False)
    samples = np.array([sp.pulse.sample(t) for t in times])
    return samples
