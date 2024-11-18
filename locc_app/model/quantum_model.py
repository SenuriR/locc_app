import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import XGate, HGate, CXGate
from k_party import k_party
from locc_operation import locc_operation

class QuantumModel:
    def __init__(self):
        self.quantum_state = None
        self.state_desc = []
        self.k = None
        self.k_party = None
        self.locc_protocol_obj = None

    def create_locc_protocol(self):
        '''Really just a method to make sure that there is an actual locc protocol object created.'''
        if self.locc_protocol_obj is None:
            raise ValueError("Error. LOCC Protocol has no items.")
        else:
            return f"LOCC Protocl created successfully, number of items in protocol: {len(self.locc_protocol_obj)}"

    def save_locc_step(self, party_index, qudit_index, operation_type, operator_choice, condition):
        if operator_choice == "XGate":
            operator = XGate()
        elif operator_choice == "HGate":
            operator = HGate()
        elif operator_choice == "CXGate":
            operator = CXGate()

        locc_op = locc_operation(party_index, qudit_index, operation_type, operator, condition)

        self.locc_protocol_obj.append(locc_op)

        return f"LOCC Operation Created:\nParty Index: {locc_op.party_index}\nQudit Index: {locc_op.qudit_index}\n Operation Type: {locc_op.operation_type}\nCondition: {locc_op.condition}\nOperator: {locc_op.operator}"

    def create_k_party(self):
        try:
            if self.current_state is None:
                raise ValueError("No quantum state created. Please create a state first.")
            
            self.kparty = k_party(
                k=self.k,
                dims=self.current_state.dim,
                state_desc=self.state_desc,
                q_state=self.current_state
            )

            return f"KParty object created successfully!"
        except Exception as e:
            return f"Error: {str(e)}"

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

            bra_ket_notation = " + ".join(
                f"({amp})|{basis}⟩" for amp, basis in zip(amplitude_list, basis_state_list)
            )

            print(f"Quantum State:\n {bra_ket_notation}")

            return "Success. Quantum state created successfully."

        except Exception as e:
            return f"Error {str(e)}"
     
    def generate_state_desc_label_and_k_party(self, num_parties_input, num_qudits_input, dim_input):
        try:
            self.k = int(num_parties_input.ktext())
            dims = [] # every item in dims will be the same, keeping dims in list form to be consistent with exisitng k party class structure
            
            num_qudits_list = list(map(int, num_qudits_input.text().split(',')))
            dim = int(self.dim_input.text())

            for i in range(self.k):
                num_qudits_str = num_qudits_list[i]

                if num_qudits_str == '' or dim == '':
                    raise ValueError("Please enter values for all fields.")
                
                num_qudits = int(num_qudits_str)

                # Append to state_desc as (number of qudits, dimensions of each qudit)
                self.state_desc.append((num_qudits, [dim] * num_qudits))

                dims.append(dim)

            if self.current_state is None:
                raise ValueError("No quantum state created. Please create a state first.")
            
            self.kparty = k_party(
                k=self.k,
                dims=self.current_state.dim,
                state_desc=self.state_desc,
                q_state=self.current_state
            )

            return f"k_party_obj created. state_desc: {self.state_desc}"
        except Exception as e:
            return f"Error {str(e)}"

    def execute_locc_protocol(self, protocol_params):
        """
        Execute an LOCC protocol based on the given parameters.
        """
        # Dummy implementation
        return f"Executed protocol with params: {protocol_params}"
