#!/usr/bin/python3

# This Python program constructs the Coined Quantum Walk Search Circuit 
# with a mark and initialized to a target state. The circuit 
# is created for each of the 2^15 possible combinations of initialization
# state and node mark. The results are saved to the "data.out" file in the 
# format:
# |      Init string        |   |Target|  |                   Number of hits for each state                               |
# <aux> <coin> <node> <theta>   <target>   0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111

# Based on the work done by the Qiskit contributors at:
# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-walk-search-algorithm.ipynb

# For data output into a file
import os

 # Importing standard Qiskit libraries
from qiskit_ibm_provider import IBMProvider
from qiskit import QuantumCircuit, execute, Aer, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.circuit import Qubit

class QWalk:
    provider = None

    def __init__(self, provider):
        self.provider = provider
    
    # Defines a marked vertex in the hypercube
    def mark(self, circuit, target):
        for i in range( len(target) - 1, -1, -1 ):
            if '0' == target[i] :
                circuit.x(len(target) - 1 - i)

        circuit.h(3)
        circuit.mct([0,1,2], 3)
        circuit.h(3)

        for i in range(0, len(target)):
            if '0' == target[i] :
                circuit.x(len(target) - 1 - i)
    
    # Constructs and runs the Coined Quantum Walk search for a set of inputs
    # theta: Initialization string for the theta qubits (4 qubits)
    # node: Initialization string for the starting node (4 qubits)
    #       This is where the 2-mer code would be entered.
    # coin: Initialization string for the coin qubits (2 qubits)
    # aux: Initialization string for the aux qubit (1 qubit)
    # target: Initialization string for the target node (4 binary bits)
    def run_qwalk(self, theta, node, coin, aux, target):

        one_step_circuit = QuantumCircuit(6, name=' ONE STEP')

        # Coin operator
        one_step_circuit.h([4,5])
        one_step_circuit.z([4,5])
        one_step_circuit.cz(4,5)
        one_step_circuit.h([4,5])

        # Shift operator function for 4d-hypercube
        def shift_operator(circuit):
            for i in range(0,4):
                circuit.x(4)
                if i%2==0:
                    circuit.x(5)
                circuit.ccx(4,5,i)

        shift_operator(one_step_circuit)

        one_step_gate = one_step_circuit.to_instruction()

        # Make controlled gates
        inv_cont_one_step = one_step_circuit.inverse().control()
        inv_cont_one_step_gate = inv_cont_one_step.to_instruction()
        cont_one_step = one_step_circuit.control()
        cont_one_step_gate = cont_one_step.to_instruction()

        inv_qft_gate = QFT(4, inverse=True).to_instruction()
        qft_gate = QFT(4, inverse=False).to_instruction()

        phase_circuit =  QuantumCircuit(6, name=' phase oracle ')

        self.mark(phase_circuit, target)

        phase_oracle_gate = phase_circuit.to_instruction()
        # Phase oracle circuit
        phase_oracle_circuit =  QuantumCircuit(11, name=' PHASE ORACLE CIRCUIT ')
        phase_oracle_circuit.append(phase_oracle_gate, [4,5,6,7,8,9])

        # Mark q_4 if the other qubits are non-zero
        mark_auxiliary_circuit = QuantumCircuit(5, name=' mark auxiliary ')
        mark_auxiliary_circuit.x([0,1,2,3,4])
        mark_auxiliary_circuit.mct([0,1,2,3], 4)
        mark_auxiliary_circuit.z(4)
        mark_auxiliary_circuit.mct([0,1,2,3], 4)
        mark_auxiliary_circuit.x([0,1,2,3,4])

        mark_auxiliary_gate = mark_auxiliary_circuit.to_instruction()

        # Phase estimation
        phase_estimation_circuit = QuantumCircuit(11, name=' phase estimation ')
        phase_estimation_circuit.h([0,1,2,3])
        for i in range(0,4):
            stop = 2**i
            for j in range(0,stop):
                phase_estimation_circuit.append(cont_one_step, [i,4,5,6,7,8,9])

        # Inverse fourier transform
        phase_estimation_circuit.append(inv_qft_gate, [0,1,2,3])

        # Mark all angles theta that are not 0 with an auxiliary qubit
        phase_estimation_circuit.append(mark_auxiliary_gate, [0,1,2,3,10])

        # Reverse phase estimation
        phase_estimation_circuit.append(qft_gate, [0,1,2,3])

        for i in range(3,-1,-1):
            stop = 2**i
            for j in range(0,stop):
                phase_estimation_circuit.append(inv_cont_one_step, [i,4,5,6,7,8,9])

        phase_estimation_circuit.barrier(range(0,10))
        phase_estimation_circuit.h([0,1,2,3])

        # Make phase estimation gate
        phase_estimation_gate = phase_estimation_circuit.to_instruction()
       
        # Implementation of the full quantum walk search algorithm
        theta_q = QuantumRegister(4, 'theta')
        node_q = QuantumRegister(4, 'node')
        coin_q = QuantumRegister(2, 'coin')
        auxiliary_q = QuantumRegister(1, 'auxiliary')
        creg_c2 = ClassicalRegister(4, 'c')

        # Full Quantum Walk Algorithm
        circuit = QuantumCircuit(theta_q, node_q, coin_q, auxiliary_q, creg_c2)

        circuit.initialize(aux+coin+node+theta, circuit.qubits)

        # Apply Hadamard gates to the qubits that represent the nodes and the coin
        circuit.h([4,5,6,7,8,9])

        iterations = 2

        for i in range(0,iterations):
            circuit.append(phase_oracle_gate, [4,5,6,7,8,9])
            circuit.append(phase_estimation_gate, [0,1,2,3,4,5,6,7,8,9,10])

        circuit.measure(node_q[0], creg_c2[0])
        circuit.measure(node_q[1], creg_c2[1])
        circuit.measure(node_q[2], creg_c2[2])
        circuit.measure(node_q[3], creg_c2[3])
 
        backend = Aer.get_backend('qasm_simulator')
          
        job = execute( circuit, backend, shots=1024 )

        hist = job.result().get_counts()

        return hist

    def main():
        # Loading your IBM Q account(s)
        provider = IBMQ.load_account()
        qwalk = QWalk(provider)

        data_file_name = "data.out"
        
        # Spanning the entire combinatorial space
        with open(data_file_name, 'w') as out:
            line = ""

            for g in range (0, 2):
                aux = format(g, '01b')
                for h in range (0, 4):
                    coin = format(h, '02b')
                    for i in range (0, 16):
                        node = format(i, '04b')
                        for j in range (0, 16):
                            theta = format(j, '04b')
                            for k in range (0, 16):
                                line = ""
                                target = format (k, '04b')
                                line = aux+" "+coin+" "+node+" "+theta+"   "+target+"   "
                                hist = qwalk.run_qwalk(theta, node, coin, aux, target)

                                for a in range(0, 16):
                                    try:
                                        index = format(a, '04b')
                                        line = line+((str(hist[index])).rjust(4))
                                    except:
                                       line = line+(("0").rjust(4))
                                
                                out =  open(data_file_name, 'a')
                                out.write(line)
                                out.write('\n')
                                out.close()


if __name__ == '__main__':
    QWalk.main()