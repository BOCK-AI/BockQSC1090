from typing import List
from dataclasses import dataclass
from .pulse import Pulse

@dataclass
class ScheduledPulse:
    pulse: Pulse
    start_time: float
    end_time: float

class PulseScheduler:
    def __init__(self, clock_resolution=1e-9):
        self.clock = clock_resolution

    def schedule(self, pulses: List[Pulse]) -> List[ScheduledPulse]:
        schedule = []
        channel_end_times = {}
        for p in pulses:
            last_end = channel_end_times.get(p.channel, 0.0)
            start = round(last_end / self.clock) * self.clock
            end = start + p.duration
            schedule.append(ScheduledPulse(pulse=p, start_time=start, end_time=end))
            channel_end_times[p.channel] = end
        return schedule
