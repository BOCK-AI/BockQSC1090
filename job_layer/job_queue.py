# job_layer/job_queue.py

from collections import deque

class JobQueue:
    def __init__(self):
        self.queue = deque()

    def submit(self, job):
        self.queue.append(job)

    def next_job(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self):
        return len(self.queue) == 0
