# OS Layer

## Overview
The OS layer coordinates the full execution flow. It sits between the
compiler and the pulse engine and manages:

- circuit compilation
- gate → pulse conversion
- pulse scheduling
- waveform building
- pulse execution
- returning structured results

## Purpose
This layer gives the pipeline a structured “platform-like” behavior,
similar to early quantum control systems.

## Files
- `qpu_os.py`
- `run_qpu_os_demo.py`

## How to Test
python run_qpu_os_demo.py


## Output
You will see:
- compiled gates  
- generated pulses  
- scheduled timing  
- waveform creation  
- simulated execution