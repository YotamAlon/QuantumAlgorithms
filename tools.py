def get_max_result(circuit, shots=1):
    circuit = circuit.measure_all(False)

    from qiskit import Aer
    backend = Aer.get_backend('qasm_simulator')

    from qiskit import execute
    job = execute(circuit, backend, shots=shots)

    counts = job.result().get_counts(circuit)
    return max(counts, key=lambda x: counts[x])