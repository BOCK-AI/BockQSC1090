#!/usr/bin/env python3
"""
Setup script for 10-Qubit Quantum Processor Development Package
"""

import os
import sys
import subprocess

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("⚠ Warning: Some requirements may have failed to install")
        print("Please manually install missing packages")

def create_output_directories():
    """Create necessary output directories"""
    directories = [
        "output",
        "fabrication_output", 
        "simulation_results",
        "verification_results",
        "logs"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_external_tools():
    """Check for external tool availability"""
    tools = {
        "klayout": "KLayout (required for physical design)",
        "hfss": "Ansys HFSS (optional for EM simulation)"
    }

    for tool, description in tools.items():
        try:
            result = subprocess.run([tool, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {description} found")
            else:
                print(f"⚠ {description} not found in PATH")
        except FileNotFoundError:
            print(f"⚠ {description} not found")

def main():
    """Main setup function"""
    print("=== 10-Qubit QPU Development Package Setup ===\n")

    # Check Python version
    check_python_version()

    # Install requirements
    install_requirements()

    # Create directories
    print("\nCreating output directories...")
    create_output_directories()

    # Check external tools
    print("\nChecking external tools...")
    check_external_tools()

    print("\n=== Setup Complete ===")
    print("\nTo get started:")
    print("1. cd qiskit_metal_designs")
    print("2. python main_10qubit_design.py")
    print("\nSee README.md for detailed usage instructions.")

if __name__ == "__main__":
    main()
