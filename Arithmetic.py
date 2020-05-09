from qiskit import QuantumCircuit


def carry(circuit: QuantumCircuit, control_qubit1, control_qubit2, control_qubit3, target_qubit):
    circuit.ccx(control_qubit3, control_qubit1, target_qubit)
    circuit.cx(control_qubit2, control_qubit1)
    circuit.ccx(control_qubit2, control_qubit1, target_qubit)
