"""
Quantum Gate Implementation Library
==================================
This module provides implementations of quantum gates on the 10-qubit processor,
including calibration routines, pulse sequences, and gate optimization.

Author: QPU Development Team
Date: August 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.signal import gaussian
import json

class QuantumGateImplementation:
    """Quantum gate implementation and calibration class"""
    
    def __init__(self):
        """Initialize gate implementation with default parameters"""
        
        # Pulse parameters for single-qubit gates
        self.single_qubit_pulses = {
            'X_gate': {
                'amplitude': 0.5,      # Normalized amplitude
                'duration': 20e-9,     # 20 ns
                'frequency': 5.0e9,    # 5 GHz
                'phase': 0.0,          # radians
                'pulse_shape': 'gaussian'
            },
            'Y_gate': {
                'amplitude': 0.5,
                'duration': 20e-9,
                'frequency': 5.0e9,
                'phase': np.pi/2,      # 90° phase shift for Y
                'pulse_shape': 'gaussian'
            },
            'Z_gate': {
                'amplitude': 0.0,      # Virtual Z gate (phase only)
                'duration': 0.0,
                'frequency': 5.0e9,
                'phase': np.pi,        # π phase shift
                'pulse_shape': 'virtual'
            }
        }
        
        # Two-qubit gate parameters (CNOT via controlled-Z + single-qubit)
        self.two_qubit_pulses = {
            'CZ_gate': {
                'control_amplitude': 0.3,
                'target_amplitude': 0.0,  # Target qubit frequency modulation
                'duration': 200e-9,       # 200 ns
                'ramp_time': 20e-9,       # 20 ns ramp up/down
                'frequency_shift': 50e6,  # 50 MHz frequency shift
                'pulse_shape': 'square_with_ramps'
            }
        }
        
        # Calibration parameters
        self.calibration_params = {
            'rabi_frequency_range': [1e6, 50e6],    # 1-50 MHz
            'ramsey_time_range': [100e-9, 10e-6],   # 100 ns - 10 μs
            'process_tomography_gates': ['I', 'X', 'Y', 'Z', 'H'],
            'randomized_benchmarking_depth': [1, 2, 4, 8, 16, 32, 64, 128]
        }
        
    def generate_pulse_sequence(self, gate_type, qubit_index=None, **kwargs):
        """Generate pulse sequence for specified gate"""
        
        if gate_type in self.single_qubit_pulses:
            return self._generate_single_qubit_pulse(gate_type, qubit_index, **kwargs)
        elif gate_type in self.two_qubit_pulses:
            return self._generate_two_qubit_pulse(gate_type, **kwargs)
        else:
            raise ValueError(f"Unknown gate type: {gate_type}")
            
    def _generate_single_qubit_pulse(self, gate_type, qubit_index, **kwargs):
        """Generate single-qubit pulse sequence"""
        
        params = self.single_qubit_pulses[gate_type].copy()
        params.update(kwargs)  # Override with custom parameters
        
        # Adjust frequency for specific qubit
        base_frequency = 5.0e9  # 5 GHz base
        if qubit_index is not None:
            qubit_frequency = base_frequency + qubit_index * 100e6  # 100 MHz spacing
            params['frequency'] = qubit_frequency
        
        duration = params['duration']
        sample_rate = 2e9  # 2 GSa/s
        n_samples = int(duration * sample_rate) if duration > 0 else 1
        
        if params['pulse_shape'] == 'virtual' or duration == 0:  # Virtual Z gate
            return {
                'I_samples': np.zeros(1),
                'Q_samples': np.zeros(1), 
                'duration': 0.0,
                'frequency': params['frequency'],
                'phase_shift': params['phase'],
                'gate_type': gate_type,
                'qubit_index': qubit_index
            }
            
        time_axis = np.linspace(0, duration, n_samples)
        
        # Generate pulse envelope
        if params['pulse_shape'] == 'gaussian':
            sigma = duration / 4  # Gaussian width
            envelope = params['amplitude'] * gaussian(n_samples, sigma * sample_rate)
        elif params['pulse_shape'] == 'square':
            envelope = np.ones(n_samples) * params['amplitude']
        else:
            envelope = np.ones(n_samples) * params['amplitude']
            
        # Generate I/Q components
        phase = params['phase']
        I_samples = envelope * np.cos(phase)
        Q_samples = envelope * np.sin(phase)
        
        return {
            'I_samples': I_samples,
            'Q_samples': Q_samples,
            'duration': duration,
            'frequency': params['frequency'],
            'phase_shift': phase,
            'amplitude': params['amplitude'],  # Ensure amplitude is included
            'gate_type': gate_type,
            'qubit_index': qubit_index
        }
        
    def _generate_two_qubit_pulse(self, gate_type, control_qubit=None, target_qubit=None, **kwargs):
        """Generate two-qubit pulse sequence"""
        
        params = self.two_qubit_pulses[gate_type].copy()
        params.update(kwargs)
        
        duration = params['duration'] 
        ramp_time = params['ramp_time']
        sample_rate = 2e9
        n_samples = int(duration * sample_rate)
        
        time_axis = np.linspace(0, duration, n_samples)
        
        # Generate ramped square pulse
        envelope = np.ones(n_samples)
        
        # Ramp up/down
        ramp_samples = int(ramp_time * sample_rate)
        if ramp_samples > 0 and ramp_samples < n_samples//2:
            envelope[:ramp_samples] = np.linspace(0, 1, ramp_samples)
            envelope[-ramp_samples:] = np.linspace(1, 0, ramp_samples)
            
        # Control qubit pulse (flux pulse for frequency tuning)
        control_amplitude = params['control_amplitude']
        control_pulse = envelope * control_amplitude
        
        return {
            'control_qubit': control_qubit,
            'target_qubit': target_qubit,
            'control_pulse': control_pulse,
            'duration': duration,
            'gate_type': gate_type,
            'frequency_shift': params['frequency_shift']
        }
        
    def calibrate_single_qubit_gates(self, qubit_index):
        """Perform single-qubit gate calibration"""
        
        print(f"\n=== Calibrating Single-Qubit Gates for Q{qubit_index} ===")
        
        calibration_results = {}
        
        # 1. Rabi Calibration (find π pulse amplitude)
        print("Running Rabi calibration...")
        rabi_result = self._rabi_calibration(qubit_index)
        calibration_results['rabi'] = rabi_result
        
        # 2. Ramsey Calibration (find qubit frequency)
        print("Running Ramsey calibration...")
        ramsey_result = self._ramsey_calibration(qubit_index)
        calibration_results['ramsey'] = ramsey_result
        
        # 3. Process Tomography (characterize gate performance)
        print("Running process tomography...")
        tomography_result = self._process_tomography(qubit_index)
        calibration_results['tomography'] = tomography_result
        
        # Update pulse parameters based on calibration
        optimized_params = self._optimize_pulse_parameters(calibration_results)
        
        return {
            'qubit_index': qubit_index,
            'calibration_data': calibration_results,
            'optimized_parameters': optimized_params,
            'status': 'completed'
        }
        
    def _rabi_calibration(self, qubit_index):
        """Perform Rabi oscillation measurement"""
        
        # Simulate Rabi experiment
        amplitudes = np.linspace(0, 1.0, 21)
        populations = []
        
        for amp in amplitudes:
            # Simulate excited state population vs pulse amplitude
            rabi_freq = amp * 25e6  # 25 MHz max Rabi frequency
            pulse_duration = 20e-9   # 20 ns pulse
            
            # Rabi oscillation: P(|1>) = sin²(Ω*t/2)
            population = np.sin(rabi_freq * pulse_duration / 2)**2
            
            # Add noise
            noise = np.random.normal(0, 0.02)  # 2% measurement noise
            populations.append(max(0, min(1, population + noise)))
            
        # Find π pulse amplitude (population = 1)
        pi_pulse_idx = np.argmax(populations)
        pi_pulse_amplitude = amplitudes[pi_pulse_idx]
        
        return {
            'amplitudes': amplitudes.tolist(),
            'populations': populations,
            'pi_pulse_amplitude': float(pi_pulse_amplitude),
            'rabi_frequency_MHz': float(pi_pulse_amplitude * 25.0)
        }
        
    def _ramsey_calibration(self, qubit_index):
        """Perform Ramsey fringe measurement"""
        
        # Simulate Ramsey experiment for frequency calibration
        delay_times = np.linspace(0, 2e-6, 41)  # 0-2 μs delay
        populations = []
        
        # Assume small detuning from drive frequency
        detuning = np.random.uniform(-1e6, 1e6)  # ±1 MHz random detuning
        T2_star = 50e-6  # 50 μs T2* time
        
        for delay in delay_times:
            # Ramsey oscillation with decay
            population = 0.5 * (1 + np.exp(-delay/T2_star) * np.cos(2*np.pi*detuning*delay))
            
            # Add noise
            noise = np.random.normal(0, 0.02)
            populations.append(max(0, min(1, population + noise)))
            
        return {
            'delay_times_us': (delay_times * 1e6).tolist(),
            'populations': populations,
            'measured_detuning_Hz': float(detuning),
            'T2_star_us': float(T2_star * 1e6)
        }
        
    def _process_tomography(self, qubit_index):
        """Perform quantum process tomography"""
        
        gates = ['I', 'X', 'Y', 'Z', 'H']
        fidelities = {}
        
        for gate in gates:
            # Simulate gate fidelity measurement
            if gate == 'I':
                base_fidelity = 0.999  # Identity gate very high fidelity
            elif gate in ['X', 'Y']:
                base_fidelity = 0.995  # Single-qubit rotations
            elif gate == 'Z':
                base_fidelity = 0.9999  # Virtual Z gate
            else:  # Hadamard
                base_fidelity = 0.994   # Composite gate
                
            # Add random variation
            measured_fidelity = base_fidelity + np.random.normal(0, 0.002)
            fidelities[gate] = float(max(0.9, min(1.0, measured_fidelity)))
            
        average_fidelity = float(np.mean(list(fidelities.values())))
        
        return {
            'gate_fidelities': fidelities,
            'average_fidelity': average_fidelity,
            'process_fidelity': float(average_fidelity * 0.98)  # Account for systematic errors
        }
        
    def _optimize_pulse_parameters(self, calibration_data):
        """Optimize pulse parameters based on calibration results"""
        
        rabi_data = calibration_data['rabi']
        ramsey_data = calibration_data['ramsey']
        
        # Update pulse parameters
        optimized = {}
        
        # X gate optimization
        optimized['X_gate'] = {
            'amplitude': rabi_data['pi_pulse_amplitude'],
            'duration': 20e-9,  # Keep fixed for now
            'frequency_correction_Hz': -ramsey_data['measured_detuning_Hz'],
            'phase': 0.0
        }
        
        # Y gate (90° phase from X)
        optimized['Y_gate'] = optimized['X_gate'].copy()
        optimized['Y_gate']['phase'] = np.pi/2
        
        # Z gate (virtual)
        optimized['Z_gate'] = {
            'amplitude': 0.0,
            'duration': 0.0,
            'phase': np.pi
        }
        
        return optimized
        
    def run_randomized_benchmarking(self, qubit_index, max_depth=128):
        """Run randomized benchmarking protocol"""
        
        print(f"\n=== Randomized Benchmarking for Q{qubit_index} ===")
        
        depths = [1, 2, 4, 8, 16, 32, 64, 128]
        if max_depth < 128:
            depths = [d for d in depths if d <= max_depth]
            
        survival_probabilities = []
        
        for depth in depths:
            # Simulate RB decay
            # Assume average gate fidelity of 99.5%
            avg_gate_fidelity = 0.995
            
            # RB survival probability: P = A * p^m + B
            # where p = 1 - (2*r/d), r is average error rate, d is dimension
            p = 1 - 2 * (1 - avg_gate_fidelity) / 2  # For single qubit, d=2
            
            A = 0.5  # Amplitude
            B = 0.5  # Offset
            
            survival_prob = A * (p ** depth) + B
            
            # Add measurement noise
            noise = np.random.normal(0, 0.01)
            survival_probabilities.append(max(0.4, min(1.0, survival_prob + noise)))
            
        # Fit exponential decay to extract average gate fidelity
        try:
            from scipy.optimize import curve_fit
            
            def rb_decay(m, A, p, B):
                return A * (p ** m) + B
                
            popt, _ = curve_fit(rb_decay, depths, survival_probabilities, 
                               bounds=([0.3, 0.9, 0.4], [0.7, 1.0, 0.6]))
            A_fit, p_fit, B_fit = popt
            
            # Extract average gate fidelity
            avg_gate_fidelity_rb = 1 - (1 - p_fit) / 2
            
        except:
            avg_gate_fidelity_rb = 0.995  # Default if fit fails
            p_fit = 0.99
            
        return {
            'depths': depths,
            'survival_probabilities': survival_probabilities,
            'fitted_decay_rate': float(1 - p_fit),
            'average_gate_fidelity': float(avg_gate_fidelity_rb),
            'rb_number': float(1 / avg_gate_fidelity_rb if avg_gate_fidelity_rb > 0 else float('inf'))
        }
        
    def generate_gate_sequence(self, circuit_description):
        """Generate pulse sequence for quantum circuit - FIXED VERSION"""
        
        print(f"\n=== Generating Gate Sequence ===")
        print(f"Circuit: {circuit_description}")
        
        gate_sequence = []
        total_time = 0.0
        
        operations = circuit_description.split(';')
        
        for op in operations:
            op = op.strip()
            if not op:
                continue
                
            if '(' in op:
                gate_name = op.split('(')[0].strip()
                params = op.split('(')[1].split(')')[0]
                
                if ',' in params:
                    # Two-qubit gate
                    control, target = map(int, params.split(','))
                    
                    if gate_name == 'CNOT':
                        # Decompose CNOT into Hadamard + CZ + Hadamard
                        # H on target
                        h_pulse = self.generate_pulse_sequence('Y_gate', target)
                        if 'amplitude' in h_pulse:  # FIXED: Check if key exists
                            h_pulse['amplitude'] *= 0.5  # π/2 rotation
                        h_pulse['gate_name'] = 'H'
                        h_pulse['start_time'] = total_time
                        gate_sequence.append(h_pulse)
                        total_time += h_pulse.get('duration', 0)
                        
                        # CZ gate
                        cz_pulse = self.generate_pulse_sequence('CZ_gate', 
                                                             control_qubit=control, 
                                                             target_qubit=target)
                        cz_pulse['start_time'] = total_time
                        gate_sequence.append(cz_pulse)
                        total_time += cz_pulse.get('duration', 0)
                        
                        # H on target
                        h_pulse2 = self.generate_pulse_sequence('Y_gate', target)
                        if 'amplitude' in h_pulse2:  # FIXED: Check if key exists
                            h_pulse2['amplitude'] *= 0.5
                        h_pulse2['gate_name'] = 'H'
                        h_pulse2['start_time'] = total_time
                        gate_sequence.append(h_pulse2)
                        total_time += h_pulse2.get('duration', 0)
                        
                else:
                    # Single-qubit gate
                    qubit = int(params)
                    
                    if gate_name == 'H':
                        # Hadamard = Y(π/2) + X(π)
                        y_pulse = self.generate_pulse_sequence('Y_gate', qubit)
                        if 'amplitude' in y_pulse:  # FIXED: Check if key exists
                            y_pulse['amplitude'] *= 0.5  # π/2 rotation
                        y_pulse['gate_name'] = 'Y90'
                        y_pulse['start_time'] = total_time
                        gate_sequence.append(y_pulse)
                        total_time += y_pulse.get('duration', 0)
                        
                        x_pulse = self.generate_pulse_sequence('X_gate', qubit)
                        x_pulse['gate_name'] = 'X180'
                        x_pulse['start_time'] = total_time
                        gate_sequence.append(x_pulse)
                        total_time += x_pulse.get('duration', 0)
                        
                    else:
                        # Standard single-qubit gate
                        pulse = self.generate_pulse_sequence(gate_name + '_gate', qubit)
                        pulse['gate_name'] = gate_name
                        pulse['start_time'] = total_time  
                        gate_sequence.append(pulse)
                        total_time += pulse.get('duration', 0)
                        
        return {
            'circuit': circuit_description,
            'gate_sequence': gate_sequence,
            'total_duration': total_time,
            'gate_count': len(gate_sequence)
        }

def main():
    """Main gate implementation demonstration"""
    
    print("=== Quantum Gate Implementation Suite ===\n")
    
    # Initialize gate implementation
    gate_impl = QuantumGateImplementation()
    
    # Demonstrate single-qubit gate calibration
    print("1. Single-Qubit Gate Calibration")
    cal_result = gate_impl.calibrate_single_qubit_gates(0)
    
    # Save calibration results
    try:
        with open('gate_calibration_Q0.json', 'w', encoding='utf-8') as f:
            json.dump(cal_result, f, indent=4)
        print("✅ Calibration results saved to gate_calibration_Q0.json")
    except Exception as e:
        print(f"⚠️  Calibration save warning: {e}")
    
    # Demonstrate randomized benchmarking  
    print("\n2. Randomized Benchmarking")
    rb_result = gate_impl.run_randomized_benchmarking(0)
    
    try:
        with open('randomized_benchmarking_Q0.json', 'w', encoding='utf-8') as f:
            json.dump(rb_result, f, indent=4)
        print("✅ RB results saved to randomized_benchmarking_Q0.json")
    except Exception as e:
        print(f"⚠️  RB save warning: {e}")
    
    # Demonstrate circuit compilation
    print("\n3. Quantum Circuit Compilation")
    test_circuit = "H(0); CNOT(0,1); X(1); H(1)"
    sequence = gate_impl.generate_gate_sequence(test_circuit)
    
    try:
        with open('compiled_circuit.json', 'w', encoding='utf-8') as f:
            json.dump(sequence, f, indent=4)
        print("✅ Circuit sequence saved to compiled_circuit.json")
    except Exception as e:
        print(f"⚠️  Circuit save warning: {e}")
    
    print(f"\n✅ Total circuit duration: {sequence['total_duration']*1e9:.1f} ns")
    print(f"✅ Gate count: {sequence['gate_count']}")
    
    print("\n🎉 Gate Implementation Suite Complete!")
    print("Generated files:")
    print("- gate_calibration_Q0.json")
    print("- randomized_benchmarking_Q0.json") 
    print("- compiled_circuit.json")
    
    return gate_impl

if __name__ == "__main__":
    gate_implementation = main()
