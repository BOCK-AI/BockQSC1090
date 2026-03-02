# pulse_engine/execution_engine_advanced.py

class PulseExecutor:
    def __init__(self, batch_size=200):
        self.batch_size = batch_size

    def load_schedule(self, path="compiled_waveforms.json"):
        import json
        with open(path, "r") as f:
            self.schedule = json.load(f)

    def execute(self):
        pulses = self.schedule

        print("\n=== EXECUTION (BATCHED) ===")

        # Split into batches
        batches = [
            pulses[i:i + self.batch_size]
            for i in range(0, len(pulses), self.batch_size)
        ]

        for i, batch in enumerate(batches):
            print(f"\n--- Batch {i+1}/{len(batches)} | {len(batch)} pulses ---")

            for p in batch:
                print(f"[EXEC] {p['name']} | ch={p['channel']} | duration={p['end_time_s']-p['start_time_s']:.2e}s")

        print("\n=== EXECUTION COMPLETE ===\n")