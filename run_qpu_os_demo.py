from quantum_gates import QuantumGateImplementation
from pulse_engine.scheduler import PulseScheduler
from pulse_engine.execution_engine import PulseExecutor
from qpu_os import QPUOS

def main():
    gate_engine = QuantumGateImplementation()
    scheduler = PulseScheduler()
    executor = PulseExecutor()

    os_layer = QPUOS(gate_engine, scheduler, executor)

    stages = os_layer.run_circuit("H(0); CNOT(0,1); X(1)")

    print("\nPipeline Stages:")
    for s in stages:
        print(s)

if __name__ == "__main__":
    main()
