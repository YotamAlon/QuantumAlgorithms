import unittest


class TestArithmetic(unittest.TestCase):
    def test_left_carry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import left_carry
        left_carry(circuit, 0, 1, 2, 3)
        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1011', res)

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
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((0, 1), 2)

        from Arithmetic import LCarry
        circuit.append(LCarry, [0, 1, 2, 3])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1011', res)

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

    def test_sum_(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)

        from Arithmetic import sum_
        sum_(circuit, 0, 1, 2)

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('011', res)

    def test_Sum(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(3)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)

        from Arithmetic import Sum
        circuit.append(Sum, [0, 1, 2])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('011', res)

    @staticmethod
    def initialize_register_to_number(circuit, register, num: int):
        from numpy import binary_repr
        for i, bit in enumerate(binary_repr(num)[::-1]):
            if bit == '1':
                circuit.x(register[i])

    def test_add(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for i in range(8):
            for j in range(8):
                a = QuantumRegister(3)
                b = QuantumRegister(4)
                c = QuantumRegister(3)
                circuit = QuantumCircuit(a, b, c)
                self.initialize_register_to_number(circuit, a, i)
                self.initialize_register_to_number(circuit, b, j)

                from Arithmetic import add
                add(circuit, a, b, c)

                from tools import get_max_result
                res = get_max_result(circuit)

                a_res = res[7:]
                b_res = res[3:7]

                self.assertEqual(i, int(a_res, 2))
                self.assertEqual(i + j, int(b_res, 2))

    def test_substract(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for i in range(8):
            for j in range(8):
                a = QuantumRegister(3)
                b = QuantumRegister(4)
                c = QuantumRegister(3)
                circuit = QuantumCircuit(a, b, c)
                self.initialize_register_to_number(circuit, a, i)
                self.initialize_register_to_number(circuit, b, j)

                from Arithmetic import substract
                substract(circuit, a, b, c)

                from tools import get_max_result
                res = get_max_result(circuit)

                a_res = res[7:]
                b_res = res[3:7]

                self.assertEqual(i, int(a_res, 2))
                print(j, '-', i, '=', int(b_res, 2))
                if j >= i:
                    self.assertEqual(j - i, int(b_res, 2))
                else:
                    self.assertEqual((2 ** 4) - (i - j), int(b_res, 2))


if __name__ == '__main__':
    unittest.main()
