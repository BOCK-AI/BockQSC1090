import json
import time

class PulseExecutor:
    def __init__(self, sample_rate=2e9):
        self.sample_rate = sample_rate
        self.clock_period = 1 / sample_rate  # seconds

    def load_schedule(self, path="compiled_waveforms.json"):
        with open(path, "r") as f:
            self.schedule = json.load(f)

        # Sort pulses by start time
        self.schedule.sort(key=lambda p: p["start_time_s"])

        print(f"Loaded {len(self.schedule)} pulses for execution.")

    def execute(self):
        """
        Execute pulses according to their scheduled times.
        """
        print("\n=== Pulse Execution Started ===")

        current_time = 0.0

        for p in self.schedule:
            start = p["start_time_s"]
            end = p["end_time_s"]

            # Respect timing gaps
            if start > current_time:
                gap = start - current_time
                print(f"[WAIT] {gap*1e9:.1f} ns")
                # No real sleep — placeholder for hardware clock

            duration = end - start
            print(f"[EXEC] {p['name']} | {duration*1e9:.1f} ns | channel={p['channel']}")

            # Simulate waveform playback
            samples = p["samples"]
            print(f"   Playing {len(samples)} samples")

            current_time = end

        print("=== Pulse Execution Finished ===\n")
