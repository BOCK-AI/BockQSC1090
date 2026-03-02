class BatchScheduler:
    def __init__(self, batch_size=2000):
        self.batch_size = batch_size

    def batch(self, scheduled_pulses):
        batches = []
        for i in range(0, len(scheduled_pulses), self.batch_size):
            batches.append(scheduled_pulses[i:i+self.batch_size])
        return batches