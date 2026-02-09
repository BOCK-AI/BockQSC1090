# Job Layer

## Overview
The Job Layer introduces an industry-style job submission model. Instead of
running circuits directly, a circuit is wrapped inside a "job" object and
moved through simple lifecycle states.

This makes the system closer to real QPU platforms, which all use job-based
execution (IBM, Rigetti, Quantinuum, AWS Braket).

## What a Job Does
A job contains:
- a unique job ID
- submitted circuit text
- timestamps for each stage
- lifecycle states (created → compiled → scheduled → executed)

The job object moves across the system instead of raw circuits.

## Files
Inside the `job_layer/` folder:
- `job.py` – defines the Job object (id, circuit, timestamps, states)
- `job_manager.py` – very small manager for creating and updating jobs

At the project root:
- `run_job_demo.py` – simple script to show job creation and state transitions

## Why It Exists
- provides structure for future queueing/batching
- adds traceability
- improves clarity when integrating OS layer & big algorithms

## How to Test
Run the demo:
python run_job_demo.py


Expected:
- job created
- job states updated (created → compiled → executed)
- printed job summary