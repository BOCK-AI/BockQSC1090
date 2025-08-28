"""
Quantum Processor Simulation and Analysis Suite
==============================================
This module provides comprehensive simulation and analysis tools for the 10-qubit
quantum processor, including electromagnetic simulation, circuit parameter extraction,
and quantum gate fidelity analysis.

Author: QPU Development Team
Date: August 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.linalg import expm
import json
import os

class QuantumProcessorSimulator:
    """Comprehensive quantum processor simulation class"""
    
    def __init__(self, config_file=None):
        """Initialize simulator with configuration"""
        
        # Default qubit parameters (can be loaded from config)
        self.qubit_params = {
            'frequency': [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9],  # GHz
            'anharmonicity': [-250e-3] * 10,  # GHz
            'T1': [100e-6] * 10,  # seconds
            'T2': [50e-6] * 10,   # seconds
            'readout_fidelity': [0.95] * 10
        }
        
        # Coupling matrix (MHz)
        self.coupling_matrix = np.zeros((10, 10))
        self._setup_coupling_network()
        
        # Gate parameters
        self.gate_params = {
            'single_qubit_time': 20e-9,    # 20 ns
            'two_qubit_time': 200e-9,      # 200 ns
            'readout_time': 1e-6,          # 1 μs
            'reset_time': 5e-6             # 5 μs
        }
        
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
            
    def _setup_coupling_network(self):
        """Setup nearest-neighbor coupling network"""
        
        # Coupling strengths (MHz)
        coupling_strength = 20.0  # 20 MHz
        
        # Horizontal couplings within rows
        horizontal_pairs = [(0,1), (1,2), (2,3), (3,4), (5,6), (6,7), (7,8), (8,9)]
        
        # Vertical couplings between rows  
        vertical_pairs = [(0,5), (1,6), (2,7), (3,8), (4,9)]
        
        # Set coupling matrix
        for i, j in horizontal_pairs + vertical_pairs:
            self.coupling_matrix[i][j] = coupling_strength
            self.coupling_matrix[j][i] = coupling_strength
            
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        # Update parameters from config
        if 'qubit_params' in config:
            self.qubit_params.update(config['qubit_params'])
        if 'gate_params' in config:
            self.gate_params.update(config['gate_params'])
            
        print(f"Configuration loaded from {config_file}")
        
    def calculate_circuit_parameters(self):
        """Calculate lumped element circuit parameters"""
        
        print("=== Circuit Parameter Analysis ===")
        
        # Calculate capacitance and inductance values
        results = {}
        
        for i in range(10):
            freq_01 = self.qubit_params['frequency'][i]  # GHz
            alpha = self.qubit_params['anharmonicity'][i]  # GHz
            
            # Transmon parameters
            Ec = -alpha  # Charging energy (GHz)
            Ej = (freq_01 + alpha)**2 / (8 * Ec)  # Josephson energy (GHz)
            
            # Convert to circuit elements
            C_total = 1.6e-19 / (2 * Ec * 1e9 * 6.626e-34)  # Total capacitance (F)
            L_j = 6.626e-34 / (2 * np.pi * 1.6e-19 * Ej * 1e9)  # Junction inductance (H)
            
            results[f'Q{i}'] = {
                'frequency_01': freq_01,
                'anharmonicity': alpha,
                'Ec_GHz': Ec,
                'Ej_GHz': Ej,
                'C_total_fF': C_total * 1e15,
                'L_junction_nH': L_j * 1e9
            }
            
        # Save results with UTF-8 encoding
        with open('circuit_parameters.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
        print("Circuit parameters calculated and saved")
        return results
        
    def simulate_single_qubit_gates(self):
        """Simulate single-qubit gate performance"""
        
        print("\n=== Single-Qubit Gate Simulation ===")
        
        # Define Pauli matrices
        sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        results = {}
        
        for i in range(10):
            qubit_results = {}
            
            # X gate (π rotation around X-axis)
            U_x = expm(-1j * np.pi/2 * sigma_x)
            
            # Y gate (π rotation around Y-axis)  
            U_y = expm(-1j * np.pi/2 * sigma_y)
            
            # Z gate (π rotation around Z-axis)
            U_z = expm(-1j * np.pi/2 * sigma_z)
            
            # Hadamard gate
            U_h = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
            
            # Calculate gate fidelities (simplified model)
            T1 = self.qubit_params['T1'][i]
            T2 = self.qubit_params['T2'][i]
            gate_time = self.gate_params['single_qubit_time']
            
            # Decoherence effects
            p_decay = 1 - np.exp(-gate_time / T1)
            p_dephase = 1 - np.exp(-gate_time / T2)
            
            # Gate fidelity (simplified)
            fidelity = 1 - 0.5 * (p_decay + p_dephase)
            
            qubit_results = {
                'X_gate_fidelity': fidelity,
                'Y_gate_fidelity': fidelity,
                'Z_gate_fidelity': fidelity + 0.01,  # Z gates typically higher fidelity
                'H_gate_fidelity': fidelity - 0.005,  # Composite gates slightly lower
                'gate_time_ns': gate_time * 1e9
            }
            
            results[f'Q{i}'] = qubit_results
            
        # Calculate average performance
        avg_fidelity = np.mean([results[f'Q{i}']['X_gate_fidelity'] for i in range(10)])
        
        print(f"Average single-qubit gate fidelity: {avg_fidelity:.4f}")
        
        # Save results
        with open('single_qubit_gates.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
        return results
        
    def simulate_two_qubit_gates(self):
        """Simulate two-qubit gate performance"""
        
        print("\n=== Two-Qubit Gate Simulation ===")
        
        results = {}
        
        # Get coupled qubit pairs
        coupled_pairs = []
        for i in range(10):
            for j in range(i+1, 10):
                if self.coupling_matrix[i][j] > 0:
                    coupled_pairs.append((i, j))
                    
        print(f"Found {len(coupled_pairs)} coupled qubit pairs")
        
        for i, j in coupled_pairs:
            # CNOT gate simulation
            coupling_strength = self.coupling_matrix[i][j]  # MHz
            gate_time = self.gate_params['two_qubit_time']
            
            # Calculate interaction strength
            chi = coupling_strength * 1e-3  # Convert to GHz
            
            # Gate fidelity model (simplified)
            T1_avg = (self.qubit_params['T1'][i] + self.qubit_params['T1'][j]) / 2
            T2_avg = (self.qubit_params['T2'][i] + self.qubit_params['T2'][j]) / 2
            
            # Decoherence during two-qubit gate
            p_decay = 1 - np.exp(-gate_time / T1_avg)
            p_dephase = 1 - np.exp(-gate_time / T2_avg)
            
            # Additional crosstalk and control errors
            p_crosstalk = 0.01  # 1% crosstalk error
            
            cnot_fidelity = 1 - 0.5 * (p_decay + p_dephase + p_crosstalk)
            
            gate_key = f'CNOT_Q{i}_Q{j}'
            results[gate_key] = {
                'fidelity': cnot_fidelity,
                'gate_time_ns': gate_time * 1e9,
                'coupling_MHz': coupling_strength,
                'control_qubit': i,
                'target_qubit': j
            }
            
        # Calculate average two-qubit gate fidelity
        avg_cnot_fidelity = np.mean([results[key]['fidelity'] for key in results])
        
        print(f"Average CNOT gate fidelity: {avg_cnot_fidelity:.4f}")
        
        # Save results
        with open('two_qubit_gates.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
        return results
        
    def simulate_readout_performance(self):
        """Simulate qubit readout performance"""
        
        print("\n=== Readout Performance Simulation ===")
        
        results = {}
        
        for i in range(10):
            # Readout parameters
            readout_fidelity = self.qubit_params['readout_fidelity'][i]
            readout_time = self.gate_params['readout_time']
            
            # Signal-to-noise ratio model
            freq_01 = self.qubit_params['frequency'][i]
            readout_freq = freq_01 + 1.0  # Dispersive readout, +1 GHz offset
            
            # Calculate measurement contrast
            chi_r = 1e-3  # 1 MHz dispersive shift
            contrast = 2 * chi_r / (0.1)  # Assume 100 kHz linewidth
            
            # Readout SNR and fidelity
            snr_db = 10 * np.log10(contrast)
            
            results[f'Q{i}'] = {
                'readout_fidelity': readout_fidelity,
                'readout_time_us': readout_time * 1e6,
                'readout_frequency_GHz': readout_freq,
                'dispersive_shift_MHz': chi_r * 1e3,
                'snr_db': snr_db,
                'contrast': contrast
            }
            
        # Calculate average readout fidelity
        avg_readout_fidelity = np.mean([results[f'Q{i}']['readout_fidelity'] for i in range(10)])
        
        print(f"Average readout fidelity: {avg_readout_fidelity:.4f}")
        
        # Save results
        with open('readout_performance.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
        return results
        
    def run_system_benchmarks(self):
        """Run comprehensive system benchmarks"""
        
        print("\n=== System Benchmark Analysis ===")
        
        # Run all simulations
        circuit_params = self.calculate_circuit_parameters()
        single_qubit_results = self.simulate_single_qubit_gates()
        two_qubit_results = self.simulate_two_qubit_gates()
        readout_results = self.simulate_readout_performance()
        
        # Compile benchmark report
        benchmark_report = {
            'system_overview': {
                'total_qubits': 10,
                'topology': '2x5 grid with nearest-neighbor coupling',
                'qubit_type': 'Transmon superconducting qubits'
            },
            'performance_summary': {
                'avg_single_qubit_fidelity': np.mean([single_qubit_results[f'Q{i}']['X_gate_fidelity'] for i in range(10)]),
                'avg_two_qubit_fidelity': np.mean([two_qubit_results[key]['fidelity'] for key in two_qubit_results]),
                'avg_readout_fidelity': np.mean([readout_results[f'Q{i}']['readout_fidelity'] for i in range(10)]),
                'avg_T1_us': np.mean(self.qubit_params['T1']) * 1e6,
                'avg_T2_us': np.mean(self.qubit_params['T2']) * 1e6
            },
            'quantum_volume': self._calculate_quantum_volume()
        }
        
        # Save benchmark report
        with open('system_benchmarks.json', 'w', encoding='utf-8') as f:
            json.dump(benchmark_report, f, indent=4)
            
        # Generate summary
        self._generate_benchmark_summary(benchmark_report)
        
        return benchmark_report
        
    def _calculate_quantum_volume(self):
        """Calculate quantum volume estimate"""
        
        # Simplified quantum volume calculation
        n_qubits = 10
        avg_gate_fidelity = 0.99  # Assume 99% average gate fidelity
        
        # Quantum volume = 2^d where d is maximum circuit depth
        # This is a simplified estimate
        max_depth = int(np.log2(n_qubits * avg_gate_fidelity * 10))
        quantum_volume = 2**max_depth
        
        return {
            'estimated_quantum_volume': quantum_volume,
            'max_circuit_depth': max_depth,
            'basis': 'Simplified model based on gate fidelities'
        }
        
    def _generate_benchmark_summary(self, benchmark_report):
        """Generate human-readable benchmark summary"""
        
        summary = f"""10-Qubit Quantum Processor Benchmark Summary
