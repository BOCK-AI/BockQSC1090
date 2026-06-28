# Job Layer

The Job Layer (`job_layer/`) provides a robust queuing system for managing quantum workloads. Because quantum processors are scarce, single-threaded resources, circuits cannot be executed simultaneously; they must be queued, prioritized, and executed sequentially.

## Components

### `Job` Object (`job.py`)
Every submitted circuit is wrapped in a `Job` dataclass. A job possesses:
- A unique UUID (`id`).
- The source `circuit` string.
- A `status` tracking its lifecycle (`CREATED`, `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`).
- Timestamps for submission and completion.
- The final execution `result`.

### `JobQueue` and `JobStore`
- **`JobQueue`**: A FIFO queue (using `collections.deque`) that holds jobs awaiting execution.
- **`JobStore`**: An in-memory dictionary that stores the canonical state of all jobs, allowing for fast retrieval by UUID.

### `JobManager` (`job_manager.py`)
The `JobManager` is the primary interface for this layer. It accepts incoming circuit strings, wraps them in `Job` objects, and places them in the queue. 

**Key Methods:**
- `submit_job(circuit_str)`: Creates and queues a new job, returning the UUID.
- `run_next()`: Pops the oldest job from the queue, passes it to the `QPUOS` for execution, updates the job's status to `COMPLETED`, and stores the result.
- `get_status(job_id)`: Retrieves the current status and results of a specific job.

## Usage Example

```python
from qpu_os import QPUOS
from job_layer.job_manager import JobManager

# Initialize dependencies...
os_layer = QPUOS(gate_engine, scheduler, executor)
manager = JobManager(os_layer)

# Asynchronous submission
job_id = manager.submit_job("H(0); X(1)")

# Process queue
finished_id, result = manager.run_next()
print(f"Job {finished_id} finished with result: {result}")
```

---

## API Reference: `job.py`

### Classes

#### `class Job`
No documentation provided.

**Methods:**

- **`__init__(self, circuit)`**: No documentation provided.
- **`set_status(self, status)`**: No documentation provided.
- **`set_result(self, result)`**: No documentation provided.


---

## API Reference: `job_manager.py`

### Classes

#### `class JobManager`
No documentation provided.

**Methods:**

- **`__init__(self, os_layer)`**: No documentation provided.
- **`submit_job(self, circuit)`**: No documentation provided.
- **`run_next(self)`**: Minimal job execution:
- **`get_status(self, job_id)`**: No documentation provided.
- **`get_result(self, job_id)`**: No documentation provided.
- **`list_jobs(self)`**: No documentation provided.


---

## API Reference: `job_queue.py`

### Classes

#### `class JobQueue`
No documentation provided.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`submit(self, job)`**: No documentation provided.
- **`next_job(self)`**: No documentation provided.
- **`is_empty(self)`**: No documentation provided.


---

## API Reference: `job_store.py`

### Classes

#### `class JobStore`
No documentation provided.

**Methods:**

- **`__init__(self)`**: No documentation provided.
- **`add(self, job)`**: No documentation provided.
- **`get(self, job_id)`**: No documentation provided.
- **`update(self, job)`**: No documentation provided.

