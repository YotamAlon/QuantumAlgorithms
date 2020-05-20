from qiskit import QuantumCircuit


def make_instruction(name, func, qbits):
    from qiskit import QuantumRegister
    q = QuantumRegister(qbits)

    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(q, name=name)

    func(circuit, *[q[i] for i in range(qbits)])

    return circuit.to_instruction()


def right_carry(circuit: QuantumCircuit, q0, q1, q2, q3):
    circuit.ccx(q1, q2, q3)
    circuit.cx(q1, q2)
    circuit.ccx(q0, q2, q3)


RCarry = make_instruction('RCarry', right_carry, 4)
LCarry = RCarry.inverse()


def sum_(circuit: QuantumCircuit, q0, q1, q2):
    circuit.cx(q1, q2)
    circuit.cx(q0, q2)


Sum = make_instruction('Sum', sum_, 3)


def add(circuit: QuantumCircuit, a, b, c):
    assert len(a) + 1 <= len(b), 'b register must be at least a.size + 1 long'
    assert len(a) <= len(c), 'c register must be at least a.size long'

    n = len(a) - 1

    for i in range(n):
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
    circuit.append(RCarry, [c[n], a[n], b[n], b[n + 1]])

    circuit.cx(a[n], b[n])

    circuit.append(Sum, [c[n], a[n], b[n]])
    for i in reversed(range(n)):
        circuit.append(LCarry, [c[i], a[i], b[i], c[i + 1]])
        circuit.append(Sum, [c[i], a[i], b[i]])


def substract(circuit: QuantumCircuit, a, b, c):
    assert len(a) + 1 <= len(b), 'b register must be at least len(a) + 1 long'
    assert len(a) <= len(c), 'c register must be at least len(a) long'

    n = len(a) - 1

    for i in range(n):
        circuit.append(Sum, [c[i], a[i], b[i]])
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
    circuit.append(Sum, [c[n], a[n], b[n]])

    circuit.cx(a[n], b[n])

    circuit.append(LCarry, [c[n], a[n], b[n], b[n + 1]])
    for i in reversed(range(n)):
        circuit.append(LCarry, [c[i], a[i], b[i], c[i + 1]])


def add_mod_n(circuit, a, b, extra, n: int):
    assert n.bit_length() <= len(a), 'b register must be at least n.bit_length() - 1 long'
    assert (len(a) * 2) + 1 <= len(extra), 'the extra register must be at least (len(a) * 2) + 1 long'
    c = extra[:len(a)]
    n_reg = extra[len(a):len(a) * 2]
    t = extra[len(a) * 2]

    from tools import initialize_register_to_number
    initialize_register_to_number(circuit, n_reg, n)

    add(circuit, a, b, c)
    substract(circuit, n_reg, b, c)

    circuit.x(b[-1])
    circuit.cx(b[-1], t)
    circuit.x(b[-1])

    initialize_register_to_number(circuit, n_reg, n, conditional=t)
    add(circuit, n_reg, b, c)
    initialize_register_to_number(circuit, n_reg, n, conditional=t)

    substract(circuit, a, b, c)

    circuit.cx(b[-1], t)
    add(circuit, a, b, c)

    initialize_register_to_number(circuit, n_reg, n)


def generate_c_mult_y_mod_n(y):
    from numpy import binary_repr
    y_list = [int(bit) for bit in binary_repr(y)[::-1]]

    def c_mult_y_mod_n(circuit, x_reg, y_reg, c, a_reg, c_reg, n, n_reg, t):
        for i in range(x_reg.size):
            from tools import initialize_register_to_number
            initialize_register_to_number(circuit, a_reg, (2 ** i) * y_list[i], conditional=x_reg[i], conditional2=c)

            add_mod_n(circuit, a_reg, y_reg, c_reg, n, n_reg, t)

            from tools import initialize_register_to_number
            initialize_register_to_number(circuit, a_reg, (2 ** i) * y_list[i], conditional=x_reg[i], conditional2=c)

        circuit.x(c)
        for i in range(x_reg.size):
            from tools import initialize_register_to_number
            initialize_register_to_number(circuit, y_reg[i], 1, conditional=x_reg[i], conditional2=c)
        circuit.x(c)

    return c_mult_y_mod_n
