# Configuration

The `config/` directory manages system-wide variables and physical parameters. While some of these files are currently placeholder architectures intended for future expansion, they define the expected data structures for hardware integration.

## 1. `qubit_params.json`
Defines the baseline physical realities of the 10 transmons.
- **`frequency_ghz`**: The 0-1 transition frequency (typically 4.5 - 5.5 GHz).
- **`anharmonicity_mhz`**: The energy difference between the 1-2 and 0-1 transitions (typically ~ -220 MHz).
- **`T1_us`**: Relaxation time in microseconds.
- **`T2_us`**: Dephasing time in microseconds.
- **`coupling_strength_mhz`**: Capacitive coupling strength to nearest neighbors.

## 2. `system_config.json`
Defines operational parameters for the execution pipeline.
- **`backend`**: Identifies whether to use `"simulator"` or physical hardware.
- **`optimization_level`**: Targets for circuit depth reduction (e.g., 0-3).
- **`error_mitigation`**: Boolean flag for applying readout or gate mitigation strategies.
- **`shots`**: The number of statistical runs per circuit execution.

## 3. `calibration_schedule.json`
Outlines maintenance tasks required for physical hardware.
Defines routines such as `qubit_frequency_cal` and `T1_measurement`, specifying the required `interval_hours` between runs and tracking the `last_run` timestamp.

## 4. `config_loader.py`
A Python utility class (`ConfigLoader`) that provides a simple key-based interface for securely parsing and loading the JSON configuration files into Python dictionaries.

---

## API Reference: `config.py`

### Classes

#### `class QPUConfig`
No documentation provided.

