print("\n============================================================")
print("BIG ALGORITHM PIPELINE RUN")
print("============================================================\n")

import sys
import os
sys.path.append(os.getcwd())

from big_algo_engine.block_builder import BigAlgoBlockBuilder
from big_algo_engine.big_algo_compiler import BigAlgoCompiler
from quantum_gates import QuantumGateImplementation
from pulse_engine.scheduler import PulseScheduler
from pulse_engine.waveform_builder import WaveformBuilder
from pulse_engine.execution_engine import PulseExecutor


def main():

    # 1. BLOCK BUILDING
    print("------------------------------------------------------------")
    print("1. BLOCK CONSTRUCTION")
    print("------------------------------------------------------------")

    block_builder = BigAlgoBlockBuilder()
    blocks = block_builder.chain_blocks(num_blocks=3)
    print(f"✓ Built {len(blocks)} blocks")

    # 2. COMPILATION
    print("\n------------------------------------------------------------")
    print("2. COMPILATION")
    print("------------------------------------------------------------")

    compiler = BigAlgoCompiler()
    gate_list = compiler.compile_blocks(blocks)

    print("✓ Gates produced:")
    for g in gate_list:
        print(" ", g)

    # 3. GATES → PULSES
    print("\n------------------------------------------------------------")
    print("3. GATE → PULSE CONVERSION")
    print("------------------------------------------------------------")

    gate_engine = QuantumGateImplementation()
    pulses = []
    for g in gate_list:
        pulses.extend(gate_engine.gate_to_pulses(g))

    print(f"✓ {len(pulses)} pulses generated")

    # 4. SCHEDULING
    print("\n------------------------------------------------------------")
    print("4. SCHEDULING")
    print("------------------------------------------------------------")

    scheduler = PulseScheduler()
    scheduled = scheduler.schedule(pulses)

    print(f"✓ {len(scheduled)} pulses scheduled")

    # 5. WAVEFORMS
    print("\n------------------------------------------------------------")
    print("5. WAVEFORM GENERATION")
    print("------------------------------------------------------------")

    WaveformBuilder.build(scheduled, path="compiled_waveforms.json")
    print("✓ Waveforms saved")

    # 6. EXECUTION
    print("\n------------------------------------------------------------")
    print("6. EXECUTION")
    print("------------------------------------------------------------")

    executor = PulseExecutor()
    executor.load_schedule("compiled_waveforms.json")
    executor.execute()

    print("\n============================================================")
    print("BIG ALGORITHM PIPELINE COMPLETE")
    print("============================================================\n")


if __name__ == "__main__":
    main()