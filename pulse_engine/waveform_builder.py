# pulse_engine/waveform_builder.py

import json

class WaveformBuilder:
    """
    Converts scheduled pulses into raw sample waveforms.
    Output saved in a single JSON for execution engine.
    """

    @staticmethod
    def build(scheduled_pulses, path="compiled_waveforms.json"):
        waveforms = []

        for sp in scheduled_pulses:
            pulse = sp.pulse
            duration = pulse.duration
            num_samples = int(duration * 2e9)  # 2 GSa/s

            # Simple placeholder: flat amplitude
            samples = [pulse.amplitude] * max(1, num_samples)

            waveforms.append({
                "name": pulse.name,
                "channel": pulse.channel,
                "start_time_s": sp.start_time,
                "end_time_s": sp.end_time,
                "samples": samples
            })

        with open(path, "w") as f:
            json.dump(waveforms, f, indent=2)

        print(f"[WaveformBuilder] Wrote {len(waveforms)} waveforms to {path}")