def get_max_result(circuit, shots=1):
    circuit = circuit.measure_all(False)

    from qiskit import Aer
    backend = Aer.get_backend('qasm_simulator')

    from qiskit import execute
    job = execute(circuit, backend, shots=shots)

    counts = job.result().get_counts(circuit)
    return max(counts, key=lambda x: counts[x])


def split_result_by_register(result, reg_len_list):
    reg_results = []
    if len(reg_len_list):
        for i in range(len(reg_len_list)):
            start_index = -sum(reg_len_list[:i + 1])
            end_index = -sum(reg_len_list[:i]) or None
            reg_results.append(result[start_index:end_index])

        if result[:start_index]:
            reg_results.append(result[:start_index])

    return reg_results


def get_numerical_register_results(circuit, reg_len_list, shots=1):
    res = get_max_result(circuit, shots)
    reg_results = split_result_by_register(res, reg_len_list)
    return [int(reg_res, 2) for reg_res in reg_results]


def initialize_register_to_number(circuit, register, num: int, conditional=None, conditional2=None):
    from numpy import binary_repr
    for i, bit in enumerate(binary_repr(num)[::-1]):
        if bit == '1':
            if conditional is None and conditional2 is None:
                circuit.x(register[i])
            elif conditional2 is None:
                circuit.cx(conditional, register[i])
            else:
                circuit.ccx(conditional, conditional2, register[i])
