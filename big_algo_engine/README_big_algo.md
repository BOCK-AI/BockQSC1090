# Big Algorithm Engine

## Overview
Provides a structured way to run large algorithms using:
- Algorithm Blocks
- A Big Algorithm Compiler
- A Runner that sends output to the OS Layer

## Pipeline Stages
1. Build blocks
2. Compile blocks → gate list
3. Convert gates → pulses
4. Schedule pulses
5. Build waveforms
6. Execute pulses

## Files
- `block_builder.py`
- `big_algo_compiler.py`
- `algorithm_runner.py`
- `run_big_algorithm.py`

## How to Run
python big_algo_engine/run_big_algorithm.py