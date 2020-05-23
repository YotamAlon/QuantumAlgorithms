import unittest


class TestArithmetic(unittest.TestCase):
    def test_right_carry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((1, 0), 2)

        from Arithmetic import right_carry
        right_carry(circuit, 0, 1, 2, 3)

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1111', res)

    def test_LCarry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((1, 0), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((1, 0), 2)

        from Arithmetic import LCarry
        circuit.append(LCarry, [0, 1, 2, 3])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1110', res)

    def test_RCarry(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(4)
        circuit.initialize((0, 1), 0)
        circuit.initialize((0, 1), 1)
        circuit.initialize((1, 0), 2)

        from Arithmetic import RCarry
        circuit.append(RCarry, [0, 1, 2, 3])

        from tools import get_max_result
        res = get_max_result(circuit)

        self.assertEqual('1111', res)

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

    def test_add(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for i in range(8):
            for j in range(8):
                a = QuantumRegister(3)
                b = QuantumRegister(4)
                circuit = QuantumCircuit(a, b)

                from tools import initialize_register_to_number
                initialize_register_to_number(circuit, a, i)
                initialize_register_to_number(circuit, b, j)

                from Arithmetic import add
                add(circuit, a, b)

                from tools import get_numerical_register_results
                a_res, b_res, extra = get_numerical_register_results(circuit, [len(a), len(b)])

                self.assertEqual(i, a_res)
                self.assertEqual(i + j, b_res)
                self.assertEqual(0, extra)

    def test_substract(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for i in range(8):
            for j in range(8):
                a = QuantumRegister(3)
                b = QuantumRegister(4)
                circuit = QuantumCircuit(a, b)

                from tools import initialize_register_to_number
                initialize_register_to_number(circuit, a, i)
                initialize_register_to_number(circuit, b, j)

                from Arithmetic import substract
                substract(circuit, a, b)

                from tools import get_numerical_register_results
                a_res, b_res, extra = get_numerical_register_results(circuit, [len(a), len(b)])

                self.assertEqual(i, a_res)
                self.assertEqual((j - i) % (2 ** 4), b_res)
                self.assertEqual(0, extra)

    def test_add_mod_n(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for k in range(1, 8):
            for i in range(k):
                for j in range(k):
                    a = QuantumRegister(3)
                    b = QuantumRegister(4)
                    circuit = QuantumCircuit(a, b)

                    from tools import initialize_register_to_number
                    initialize_register_to_number(circuit, a, i)
                    initialize_register_to_number(circuit, b, j)

                    from Arithmetic import add_mod_n
                    add_mod_n(circuit, a, b, k)

                    from tools import get_numerical_register_results
                    a_res, b_res, extra = get_numerical_register_results(circuit, [len(a), len(b)])

                    self.assertEqual(i, a_res)
                    self.assertEqual((i + j) % k, b_res)
                    self.assertEqual(0, extra)

    @unittest.skip
    def test_c_mult_a_mod_n(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for k in range(1, 4):
            for i in range(k):
                for j in range(k):
                    x = QuantumRegister(2)
                    y = QuantumRegister(4)
                    c = QuantumRegister(1)
                    circuit = QuantumCircuit(x, y, c)

                    from tools import initialize_register_to_number
                    initialize_register_to_number(circuit, x, j)
                    initialize_register_to_number(circuit, c, 1)

                    from Arithmetic import c_mult_a_mod_n
                    c_mult_a_mod_n(circuit, x, y, c, i, k)

                    from tools import get_numerical_register_results
                    x_res, y_res, c_res, extra = get_numerical_register_results(circuit, [len(x), len(y), 1])

                    self.assertEqual(j, x_res)
                    self.assertEqual((j * i) % k, y_res)
                    self.assertEqual(1, c_res)
                    self.assertEqual(0, extra)


if __name__ == '__main__':
    unittest.main()
