# Algorithm Blocks

## Overview
Algorithm Blocks are small, reusable quantum operations that help build
large circuits step-by-step instead of writing full circuits manually.

## Why Blocks?
- Clean structure
- Easy reuse
- Debug one part at a time
- Helps scale to larger algorithms

## Example Block
 {"name": "mix_layer",
 "gates": [
    {"gate": "H", "qubit": 0, "duration_ns": 20},
    {"gate": "X", "qubit": 1, "duration_ns": 20},
    {"gate": "CNOT", "control": 0, "target": 1, "duration_ns": 200},
    {"gate": "H", "qubit": 0, "duration_ns": 20}
 ]}
 ## Files
- block_builder.py