==========================================

System Configuration:
- Qubits: {benchmark_report['system_overview']['total_qubits']}
- Topology: {benchmark_report['system_overview']['topology']}
- Technology: {benchmark_report['system_overview']['qubit_type']}

Performance Metrics:
- Single-Qubit Gate Fidelity: {benchmark_report['performance_summary']['avg_single_qubit_fidelity']:.4f}
- Two-Qubit Gate Fidelity: {benchmark_report['performance_summary']['avg_two_qubit_fidelity']:.4f}  
- Readout Fidelity: {benchmark_report['performance_summary']['avg_readout_fidelity']:.4f}
- Average T1: {benchmark_report['performance_summary']['avg_T1_us']:.1f} microseconds
- Average T2: {benchmark_report['performance_summary']['avg_T2_us']:.1f} microseconds

Quantum Volume:
- Estimated QV: {benchmark_report['quantum_volume']['estimated_quantum_volume']}
- Max Circuit Depth: {benchmark_report['quantum_volume']['max_circuit_depth']}

Status: {'✓ PASS' if benchmark_report['performance_summary']['avg_single_qubit_fidelity'] > 0.99 else '⚠ NEEDS OPTIMIZATION'}
"""
        
        print(summary)
        
        # Save summary to file with UTF-8 encoding (FIXED)
        try:
            with open('benchmark_summary.txt', 'w', encoding='utf-8') as f:
                f.write(summary)
            print("✅ Summary saved to benchmark_summary.txt")
        except Exception as e:
            print(f"⚠️  Summary save warning: {e}")

def main():
    """Main simulation execution function"""
    
    print("=== Quantum Processor Simulation Suite ===\n")
    
    # Initialize simulator
    simulator = QuantumProcessorSimulator()
    
    # Run comprehensive benchmarks
    benchmark_results = simulator.run_system_benchmarks()
    
    print("\n=== Simulation Complete ===")
    print("Generated files:")
    print("- circuit_parameters.json")
    print("- single_qubit_gates.json") 
    print("- two_qubit_gates.json")
    print("- readout_performance.json")
    print("- system_benchmarks.json")
    print("- benchmark_summary.txt")
    
    return simulator

if __name__ == "__main__":
    simulator = main()
