# job_layer/job_manager.py

from job_layer.job import Job
from job_layer.job_queue import JobQueue
from job_layer.job_store import JobStore
import job_layer.job_status as STATUS


class JobManager:
    def __init__(self, os_layer):
        self.os_layer = os_layer
        self.queue = JobQueue()
        self.store = JobStore()

    def submit_job(self, circuit):
        job = Job(circuit)
        self.queue.submit(job)
        self.store.add(job)
        return job.id

    def run_next(self):
        """
        Minimal job execution:
        - pop next job
        - mark as RUNNING
        - run via OS layer
        - mark as COMPLETED
        """
        job = self.queue.next_job()
        if not job:
            return None

        job.set_status(STATUS.RUNNING)
        self.store.update(job)

        try:
            result = self.os_layer.run_circuit(job.circuit)
            job.set_result(result)
            job.set_status(STATUS.COMPLETED)
        except Exception as e:
            job.set_result({"error": str(e)})
            job.set_status(STATUS.FAILED)

        self.store.update(job)
        return job.id, job.result

    def get_status(self, job_id):
        job = self.store.get(job_id)
        if job:
            return job.status
        return None

    def get_result(self, job_id):
        job = self.store.get(job_id)
        if job:
            return job.result
        return None

    def list_jobs(self):
        return list(self.store.jobs.keys())
