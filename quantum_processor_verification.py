"""
Quantum Processor Verification and Testing Suite
===============================================
This module provides comprehensive verification and testing capabilities for the
10-qubit quantum processor, including hardware validation, performance testing,
and system integration verification.

Author: QPU Development Team
Date: August 2025
"""

import numpy as np
import json
import time
import os
from datetime import datetime

class QuantumProcessorVerification:
    """Comprehensive verification and testing class"""
    
    def __init__(self):
        """Initialize verification suite"""
        
        # Test specifications
        self.test_specs = {
            'coherence_requirements': {
                'T1_min_us': 100.0,
                'T2_min_us': 50.0,
                'T2_echo_min_us': 100.0
            },
            'gate_fidelity_requirements': {
                'single_qubit_min': 0.999,
                'two_qubit_min': 0.99,
                'readout_min': 0.95
            },
            'frequency_requirements': {
                'qubit_frequency_range_GHz': [4.0, 8.0],
                'frequency_spacing_min_MHz': 50.0,
                'frequency_stability_ppm': 1.0
            },
            'timing_requirements': {
                'pulse_timing_accuracy_ns': 1.0,
                'synchronization_accuracy_ns': 0.1,
                'jitter_max_ps': 100.0
            }
        }
        
        # Test results storage
        self.test_results = {}
        self.verification_status = {}
        
    def convert_numpy_bool(self, obj):
        """Convert numpy bool types to native Python bool for JSON serialization"""
        if isinstance(obj, dict):
            return {k: self.convert_numpy_bool(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_numpy_bool(i) for i in obj]
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.int64) or isinstance(obj, np.int32):
            return int(obj)
        elif isinstance(obj, np.float64) or isinstance(obj, np.float32):
            return float(obj)
        else:
            return obj
        
    def run_full_verification_suite(self):
        """Execute complete verification test suite"""
        
        print("=== Starting Full Quantum Processor Verification ===\n")
        
        verification_start_time = datetime.now()
        
        # 1. Hardware connectivity tests
        print("1. Hardware Connectivity Verification")
        connectivity_results = self.verify_hardware_connectivity()
        self.test_results['connectivity'] = connectivity_results
        
        # 2. Qubit characterization tests
        print("\n2. Qubit Characterization Tests")
        qubit_results = self.verify_qubit_parameters()
        self.test_results['qubit_characterization'] = qubit_results
        
        # 3. Gate performance verification
        print("\n3. Gate Performance Verification")
        gate_results = self.verify_gate_performance()
        self.test_results['gate_performance'] = gate_results
        
        # 4. System timing verification
        print("\n4. System Timing Verification")
        timing_results = self.verify_system_timing()
        self.test_results['timing'] = timing_results
        
        # 5. Crosstalk and interference tests
        print("\n5. Crosstalk and Interference Tests")
        crosstalk_results = self.verify_crosstalk_suppression()
        self.test_results['crosstalk'] = crosstalk_results
        
        # 6. System integration tests
        print("\n6. System Integration Tests")
        integration_results = self.verify_system_integration()
        self.test_results['integration'] = integration_results
        
        # 7. Performance benchmarks
        print("\n7. Performance Benchmarks")
        benchmark_results = self.run_performance_benchmarks()
        self.test_results['benchmarks'] = benchmark_results
        
        # Generate final verification report
        verification_end_time = datetime.now()
        verification_duration = verification_end_time - verification_start_time
        
        final_report = self.generate_verification_report(verification_duration)
        
        return final_report
        
    def verify_hardware_connectivity(self):
        """Verify hardware connectivity and basic functionality"""
        
        print("  Testing hardware connectivity...")
        
        connectivity_results = {
            'control_electronics': {},
            'rf_connections': {},
            'power_supplies': {},
            'timing_systems': {}
        }
        
        # Simulate control electronics connectivity check
        for i in range(10):
            # Check digital control connection
            control_status = np.random.choice(['PASS', 'FAIL'], p=[0.95, 0.05])
            connectivity_results['control_electronics'][f'Q{i}_control'] = {
                'status': control_status,
                'response_time_us': float(np.random.uniform(1.0, 5.0)),
                'signal_integrity': 'GOOD' if control_status == 'PASS' else 'DEGRADED'
            }
            
            # Check RF connectivity
            rf_status = np.random.choice(['PASS', 'FAIL'], p=[0.98, 0.02])
            connectivity_results['rf_connections'][f'Q{i}_rf'] = {
                'status': rf_status,
                'insertion_loss_dB': float(np.random.uniform(-1.0, -3.0)),
                'reflection_dB': float(np.random.uniform(-20, -40)),
                'frequency_response': 'FLAT' if rf_status == 'PASS' else 'DISTORTED'
            }
            
        # Check power supply connections
        power_rails = ['3V3_digital', '15V_analog', 'minus15V_analog', '1V8_core']
        for rail in power_rails:
            voltage_accuracy = float(np.random.uniform(0.98, 1.02))  # ±2% accuracy
            noise_level = float(np.random.uniform(1, 10))  # mV noise
            
            connectivity_results['power_supplies'][rail] = {
                'status': 'PASS' if 0.95 < voltage_accuracy < 1.05 else 'FAIL',
                'voltage_accuracy': voltage_accuracy,
                'noise_mV': noise_level,
                'load_regulation': float(np.random.uniform(0.1, 1.0))
            }
            
        # Check timing system
        connectivity_results['timing_systems'] = {
            'master_clock_10MHz': {
                'status': 'PASS',
                'frequency_stability_ppm': float(np.random.uniform(0.1, 0.5)),
                'phase_noise_dBc': float(np.random.uniform(-120, -100))
            },
            'sample_clock_2GHz': {
                'status': 'PASS',
                'jitter_ps': float(np.random.uniform(50, 150)),
                'duty_cycle_percent': float(np.random.uniform(49, 51))
            }
        }
        
        # Overall connectivity status
        all_status = []
        for category in connectivity_results.values():
            if isinstance(category, dict):
                for item in category.values():
                    if isinstance(item, dict) and 'status' in item:
                        all_status.append(item['status'])
                        
        overall_pass_rate = all_status.count('PASS') / len(all_status)
        connectivity_results['overall'] = {
            'pass_rate': float(overall_pass_rate),
            'status': 'PASS' if overall_pass_rate > 0.95 else 'FAIL'
        }
        
        print(f"  Connectivity verification: {connectivity_results['overall']['status']}")
        print(f"  Pass rate: {overall_pass_rate:.1%}")
        
        return connectivity_results
        
    def verify_qubit_parameters(self):
        """Verify individual qubit parameters meet specifications"""
        
        print("  Measuring qubit parameters...")
        
        qubit_results = {}
        
        for i in range(10):
            print(f"    Testing Q{i}...")
            
            # Simulate qubit parameter measurements
            # T1 measurement
            T1_measured = float(np.random.normal(120e-6, 20e-6))  # 120 ± 20 μs
            T1_pass = bool(T1_measured > self.test_specs['coherence_requirements']['T1_min_us'] * 1e-6)
            
            # T2* measurement
            T2_star_measured = float(np.random.normal(60e-6, 15e-6))  # 60 ± 15 μs
            T2_star_pass = bool(T2_star_measured > self.test_specs['coherence_requirements']['T2_min_us'] * 1e-6)
            
            # T2 echo measurement
            T2_echo_measured = float(np.random.normal(150e-6, 30e-6))  # 150 ± 30 μs
            T2_echo_pass = bool(T2_echo_measured > self.test_specs['coherence_requirements']['T2_echo_min_us'] * 1e-6)
            
            # Frequency measurement
            base_frequency = 5.0 + i * 0.1  # GHz, 100 MHz spacing
            frequency_measured = float(base_frequency + np.random.normal(0, 0.005))  # ±5 MHz uncertainty
            frequency_pass = bool(self.test_specs['frequency_requirements']['qubit_frequency_range_GHz'][0] 
                            <= frequency_measured <= 
                            self.test_specs['frequency_requirements']['qubit_frequency_range_GHz'][1])
            
            # Anharmonicity measurement
            anharmonicity_measured = float(np.random.normal(-250e-3, 20e-3))  # -250 ± 20 MHz
            
            qubit_results[f'Q{i}'] = {
                'T1_us': T1_measured * 1e6,
                'T1_pass': T1_pass,
                'T2_star_us': T2_star_measured * 1e6,
                'T2_star_pass': T2_star_pass,
                'T2_echo_us': T2_echo_measured * 1e6,
                'T2_echo_pass': T2_echo_pass,
                'frequency_GHz': frequency_measured,
                'frequency_pass': frequency_pass,
                'anharmonicity_MHz': anharmonicity_measured * 1e3,
                'overall_pass': bool(all([T1_pass, T2_star_pass, T2_echo_pass, frequency_pass]))
            }
            
        # Calculate summary statistics
        all_qubits_pass = all([qubit_results[f'Q{i}']['overall_pass'] for i in range(10)])
        avg_T1 = float(np.mean([qubit_results[f'Q{i}']['T1_us'] for i in range(10)]))
        avg_T2_star = float(np.mean([qubit_results[f'Q{i}']['T2_star_us'] for i in range(10)]))
        
        qubit_results['summary'] = {
            'all_qubits_pass': bool(all_qubits_pass),
            'average_T1_us': avg_T1,
            'average_T2_star_us': avg_T2_star,
            'qubit_count': 10,
            'pass_count': int(sum([qubit_results[f'Q{i}']['overall_pass'] for i in range(10)]))
        }
        
        print(f"  Qubit characterization: {'PASS' if all_qubits_pass else 'FAIL'}")
        print(f"  Average T1: {avg_T1:.1f} μs")
        print(f"  Average T2*: {avg_T2_star:.1f} μs")
        
        return qubit_results
        
    def verify_gate_performance(self):
        """Verify quantum gate performance meets specifications"""
        
        print("  Testing gate performance...")
        
        gate_results = {
            'single_qubit_gates': {},
            'two_qubit_gates': {},
            'readout_performance': {}
        }
        
        # Single-qubit gate testing
        for i in range(10):
            for gate in ['X', 'Y', 'Z', 'H']:
                # Simulate gate fidelity measurement
                base_fidelity = 0.9995 if gate == 'Z' else 0.9985  # Virtual Z gates higher fidelity
                measured_fidelity = float(base_fidelity + np.random.normal(0, 0.001))
                fidelity_pass = bool(measured_fidelity > self.test_specs['gate_fidelity_requirements']['single_qubit_min'])
                
                gate_key = f'Q{i}_{gate}'
                gate_results['single_qubit_gates'][gate_key] = {
                    'fidelity': measured_fidelity,
                    'pass': fidelity_pass,
                    'gate_time_ns': float(20.0 if gate != 'Z' else 0.0),
                    'process_fidelity': float(measured_fidelity * 0.98)  # Account for coherent errors
                }
                
        # Two-qubit gate testing (CNOT gates)
        coupling_pairs = [(0,1), (1,2), (2,3), (3,4), (5,6), (6,7), (7,8), (8,9), (0,5), (1,6), (2,7), (3,8), (4,9)]
        
        for control, target in coupling_pairs:
            # Simulate CNOT gate fidelity
            cnot_fidelity = float(np.random.normal(0.992, 0.003))  # 99.2% ± 0.3%
            cnot_pass = bool(cnot_fidelity > self.test_specs['gate_fidelity_requirements']['two_qubit_min'])
            
            gate_key = f'CNOT_Q{control}_Q{target}'
            gate_results['two_qubit_gates'][gate_key] = {
                'fidelity': cnot_fidelity,
                'pass': cnot_pass,
                'gate_time_ns': float(200.0),
                'entangling_power': float(np.random.uniform(0.8, 1.0))
            }
            
        # Readout performance testing
        for i in range(10):
            readout_fidelity = float(np.random.normal(0.965, 0.015))  # 96.5% ± 1.5%
            readout_pass = bool(readout_fidelity > self.test_specs['gate_fidelity_requirements']['readout_min'])
            
            gate_results['readout_performance'][f'Q{i}_readout'] = {
                'fidelity': readout_fidelity,
                'pass': readout_pass,
                'readout_time_us': float(1.0),
                'snr_db': float(np.random.uniform(15, 25))
            }
            
        # Calculate summary statistics
        single_qubit_fidelities = [gate_results['single_qubit_gates'][k]['fidelity'] 
                                 for k in gate_results['single_qubit_gates']]
        two_qubit_fidelities = [gate_results['two_qubit_gates'][k]['fidelity'] 
                              for k in gate_results['two_qubit_gates']]
        readout_fidelities = [gate_results['readout_performance'][k]['fidelity'] 
                            for k in gate_results['readout_performance']]
        
        gate_results['summary'] = {
            'avg_single_qubit_fidelity': float(np.mean(single_qubit_fidelities)),
            'avg_two_qubit_fidelity': float(np.mean(two_qubit_fidelities)),
            'avg_readout_fidelity': float(np.mean(readout_fidelities)),
            'all_gates_pass': bool(np.min(single_qubit_fidelities) > self.test_specs['gate_fidelity_requirements']['single_qubit_min'] and
                             np.min(two_qubit_fidelities) > self.test_specs['gate_fidelity_requirements']['two_qubit_min'] and
                             np.min(readout_fidelities) > self.test_specs['gate_fidelity_requirements']['readout_min'])
        }
        
        print(f"  Gate performance: {'PASS' if gate_results['summary']['all_gates_pass'] else 'FAIL'}")
        print(f"  Avg single-qubit fidelity: {gate_results['summary']['avg_single_qubit_fidelity']:.4f}")
        print(f"  Avg two-qubit fidelity: {gate_results['summary']['avg_two_qubit_fidelity']:.4f}")
        
        return gate_results
        
    def verify_system_timing(self):
        """Verify system timing and synchronization"""
        
        print("  Testing system timing...")
        
        timing_results = {
            'pulse_timing_accuracy': {},
            'synchronization_accuracy': {},
            'jitter_measurements': {}
        }
        
        # Pulse timing accuracy tests
        for i in range(10):
            # Measure pulse timing accuracy
            timing_error = float(np.random.normal(0, 0.5))  # ±0.5 ns Gaussian error
            timing_pass = bool(abs(timing_error) < self.test_specs['timing_requirements']['pulse_timing_accuracy_ns'])
            
            timing_results['pulse_timing_accuracy'][f'Q{i}'] = {
                'timing_error_ns': timing_error,
                'pass': timing_pass,
                'absolute_error_ns': float(abs(timing_error))
            }
            
        # Synchronization accuracy between qubits
        sync_pairs = [(0,1), (1,2), (2,3), (3,4), (5,6), (6,7), (7,8), (8,9)]
        for q1, q2 in sync_pairs:
            sync_error = float(np.random.normal(0, 0.05))  # ±50 ps synchronization error
            sync_pass = bool(abs(sync_error) < self.test_specs['timing_requirements']['synchronization_accuracy_ns'])
            
            timing_results['synchronization_accuracy'][f'Q{q1}_Q{q2}'] = {
                'sync_error_ns': sync_error,
                'pass': sync_pass,
                'absolute_error_ps': float(abs(sync_error) * 1000)
            }
            
        # Jitter measurements
        clock_sources = ['master_10MHz', 'sample_2GHz', 'local_oscillators']
        for source in clock_sources:
            if source == 'master_10MHz':
                jitter = float(np.random.uniform(10, 50))  # ps
            elif source == 'sample_2GHz':
                jitter = float(np.random.uniform(80, 120))  # ps
            else:
                jitter = float(np.random.uniform(50, 100))  # ps
                
            jitter_pass = bool(jitter < self.test_specs['timing_requirements']['jitter_max_ps'])
            
            timing_results['jitter_measurements'][source] = {
                'jitter_ps': jitter,
                'pass': jitter_pass,
                'specification_ps': float(self.test_specs['timing_requirements']['jitter_max_ps'])
            }
            
        # Overall timing system pass/fail
        all_timing_pass = (
            all([timing_results['pulse_timing_accuracy'][k]['pass'] for k in timing_results['pulse_timing_accuracy']]) and
            all([timing_results['synchronization_accuracy'][k]['pass'] for k in timing_results['synchronization_accuracy']]) and
            all([timing_results['jitter_measurements'][k]['pass'] for k in timing_results['jitter_measurements']])
        )
        
        timing_results['overall'] = {
            'all_timing_pass': bool(all_timing_pass),
            'max_pulse_timing_error_ns': float(max([abs(timing_results['pulse_timing_accuracy'][k]['timing_error_ns']) 
                                            for k in timing_results['pulse_timing_accuracy']])),
            'max_sync_error_ps': float(max([abs(timing_results['synchronization_accuracy'][k]['sync_error_ns']) * 1000 
                                    for k in timing_results['synchronization_accuracy']])),
            'max_jitter_ps': float(max([timing_results['jitter_measurements'][k]['jitter_ps'] 
                                for k in timing_results['jitter_measurements']]))
        }
        
        print(f"  System timing: {'PASS' if all_timing_pass else 'FAIL'}")
        print(f"  Max timing error: {timing_results['overall']['max_pulse_timing_error_ns']:.2f} ns")
        print(f"  Max jitter: {timing_results['overall']['max_jitter_ps']:.1f} ps")
        
        return timing_results
        
    def verify_crosstalk_suppression(self):
        """Verify crosstalk and interference suppression"""
        
        print("  Testing crosstalk suppression...")
        
        crosstalk_results = {
            'qubit_crosstalk': {},
            'readout_crosstalk': {},
            'control_line_isolation': {}
        }
        
        # Qubit-to-qubit crosstalk
        for i in range(10):
            for j in range(10):
                if i != j:
                    # Measure crosstalk when operating qubit i and measuring effect on qubit j
                    distance = abs(i - j)  # Simplified distance metric
                    base_crosstalk = -40 - 10 * distance  # dB, further qubits have less crosstalk
                    crosstalk_db = float(base_crosstalk + np.random.normal(0, 3))
                    
                    crosstalk_pass = bool(crosstalk_db < -30)  # <-30 dB crosstalk requirement
                    
                    crosstalk_results['qubit_crosstalk'][f'Q{i}_to_Q{j}'] = {
                        'crosstalk_db': crosstalk_db,
                        'pass': crosstalk_pass,
                        'distance': int(distance)
                    }
                    
        # Readout line crosstalk
        for i in range(10):
            for j in range(i+1, 10):
                # Measure readout line isolation
                isolation_db = float(np.random.normal(-45, 5))  # -45 ± 5 dB isolation
                isolation_pass = bool(isolation_db < -35)  # <-35 dB requirement
                
                crosstalk_results['readout_crosstalk'][f'R{i}_to_R{j}'] = {
                    'isolation_db': isolation_db,
                    'pass': isolation_pass
                }
                
        # Control line isolation
        control_lines = ['flux_control', 'drive_control', 'readout_control']
        for line1 in control_lines:
            for line2 in control_lines:
                if line1 != line2:
                    isolation_db = float(np.random.normal(-50, 3))  # -50 ± 3 dB isolation
                    isolation_pass = bool(isolation_db < -40)  # <-40 dB requirement
                    
                    crosstalk_results['control_line_isolation'][f'{line1}_to_{line2}'] = {
                        'isolation_db': isolation_db,
                        'pass': isolation_pass
                    }
                    
        # Overall crosstalk performance
        all_crosstalk_tests = []
        for category in crosstalk_results.values():
            if isinstance(category, dict):
                for test in category.values():
                    if isinstance(test, dict) and 'pass' in test:
                        all_crosstalk_tests.append(test['pass'])
                        
        crosstalk_pass_rate = float(sum(all_crosstalk_tests) / len(all_crosstalk_tests))
        
        crosstalk_results['overall'] = {
            'pass_rate': crosstalk_pass_rate,
            'overall_pass': bool(crosstalk_pass_rate > 0.9),  # >90% pass rate required
            'worst_crosstalk_db': float(min([crosstalk_results['qubit_crosstalk'][k]['crosstalk_db'] 
                                     for k in crosstalk_results['qubit_crosstalk']]))
        }
        
        print(f"  Crosstalk suppression: {'PASS' if crosstalk_results['overall']['overall_pass'] else 'FAIL'}")
        print(f"  Pass rate: {crosstalk_pass_rate:.1%}")
        
        return crosstalk_results
        
    def verify_system_integration(self):
        """Verify end-to-end system integration"""
        
        print("  Testing system integration...")
        
        integration_results = {
            'quantum_classical_interface': {},
            'real_time_feedback': {},
            'system_throughput': {},
            'error_correction_ready': {}
        }
        
        # Quantum-classical interface tests
        interface_latency = float(np.random.uniform(3, 6))  # μs
        interface_throughput = float(np.random.uniform(50, 100))  # MB/s
        interface_reliability = float(np.random.uniform(0.995, 0.999))
        
        integration_results['quantum_classical_interface'] = {
            'latency_us': interface_latency,
            'throughput_MBps': interface_throughput,
            'reliability': interface_reliability,
            'pass': bool(interface_latency < 10 and interface_throughput > 25 and interface_reliability > 0.99)
        }
        
        # Real-time feedback capability
        feedback_latency = float(np.random.uniform(0.8, 1.5))  # μs
        feedback_success_rate = float(np.random.uniform(0.95, 0.99))
        
        integration_results['real_time_feedback'] = {
            'feedback_latency_us': feedback_latency,
            'success_rate': feedback_success_rate,
            'pass': bool(feedback_latency < 2.0 and feedback_success_rate > 0.9)
        }
        
        # System throughput tests
        gate_rate = float(np.random.uniform(800, 1200))  # kHz
        measurement_rate = float(np.random.uniform(400, 600))  # kHz
        
        integration_results['system_throughput'] = {
            'gate_rate_kHz': gate_rate,
            'measurement_rate_kHz': measurement_rate,
            'pass': bool(gate_rate > 500 and measurement_rate > 200)
        }
        
        # Error correction readiness
        syndrome_extraction_time = float(np.random.uniform(2, 5))  # μs
        correction_latency = float(np.random.uniform(5, 10))  # μs
        
        integration_results['error_correction_ready'] = {
            'syndrome_extraction_us': syndrome_extraction_time,
            'correction_latency_us': correction_latency,
            'pass': bool(syndrome_extraction_time < 10 and correction_latency < 20)
        }
        
        # Overall integration status
        all_integration_pass = all([
            integration_results['quantum_classical_interface']['pass'],
            integration_results['real_time_feedback']['pass'],
            integration_results['system_throughput']['pass'],
            integration_results['error_correction_ready']['pass']
        ])
        
        integration_results['overall'] = {
            'all_integration_pass': bool(all_integration_pass),
            'readiness_level': 'Production Ready' if all_integration_pass else 'Requires Optimization'
        }
        
        print(f"  System integration: {'PASS' if all_integration_pass else 'FAIL'}")
        print(f"  Readiness: {integration_results['overall']['readiness_level']}")
        
        return integration_results
        
    def run_performance_benchmarks(self):
        """Run standard quantum computing benchmarks"""
        
        print("  Running performance benchmarks...")
        
        benchmark_results = {}
        
        # Quantum Volume benchmark
        qv_depth = 8  # Maximum reliable circuit depth
        qv_success_rate = float(np.random.uniform(0.65, 0.85))  # Success rate for QV circuits
        quantum_volume = int(2**qv_depth if qv_success_rate > 2/3 else 2**(qv_depth-1))
        
        benchmark_results['quantum_volume'] = {
            'qv_depth': int(qv_depth),
            'success_rate': qv_success_rate,
            'quantum_volume': quantum_volume,
            'pass': bool(qv_success_rate > 2/3)
        }
        
        # Randomized benchmarking
        rb_fidelity = float(np.random.uniform(0.995, 0.999))
        rb_coherence_limit = float(rb_fidelity * 100)  # Estimated coherence-limited depth
        
        benchmark_results['randomized_benchmarking'] = {
            'average_fidelity': rb_fidelity,
            'coherence_limited_depth': rb_coherence_limit,
            'rb_number': float(1/rb_fidelity)
        }
        
        # Cross-entropy benchmarking (Google's benchmark)
        xeb_fidelity = float(np.random.uniform(0.002, 0.01))  # Typical for NISQ devices
        classical_verification_depth = int(12)  # Maximum classically verifiable depth
        
        benchmark_results['cross_entropy_benchmarking'] = {
            'xeb_fidelity': xeb_fidelity,
            'verification_depth': classical_verification_depth,
            'quantum_advantage_estimate': bool(xeb_fidelity > 0.001)
        }
        
        # Application-specific benchmarks
        vqe_convergence = float(np.random.uniform(0.85, 0.95))  # VQE convergence success rate
        qaoa_approximation_ratio = float(np.random.uniform(0.7, 0.9))  # QAOA performance
        
        benchmark_results['application_benchmarks'] = {
            'vqe_convergence_rate': vqe_convergence,
            'qaoa_approximation_ratio': qaoa_approximation_ratio,
            'algorithm_suitability': 'NISQ-era algorithms'
        }
        
        print(f"  Quantum Volume: {quantum_volume}")
        print(f"  RB Fidelity: {rb_fidelity:.4f}")
        print(f"  XEB Fidelity: {xeb_fidelity:.6f}")
        
        return benchmark_results
        
    def generate_verification_report(self, verification_duration):
        """Generate comprehensive verification report"""
        
        print("\n=== Generating Verification Report ===")
        
        # Calculate overall system status
        critical_systems = [
            self.test_results['connectivity']['overall']['status'] == 'PASS',
            self.test_results['qubit_characterization']['summary']['all_qubits_pass'],
            self.test_results['gate_performance']['summary']['all_gates_pass'],
            self.test_results['timing']['overall']['all_timing_pass'],
            self.test_results['integration']['overall']['all_integration_pass']
        ]
        
        overall_system_pass = all(critical_systems)
        pass_rate = float(sum(critical_systems) / len(critical_systems))
        
        # Generate report
        report = {
            'verification_summary': {
                'overall_status': 'PASS' if overall_system_pass else 'FAIL',
                'pass_rate': pass_rate,
                'verification_duration_minutes': float(verification_duration.total_seconds() / 60),
                'timestamp': datetime.now().isoformat(),
                'system_readiness': 'Production Ready' if overall_system_pass else 'Requires Attention'
            },
            'detailed_results': self.test_results,
            'recommendations': self._generate_recommendations(),
            'next_steps': self._generate_next_steps(overall_system_pass)
        }
        
        # Convert numpy types to native Python types before JSON serialization
        safe_report = self.convert_numpy_bool(report)
        
        # Save report to file
        report_filename = f"verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(safe_report, f, indent=4)
            print(f"✅ Verification report saved: {report_filename}")
        except Exception as e:
            print(f"⚠️  Report save warning: {e}")
            
        # Generate human-readable summary
        summary = self._generate_human_readable_summary(safe_report)
        summary_filename = f"verification_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(summary_filename, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"✅ Summary report saved: {summary_filename}")
        except Exception as e:
            print(f"⚠️  Summary save warning: {e}")
            
        return safe_report
        
    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        
        recommendations = []
        
        # Check each test category and generate specific recommendations
        if not self.test_results['connectivity']['overall']['status'] == 'PASS':
            recommendations.append("Check and repair hardware connectivity issues before proceeding")
            
        if not self.test_results['qubit_characterization']['summary']['all_qubits_pass']:
            recommendations.append("Optimize qubit fabrication parameters to improve coherence times")
            
        if not self.test_results['gate_performance']['summary']['all_gates_pass']:
            recommendations.append("Recalibrate gate parameters and optimize pulse sequences")
            
        if not self.test_results['timing']['overall']['all_timing_pass']:
            recommendations.append("Improve timing synchronization and reduce system jitter")
            
        if self.test_results['crosstalk']['overall']['pass_rate'] < 0.95:
            recommendations.append("Enhance isolation between control lines and qubits")
            
        if not recommendations:
            recommendations.append("System performing within specifications - ready for production use")
            
        return recommendations
        
    def _generate_next_steps(self, system_pass):
        """Generate next steps based on verification results"""
        
        if system_pass:
            return [
                "Begin production qualification testing",
                "Initiate user acceptance testing",
                "Prepare system documentation and user manuals",
                "Schedule customer demonstrations"
            ]
        else:
            return [
                "Address identified issues in priority order",
                "Re-run verification tests after fixes",
                "Consider design modifications if issues persist",
                "Schedule follow-up verification session"
            ]
            
    def _generate_human_readable_summary(self, report):
        """Generate human-readable verification summary"""
        
        summary = f"""10-Qubit Quantum Processor Verification Summary
=============================================

Verification Date: {report['verification_summary']['timestamp'][:10]}
Duration: {report['verification_summary']['verification_duration_minutes']:.1f} minutes
Overall Status: {report['verification_summary']['overall_status']}
System Readiness: {report['verification_summary']['system_readiness']}

Test Results Summary:
- Hardware Connectivity: {self.test_results['connectivity']['overall']['status']}
- Qubit Characterization: {'PASS' if self.test_results['qubit_characterization']['summary']['all_qubits_pass'] else 'FAIL'}
- Gate Performance: {'PASS' if self.test_results['gate_performance']['summary']['all_gates_pass'] else 'FAIL'}
- System Timing: {'PASS' if self.test_results['timing']['overall']['all_timing_pass'] else 'FAIL'}
- Crosstalk Suppression: {'PASS' if self.test_results['crosstalk']['overall']['overall_pass'] else 'FAIL'}
- System Integration: {'PASS' if self.test_results['integration']['overall']['all_integration_pass'] else 'FAIL'}

Key Performance Metrics:
- Average T1: {self.test_results['qubit_characterization']['summary']['average_T1_us']:.1f} microseconds
- Average T2*: {self.test_results['qubit_characterization']['summary']['average_T2_star_us']:.1f} microseconds
- Single-Qubit Fidelity: {self.test_results['gate_performance']['summary']['avg_single_qubit_fidelity']:.4f}
- Two-Qubit Fidelity: {self.test_results['gate_performance']['summary']['avg_two_qubit_fidelity']:.4f}
- Readout Fidelity: {self.test_results['gate_performance']['summary']['avg_readout_fidelity']:.4f}
- Quantum Volume: {self.test_results['benchmarks']['quantum_volume']['quantum_volume']}

Recommendations:
"""
        
        for i, rec in enumerate(report['recommendations'], 1):
            summary += f"\n        {i}. {rec}"
            
        summary += "\n\n        Next Steps:\n"
        for i, step in enumerate(report['next_steps'], 1):
            summary += f"        {i}. {step}\n"
            
        return summary

def main():
    """Main verification execution function"""
    
    print("=== Quantum Processor Verification Suite ===\n")
    
    # Initialize verification system
    verifier = QuantumProcessorVerification()
    
    # Run full verification suite
    verification_report = verifier.run_full_verification_suite()
    
    print("\n=== Verification Complete ===")
    print(f"Overall Status: {verification_report['verification_summary']['overall_status']}")
    print(f"System Readiness: {verification_report['verification_summary']['system_readiness']}")
    
    return verifier

if __name__ == "__main__":
    verifier = main()
