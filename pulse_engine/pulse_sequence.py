from typing import List
from .pulse import Pulse, constant_wave

GATE_LIBRARY = {
    "X":  {"duration": 20e-9, "amplitude": 1.0, "waveform": constant_wave},
    "Y":  {"duration": 20e-9, "amplitude": 1.0, "waveform": constant_wave},
    "H":  {"duration": 30e-9, "amplitude": 0.7, "waveform": constant_wave},
    "CNOT": {"duration": 40e-9, "amplitude": 0.8, "waveform": constant_wave},
}

def circuit_to_pulses(circuit: List[dict]):
    pulses = []
    for inst in circuit:
        gate = inst["gate"]
        qubit = inst["qubit"]
        if gate not in GATE_LIBRARY:
            raise ValueError(f"Gate {gate} has no pulse template")
        tmpl = GATE_LIBRARY[gate]
        p = Pulse(
            name=f"{gate}_{qubit}",
            duration=tmpl["duration"],
            amplitude=tmpl["amplitude"],
            waveform=tmpl["waveform"],
            channel=f"d{qubit}"
        )
        pulses.append(p)
    return pulses
