# run_multi_job_demo.py

from qpu_os import QPUOS
from quantum_gates import QuantumGateImplementation
from pulse_engine.scheduler import PulseScheduler
from pulse_engine.execution_engine import PulseExecutor

from job_layer.job_manager import JobManager


def main():

    # OS Layer
    gate_engine = QuantumGateImplementation()
    scheduler = PulseScheduler()
    executor = PulseExecutor()
    os_layer = QPUOS(gate_engine, scheduler, executor)

    manager = JobManager(os_layer)

    # ---- SUBMIT MULTIPLE JOBS ----
    job1 = manager.submit_job("H(0); X(1)")
    job2 = manager.submit_job("H(0); CNOT(0,1)")
    job3 = manager.submit_job("X(0); H(1)")

    print("Submitted jobs:", job1, job2, job3)

    # ---- EXECUTE JOBS ONE BY ONE ----
    for i in range(3):
        finished_id, result = manager.run_next()
        print(f"\nFinished job: {finished_id}")
        print("Result:", result)
        print("Final status:", manager.get_status(finished_id))


if __name__ == "__main__":
    main()
