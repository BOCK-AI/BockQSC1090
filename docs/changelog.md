# Changelog

All notable changes to the BockQSC1090 project are documented here.

## [v1.0.0] - Handoff Release (June 2026)

### Added
- Comprehensive `docs/` directory detailing the entire software stack.
- Modern `setuptools` based `setup.py` and dedicated `scripts/setup_env.py`.

### Changed
- **Dependency Overhaul**: Removed deprecated `qiskit-metal` and unused dependencies (pandas, seaborn, plotly). Pinned modern versions of `numpy`, `matplotlib`, and `streamlit`.
- **Hardware Layer Migration**: Transitioned `main_10qubit_design.py` from the end-of-life `gdspy` library to the modern `gdstk` library, updating all geometric rendering APIs.
- **Pipeline Execution**: Replaced unsafe `os.system()` calls with `subprocess.run()` in `run_pipeline.py`.

### Fixed
- **CRITICAL**: Fixed a mathematical bug in `dashboard.py` where the `Z_GATE` was defined as the Identity matrix `[[1,0],[0,1]]` instead of `[[1,0],[0,-1]]`.
- **CRITICAL**: Fixed a `KeyError` crash in `pulse_engine/pulse_sequence.py` by properly parsing `control` and `target` keys for `CNOT` gates.
- Fixed a string formatting bug in `run_custom_algorithm.py` that caused measurement bitstrings to render incorrectly. Added missing qubit bounds checking (0-9).
- Repaired bare `except:` clauses causing silent failures in the dashboard data loaders.

---

## [Pre-v1.0.0] - Historic Milestones

### March 2026
- Integrated OS layer, Job system, and Big Algorithm pipeline into a cohesive flow.
- Added the SHA-256 quantum-inspired benchmark module.

### February 2026
- Initial implementation of the OS layer and Job layer (queue management).
- Created the Algorithm Blocks library and the Big Algorithm Engine for `.algo` parsing.
- Added exploratory Quantum Machine Learning (QML) scripts.

### December 2025
- Replaced initial software stubs with real implementations.
- Developed the Streamlit dashboard and custom algorithm execution engine.
- Integrated pulse execution and measurement translation.

### August 2025
- Initial upload of the repository.
- Created the 10-qubit GDS design generator and the verification/benchmarking framework.
