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
        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1101', res)

    def test_right_carry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import right_carry
        right_carry(circuit, 0, 1, 2, 3)

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1011', res)

    def test_LCarry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)
        circuit.initialize((0, 1), 3)

        from Arithmetic import LCarry
        circuit.append(LCarry, [0, 1, 2, 3])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1101', res)

    def test_RCarry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import RCarry
        circuit.append(RCarry, [0, 1, 2, 3])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1011', res)

    def test_left_sum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import left_sum
        left_sum(circuit, 0, 1, 2)

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('110', res)

    def test_right_sum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)

        from Arithmetic import right_sum
        right_sum(circuit, 0, 1, 2)

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('011', res)

    def test_LSum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import LSum
        circuit.append(LSum, [0, 1, 2])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('110', res)

    def test_RSum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)

        from Arithmetic import RSum
        circuit.append(RSum, [0, 1, 2])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('011', res)

    @staticmethod
    def initialize_register_to_number(circuit, register, num: int):
        from numpy import binary_repr
        for i, bit in enumerate(binary_repr(num)[::-1]):
            if bit == '1':
                circuit.x(register[i])

    def test_right_add(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for i in range(8):
            for j in range(8):
                a = QuantumRegister(3)
                b = QuantumRegister(4)
                c = QuantumRegister(3)
                circuit = QuantumCircuit(a, b, c)
                self.initialize_register_to_number(circuit, a, i)
                self.initialize_register_to_number(circuit, b, j)

                from Arithmetic import right_add
                right_add(circuit, a, b, c)

                from tools import get_max_result
                res = get_max_result(circuit)

                a_res = res[7:]
                b_res = res[3:7]

                self.assertEqual(i, int(a_res, 2))
                self.assertEqual(i+j, int(b_res, 2))


if __name__ == '__main__':
    unittest.main()
