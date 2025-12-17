from pulse_engine.pulse_sequence import circuit_to_pulses
from pulse_engine.scheduler import PulseScheduler
from pulse_engine.waveform_builder import build_waveform
from pulse_engine.timing_engine import align_to_hardware_clock

# Fake small circuit for demo
circuit = [
    {"gate": "X", "qubit": 0},
    {"gate": "H", "qubit": 1},
    {"gate": "CNOT", "qubit": 0},
]

pulses = circuit_to_pulses(circuit)
scheduler = PulseScheduler(clock_resolution=1e-9)
schedule = scheduler.schedule(pulses)
schedule = align_to_hardware_clock(schedule, clock=1e-9)

for sp in schedule:
    print(f"{sp.pulse.name} @ {sp.start_time*1e9:.1f} ns → {sp.end_time*1e9:.1f} ns on {sp.pulse.channel}")

# show first pulse waveform
samples = build_waveform(schedule[0])
print("First pulse sample count:", len(samples))
print("First 10 samples:", samples[:10].tolist())
