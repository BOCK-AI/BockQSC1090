import subprocess
import sys
import os

def run(script):
    print(f"\n🔹 Running {script}...")
    try:
        result = subprocess.run([sys.executable, script], check=False)
        if result.returncode != 0:
            print(f"❌ {script} failed with exit code {result.returncode}")
            return False
        print(f"✅ Finished {script}")
        return True
    except Exception as e:
        print(f"❌ Error running {script}: {e}")
        return False

def main():
    print("\n🚀 Starting 10-Qubit Processor Pipeline...\n")

    steps = [
        "main_10qubit_design_stub.py",        # Stub design (good for local)
        "klayout_quantum_processor.py",       # REAL KLayout step (pya installed)
        "quantum_processor_simulation.py",    # Simulation
        "quantum_gates_stub.py",             # Stub gates (SciPy-free)
        "quantum_processor_verification.py"   # Verification
    ]

    for step in steps:
        if not os.path.exists(step):
            print(f"⚠️  Skipping missing script: {step}")
            continue

        ok = run(step)
        if not ok:
            print("\n⚠️ Pipeline stopped because of an error above.")
            return

    print("\n🎉 Pipeline completed successfully!\n")

if __name__ == "__main__":
    main()
