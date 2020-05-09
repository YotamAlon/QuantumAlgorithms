import unittest


class TestArithmetic(unittest.TestCase):
    def test_carry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)
        circuit.initialize((0, 1), 3)

        from Arithmetic import carry
        carry(circuit, 1, 2, 3, 0)
        circuit.measure_all()

        from qiskit import Aer
        backend = Aer.get_backend('qasm_simulator')

        from qiskit import execute
        job = execute(circuit, backend)
        counts = job.result().get_counts(circuit)

        self.assertIn('1101', counts)
        self.assertEqual(counts['1101'], 1024)


if __name__ == '__main__':
    unittest.main()
