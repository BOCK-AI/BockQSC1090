import json
from pulse_engine.pulse import Pulse

class QPUOS:
    def __init__(self, gate_engine, scheduler, executor):
        self.gate_engine = gate_engine
        self.scheduler = scheduler
        self.executor = executor

    def run_circuit(self, circuit_str):
        stages = []
        stages.append("stage: compile")

        compiled = self.gate_engine.compile_circuit(circuit_str)

        pulses = []

        for g in compiled["gates"]:
            duration = g.get("duration_ns", g.get("duration", 20))

            if g["gate"] == "CNOT":
                pulses.append(Pulse(
                    name="CNOT_control",
                    channel=f"d{g['control']}",
                    duration=duration * 1e-9
                ))
                pulses.append(Pulse(
                    name="CNOT_target",
                    channel=f"d{g['target']}",
                    duration=duration * 1e-9
                ))
            else:
                pulses.append(Pulse(
                    name=g["gate"],
                    channel=f"d{g['qubit']}",
                    duration=duration * 1e-9
                ))

        stages.append("stage: schedule")
        scheduled = self.scheduler.schedule(pulses)

        waveform_data = []
        for sp in scheduled:
            waveform_data.append({
                "name": sp.pulse.name,
                "channel": sp.pulse.channel,
                "start_time_s": sp.start_time,
                "end_time_s": sp.end_time,
                "samples": [0.1] * 10
            })

        json.dump(waveform_data, open("compiled_waveforms.json", "w"), indent=4)

        stages.append("stage: execute")
        self.executor.load_schedule("compiled_waveforms.json")
        self.executor.execute()

        return stages
