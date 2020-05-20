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
                c = QuantumRegister(3)
                circuit = QuantumCircuit(a, b, c)

                from tools import initialize_register_to_number
                initialize_register_to_number(circuit, a, i)
                initialize_register_to_number(circuit, b, j)

                from Arithmetic import add
                add(circuit, a, b, c)

                from tools import get_max_result
                res = get_max_result(circuit)

                a_res = res[7:]
                b_res = res[3:7]
                c_res = res[0:3]

                self.assertEqual(i, int(a_res, 2))
                self.assertEqual(i + j, int(b_res, 2))
                self.assertEqual(0, int(c_res, 2))

    def test_substract(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for i in range(8):
            for j in range(8):
                a = QuantumRegister(3)
                b = QuantumRegister(4)
                c = QuantumRegister(3)
                circuit = QuantumCircuit(a, b, c)

                from tools import initialize_register_to_number
                initialize_register_to_number(circuit, a, i)
                initialize_register_to_number(circuit, b, j)

                from Arithmetic import substract
                substract(circuit, a, b, c)

                from tools import get_max_result
                res = get_max_result(circuit)

                a_res = res[7:]
                b_res = res[3:7]
                c_res = res[0:3]

                self.assertEqual(i, int(a_res, 2))
                self.assertEqual((j - i) % (2 ** 4), int(b_res, 2))
                self.assertEqual(0, int(c_res, 2))

    def test_add_mod_n(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for k in range(1, 8):
            for i in range(k):
                for j in range(k):
                    a = QuantumRegister(3)
                    b = QuantumRegister(4)
                    extra = QuantumRegister(7)
                    circuit = QuantumCircuit(a, b, extra)

                    from tools import initialize_register_to_number
                    initialize_register_to_number(circuit, a, i)
                    initialize_register_to_number(circuit, b, j)

                    from Arithmetic import add_mod_n
                    add_mod_n(circuit, a, b, extra, k)

                    from tools import get_max_result
                    res = get_max_result(circuit)

                    a_res = res[11:]
                    b_res = res[7:11]
                    c_res = res[4:7]
                    n_res = res[1:4]
                    t_res = res[0]

                    self.assertEqual(i, int(a_res, 2))
                    self.assertEqual((i + j) % k, int(b_res, 2))
                    self.assertEqual(0, int(c_res, 2))
                    self.assertEqual(k, int(n_res, 2))
                    self.assertEqual(0, int(t_res, 2))

    def test_c_mult_mod_n(self):
        from qiskit import QuantumCircuit, QuantumRegister
        for k in range(1, 8):
            for i in range(k):
                for j in range(k):
                    a = QuantumRegister(3)
                    b = QuantumRegister(4)
                    c = QuantumRegister(3)
                    e = QuantumRegister(3)
                    n = QuantumRegister(3)
                    t = QuantumRegister(1)
                    cc = QuantumRegister(1)
                    circuit = QuantumCircuit(a, b, c, n, t)

                    from Arithmetic import generate_c_mult_y_mod_n
                    c_mult_a_mod_n = generate_c_mult_y_mod_n(i)
                    c_mult_a_mod_n(circuit, a, b, cc, e, c, k, n, t)

                    from tools import get_max_result
                    res = get_max_result(circuit)

                    a_res = res[11:]
                    b_res = res[7:11]
                    c_res = res[4:7]
                    n_res = res[1:4]
                    t_res = res[0]

                    self.assertEqual(i, int(a_res, 2))
                    self.assertEqual((i + j) % k, int(b_res, 2))
                    self.assertEqual(0, int(c_res, 2))
                    self.assertEqual(k, int(n_res, 2))
                    self.assertEqual(0, int(t_res, 2))


if __name__ == '__main__':
    unittest.main()
