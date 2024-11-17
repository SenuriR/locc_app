import numpy as np
from qiskit.quantum_info import Statevector

class QuantumModel:
    def __init__(self):
        self.quantum_state = None
        self.state_desc = []  # Description of the multi-party system

    def create_quantum_state(self, amplitude_list, basis_state_list):
        """
        Initialize the quantum state with a given state.
        """
        try:
            num_qubits = len(basis_state_list[0])
            state_vector = np.zeros(2**num_qubits, dtype=complex)

            for amp, basis in zip(amplitude_list, basis_state_list):
                index = int(basis, 2)
                state_vector[index] = amp

            self.quantum_state = Statevector(state_vector)

            print(self.current_state.is_valid())

            # Manually generate bra-ket notation for the state
            bra_ket_notation = " + ".join(
                f"({amp})|{basis}⟩" for amp, basis in zip(amplitude_list, basis_state_list)
            )

            # Display the generated bra-ket notation
            print(f"Quantum State:\n {bra_ket_notation}")
            # self.q_state_label.setText(f"Quantum State:\n {bra_ket_notation}")

            # QMessageBox.information(self, "Success", "Quantum state created successfully!")
            return "Success. Quantum state created successfully."

        except Exception as e:
            # QMessageBox.warning(self, "Error", str(e))    
            return f"Error {str(e)}"
     
    def generate_state_desc_label(self, num_parties_input, num_qudits_input, dim_input):
        try:
            k = int(num_parties_input.text())
            dims = [] # overall dimension of k party
            
            num_qudits_list = list(map(int, num_qudits_input.text().split(',')))
            dim = int(self.dim_input.text())

            for i in range(k):
                num_qudits_str = num_qudits_list[i]

                if num_qudits_str == '' or dim == '':
                    raise ValueError("Please enter values for all fields.")
                
                num_qudits = int(num_qudits_str)
                

                # Append to state_desc as (number of qudits, dimensions of each qudit)
                self.state_desc.append((num_qudits, [dim] * num_qudits))

                dims.append(dim)

            # self.state_desc_label.setText(f"State Descriptor: {self.state_desc}")
            return f"{self.state_desc}"
        except Exception as e:
            return f"Error {str(e)}"

        

    def execute_locc_protocol(self, protocol_params):
        """
        Execute an LOCC protocol based on the given parameters.
        """
        # Dummy implementation
        return f"Executed protocol with params: {protocol_params}"
