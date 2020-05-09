class Solver(object):
    def solve(self, func, bits=None, backend_name='qasm_simulator'):
        bits = bits or getattr(func, 'bits', None)

        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(bits + 1)
        [circuit.initialize((1, 0), i) for i in range(bits)]
        circuit.initialize((0, 1), bits)

        circuit.h([i for i in range(bits + 1)])
        func(circuit)
        circuit.h([i for i in range(bits + 1)])

        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend(backend_name)

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)
        res = int(max(counts, key=lambda x: counts[x])[1:], 2)

        return res


def create_func_helper(num: int):
    def func(circuit):
        from numpy import binary_repr
        [circuit.cx(i, num.bit_length()) for i, x in enumerate(binary_repr(num)[::-1]) if x == '1']
    func.bits = num.bit_length()
    return func
