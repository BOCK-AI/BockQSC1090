"""
Quantum Gate Implementation Library
-----------------------------------

Implements:
- Calibration & benchmarking
- Circuit compilation
- Pulse scheduling
- Waveform generation
- Pulse execution
- Measurement (mock readout)

This completes a full gate → pulse → execution → readout flow.
"""

import numpy as np
import json
import time

from pulse_engine.pulse_sequence import circuit_to_pulses
from pulse_engine.scheduler import PulseScheduler
from pulse_engine.waveform_builder import build_waveform
from pulse_engine.timing_engine import align_to_hardware_clock
from pulse_engine.execution_engine import PulseExecutor
from pulse_engine.measurement import MeasurementEngine


class QuantumGateImplementation:

    def __init__(self):
        self.sample_rate = 2e9  # 2 GS/s

    # --------------------------------------------------
    # Calibration (mock)
    # --------------------------------------------------
    def calibrate_qubit(self, qubit=0):
        return {
            "timestamp": time.ctime(),
            "qubit": qubit,
            "pi_pulse_amplitude": 0.85,
            "T1_us": 110.0,
            "T2_us": 60.0
        }

    # --------------------------------------------------
    # Randomized Benchmarking (mock)
    # --------------------------------------------------
    def randomized_benchmarking(self, qubit=0):
        return {
            "timestamp": time.ctime(),
            "qubit": qubit,
            "average_gate_fidelity": 0.996
        }

    # --------------------------------------------------
    # Circuit Compiler
    # --------------------------------------------------
    def compile_circuit(self, circuit_str):
        ops = circuit_str.split(";")
        gates = []

        for op in ops:
            op = op.strip()
            if not op:
                continue

            name = op.split("(")[0]
            params = op.split("(")[1].split(")")[0]

            if "," in params:
                c, t = map(int, params.split(","))
                gates.append({"gate": "CNOT", "control": c, "target": t})
            else:
                gates.append({"gate": name, "qubit": int(params)})

        return {
            "timestamp": time.ctime(),
            "circuit": circuit_str,
            "gates": gates
        }


# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    gate_impl = QuantumGateImplementation()

    print("Running calibration...")
    json.dump(gate_impl.calibrate_qubit(0),
              open("gate_calibration_Q0.json", "w"), indent=4)

    print("Running benchmarking...")
    json.dump(gate_impl.randomized_benchmarking(0),
              open("randomized_benchmarking_Q0.json", "w"), indent=4)

    print("Compiling circuit...")
    seq = gate_impl.compile_circuit("H(0); CNOT(0,1); X(1); H(1)")
    json.dump(seq, open("compiled_circuit.json", "w"), indent=4)

    # --------------------------------------------------
    # Gate → Pulse conversion
    # --------------------------------------------------
    converted = []
    for g in seq["gates"]:
        if g["gate"] == "CNOT":
            converted.append({"gate": "CNOT", "qubit": g["control"]})
            converted.append({"gate": "CNOT", "qubit": g["target"]})
        else:
            converted.append({"gate": g["gate"], "qubit": g["qubit"]})

    pulses = circuit_to_pulses(converted)

    # --------------------------------------------------
    # Pulse Scheduling
    # --------------------------------------------------
    scheduler = PulseScheduler(clock_resolution=1e-9)
    schedule = scheduler.schedule(pulses)
    schedule = align_to_hardware_clock(schedule)

    # --------------------------------------------------
    # Waveform Generation
    # --------------------------------------------------
    waveforms = []
    for sp in schedule:
        samples = build_waveform(sp, sample_rate=gate_impl.sample_rate)
        waveforms.append({
            "name": sp.pulse.name,
            "channel": sp.pulse.channel,
            "start_time_s": float(sp.start_time),
            "end_time_s": float(sp.end_time),
            "samples": [float(x) for x in samples.tolist()]
        })

    json.dump(waveforms, open("compiled_waveforms.json", "w"), indent=2)
    print("✓ compiled_waveforms.json generated")

    print("\nScheduled pulses:")
    for sp in schedule:
        print(f"  {sp.pulse.name} | {sp.start_time*1e9:.1f} → {sp.end_time*1e9:.1f} ns")

    # --------------------------------------------------
    # Pulse Execution
    # --------------------------------------------------
    executor = PulseExecutor(sample_rate=gate_impl.sample_rate)
    executor.load_schedule("compiled_waveforms.json")
    executor.execute()

    # --------------------------------------------------
    # Measurement
    # --------------------------------------------------
    meas = MeasurementEngine(readout_error=0.03)
    results = meas.measure_all(num_qubits=2)

    print("\nMeasurement results:")
    for q, r in results.items():
        print(f"  {q} → {r}")

    print("\n🎉 Quantum gates pipeline complete")


if __name__ == "__main__":
    main()
