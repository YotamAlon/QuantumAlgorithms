import unittest


class TestArithmetic(unittest.TestCase):
    def test_left_carry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)
        circuit.initialize((0, 1), 3)

        from Arithmetic import left_carry
        left_carry(circuit, 0, 1, 2, 3)
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('1101', counts)
        self.assertEqual(counts['1101'], 1024)

    def test_right_carry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import right_carry
        right_carry(circuit, 0, 1, 2, 3)
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('1011', counts)
        self.assertEqual(counts['1011'], 1024)

    def test_LCarry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)
        circuit.initialize((0, 1), 3)

        from Arithmetic import LCarry
        circuit.append(LCarry, [0, 1, 2, 3])
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('1101', counts)
        self.assertEqual(counts['1101'], 1024)

    def test_RCarry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import RCarry
        circuit.append(RCarry, [0, 1, 2, 3])
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('1011', counts)
        self.assertEqual(counts['1011'], 1024)

    def test_left_sum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import left_sum
        left_sum(circuit, 0, 1, 2)
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('110', counts)
        self.assertEqual(counts['110'], 1024)

    def test_right_sum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)

        from Arithmetic import right_sum
        right_sum(circuit, 0, 1, 2)
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('011', counts)
        self.assertEqual(counts['011'], 1024)

    def test_LSum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import LSum
        circuit.append(LSum, [0, 1, 2])
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('110', counts)
        self.assertEqual(counts['110'], 1024)

    def test_RSum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)

        from Arithmetic import RSum
        circuit.append(RSum, [0, 1, 2])
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('011', counts)
        self.assertEqual(counts['011'], 1024)

    @staticmethod
    def initialize_register_to_number(circuit, register, num: int):
        from numpy import binary_repr
        for i, bit in enumerate(binary_repr(num)[::-1]):
            if bit == '1':
                circuit.x(register[i])

    def test_right_add(self):
        from qiskit import QuantumCircuit, QuantumRegister
        a = QuantumRegister(3)
        b = QuantumRegister(4)
        c = QuantumRegister(3)
        circuit = QuantumCircuit(a, b, c)
        self.initialize_register_to_number(circuit, a, 5)
        self.initialize_register_to_number(circuit, b, 7)

        from Arithmetic import right_add
        right_add(circuit, a, b, c)
        circuit.measure_all()
        print(circuit.draw())

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend, shots=1)

        counts = job.result().get_counts(circuit)
        res = max(counts, key=lambda x: counts[x])
        c_res = res[:3]
        b_res = res[3:7]
        a_res = res[7:]
        print(a_res, b_res, c_res)
        print(int(b_res, 2))

        self.assertEqual(12, int(list(counts.keys())[0][3:7], 2))


if __name__ == '__main__':
    unittest.main()
