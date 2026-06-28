print("\n============================================================")
print("RUNNING SHA-256 STYLE ALGORITHM THROUGH QPU PIPELINE")
print("============================================================")

import os, sys
sys.path.append(os.getcwd())

# SHA-256 components (inside sha256/)
from sha256.sha256_blocks import SHA256BlockBuilder
from sha256.sha256_compiler import SHA256Compiler

# QPU pipeline
from core.quantum_gates import QuantumGateImplementation
from pulse_engine.scheduler import PulseScheduler
from pulse_engine.execution_engine import PulseExecutor
from core.qpu_os import QPUOS


def main():

    # 1. BUILD 64 BLOCKS
    print("\n--- 1. BUILDING 64 ROUNDS ---")
    builder = SHA256BlockBuilder()
    blocks = builder.build_sha256(rounds=64)
    print(f"✓ Built {len(blocks)} rounds")

    # 2. COMPILE BLOCKS → GATES
    print("\n--- 2. COMPILING BLOCKS → GATES ---")
    compiler = SHA256Compiler()
    gate_list = compiler.compile_sha_blocks(blocks)
    print(f"✓ Total gates produced: {len(gate_list)}")

    # 3. RUN THROUGH QPU OS LAYER
    print("\n--- 3. RUNNING THROUGH OS LAYER ---")
    gate_engine = QuantumGateImplementation()
    scheduler = PulseScheduler()
    executor = PulseExecutor()
    os_layer = QPUOS(gate_engine, scheduler, executor)

    stages = os_layer.run_gate_list(gate_list)

    # 4. OUTPUT
    print("\n✓ Pipeline stages:")
    for s in stages:
        print(" -", s)

    print("\n============================================================")
    print("SHA-256 PIPELINE EXECUTION COMPLETE")
    print("============================================================")


if __name__ == "__main__":
    main()