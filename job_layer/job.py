# job_layer/job.py

import uuid
import time

class Job:
    def __init__(self, circuit):
        self.id = str(uuid.uuid4())
        self.circuit = circuit
        self.status = "PENDING"
        self.created_at = time.time()
        self.result = None

    def set_status(self, status):
        self.status = status

    def set_result(self, result):
        self.result = result
