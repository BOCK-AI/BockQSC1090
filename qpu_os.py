# qpu_os.py

import json
from pulse_engine.pulse import Pulse


class QPUOS:
    """
    OS-layer controlling the full execution path:

        circuit OR precompiled gate-list
            → compile
            → schedule
            → waveform json
            → execute pulses

    Works for:
    - small circuits
    - large SHA256-style algorithms (gate lists)
    - job manager
    """

    def __init__(self, gate_engine, scheduler, executor):
        self.gate_engine = gate_engine
        self.scheduler = scheduler
        self.executor = executor

    # ===============================================================
    # CASE 1 — NORMAL CIRCUIT: "H(0); CNOT(0,1)"
    # ===============================================================
    def run_circuit(self, circuit_str):
        stages = []

        # 1. compile
        stages.append("stage: compile")
        compiled = self.gate_engine.compile_circuit(circuit_str)

        gate_list = compiled["gates"]

        # convert to pulses
        pulses = self._gates_to_pulses(gate_list)

        # 2. schedule
        stages.append("stage: schedule")
        scheduled = self.scheduler.schedule(pulses)

        # 3. waveform export
        stages.append("stage: waveforms")
        self._export_waveforms(scheduled)

        # 4. execute
        stages.append("stage: execute")
        self.executor.load_schedule("compiled_waveforms.json")
        self.executor.execute()

        return stages

    # ===============================================================
    # CASE 2 — SHA256 OR ANY BIG ALGO (already compiled gate list)
    # ===============================================================
    def run_gate_list(self, gate_list):
        stages = []

        stages.append("stage: load-precompiled-gates")

        # convert to pulses
        pulses = self._gates_to_pulses(gate_list)

        # schedule pulses
        stages.append("stage: schedule")
        scheduled = self.scheduler.schedule(pulses)

        # export waveforms
        stages.append("stage: waveforms")
        self._export_waveforms(scheduled)

        # execution
        stages.append("stage: execute")
        self.executor.load_schedule("compiled_waveforms.json")
        self.executor.execute()

        return stages

    # ===============================================================
    # INTERNAL — gates → pulses
    # ===============================================================
    def _gates_to_pulses(self, gate_list):
        pulses = []

        for g in gate_list:
            duration = g.get("duration_ns", g.get("duration", 20))

            if g["gate"] == "CNOT":
                pulses.append(Pulse(
                    name=f"CNOT_ctrl_{g['control']}",
                    channel=f"d{g['control']}",
                    duration=duration * 1e-9
                ))
                pulses.append(Pulse(
                    name=f"CNOT_tgt_{g['target']}",
                    channel=f"d{g['target']}",
                    duration=duration * 1e-9
                ))

            else:
                pulses.append(Pulse(
                    name=f"{g['gate']}_{g['qubit']}",
                    channel=f"d{g['qubit']}",
                    duration=duration * 1e-9
                ))

        return pulses

    # ===============================================================
    # INTERNAL — scheduled pulses → waveform JSON
    # ===============================================================
    def _export_waveforms(self, scheduled):
        waveform_data = []

        for sp in scheduled:
            waveform_data.append({
                "name": sp.pulse.name,
                "channel": sp.pulse.channel,
                "start_time_s": sp.start_time,
                "end_time_s": sp.end_time,
                "samples": [0.1] * 10
            })

        with open("compiled_waveforms.json", "w") as f:
            json.dump(waveform_data, f, indent=4)