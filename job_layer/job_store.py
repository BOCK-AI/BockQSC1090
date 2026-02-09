# job_layer/job_store.py

class JobStore:
    def __init__(self):
        self.jobs = {}

    def add(self, job):
        self.jobs[job.id] = job

    def get(self, job_id):
        return self.jobs.get(job_id)

    def update(self, job):
        self.jobs[job.id] = job
