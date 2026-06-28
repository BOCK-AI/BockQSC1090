# Getting Started

This guide will help you install the BockQSC1090 package and run your first quantum pipeline.

## Prerequisites

- **Python**: Version 3.10 or higher is required.
- **Git**: For cloning the repository.
- **Virtual Environment** (Recommended): We strongly recommend using `venv` or `conda` to isolate the project dependencies.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BOCK-AI/BockQSC1090.git
   cd BockQSC1090
   ```

2. **Install the package in editable mode**:
   This will install all required dependencies (such as `numpy`, `streamlit`, `gdstk`, and `matplotlib`).
   ```bash
   pip install -e .
   ```

3. **Initialize the workspace**:
   The project requires several output directories to store generated GDS files, JSON reports, and logs. Run the setup script to create these:
   ```bash
   python scripts/setup_env.py
   ```
   *Expected Output:*
   ```text
   Setting up BockQSC1090 environment...
   Ensured directory exists: output/
   Ensured directory exists: fabrication_output/
   ...
   Environment setup complete.
   ```

## Running the End-to-End Pipeline

To verify that the installation was successful and to generate the baseline datasets required by the dashboard, run the main pipeline script. This script executes the hardware design, simulation, gate generation, and verification suites in sequence.

```bash
python run_pipeline.py
```

*Expected Output:*
The script will output progress logs as it moves through the stages. Upon completion, it will list the generated files, including `10qubit_processor_v1.gds`, `circuit_parameters.json`, and the verification summaries.

## Launching the Dashboard

Once the pipeline has generated the necessary data, you can explore the results interactively via the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

This will open a local web server (typically at `http://localhost:8501`) where you can:
- View the 10-qubit processor design metadata and qubit frequencies.
- Analyze simulated gate fidelities and randomized benchmarking results.
- Write and execute custom `.algo` quantum programs in the browser.
