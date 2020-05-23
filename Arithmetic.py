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


def add(circuit: QuantumCircuit, a, b):
    assert len(a) + 1 <= len(b), 'b register must be at least len(a) + 1 long'

    from qiskit import QuantumRegister
    c = QuantumRegister(len(a), name='adder-c')
    if not circuit.has_register(c):
        circuit.add_register(c)

    n = len(a) - 1

    for i in range(n):
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
    circuit.append(RCarry, [c[n], a[n], b[n], b[n + 1]])

    circuit.cx(a[n], b[n])

    circuit.append(Sum, [c[n], a[n], b[n]])
    for i in reversed(range(n)):
        circuit.append(LCarry, [c[i], a[i], b[i], c[i + 1]])
        circuit.append(Sum, [c[i], a[i], b[i]])


def substract(circuit: QuantumCircuit, a, b):
    assert len(a) + 1 <= len(b), 'b register must be at least len(a) + 1 long'

    from qiskit import QuantumRegister
    c = QuantumRegister(len(a), name='adder-c')
    if not circuit.has_register(c):
        circuit.add_register(c)

    n = len(a) - 1

    for i in range(n):
        circuit.append(Sum, [c[i], a[i], b[i]])
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
    circuit.append(Sum, [c[n], a[n], b[n]])

    circuit.cx(a[n], b[n])

    circuit.append(LCarry, [c[n], a[n], b[n], b[n + 1]])
    for i in reversed(range(n)):
        circuit.append(LCarry, [c[i], a[i], b[i], c[i + 1]])


def add_mod_n(circuit: QuantumCircuit, a, b, n: int):
    assert n.bit_length() - 1 <= len(b), f'b register must be at least n.bit_length() - 1 long\n' \
                                         f'Current: {len(b)}, Needed: {n.bit_length() - 1}'

    from qiskit import QuantumRegister
    n_reg = QuantumRegister(len(a), name='adder-mod-n-reg')
    if not circuit.has_register(n_reg):
        circuit.add_register(n_reg)

    t = QuantumRegister(1, name='adder-mod-t')
    if not circuit.has_register(t):
        circuit.add_register(t)

    from tools import initialize_register_to_number
    initialize_register_to_number(circuit, n_reg, n)

    add(circuit, a, b)
    substract(circuit, n_reg, b)

    circuit.x(b[-1])
    circuit.cx(b[-1], t)
    circuit.x(b[-1])

    initialize_register_to_number(circuit, n_reg, n, conditional=t)
    add(circuit, n_reg, b)
    initialize_register_to_number(circuit, n_reg, n, conditional=t)

    substract(circuit, a, b)

    circuit.cx(b[-1], t)
    add(circuit, a, b)

    initialize_register_to_number(circuit, n_reg, n)


def c_mult_a_mod_n(circuit, x, y, c, a, n):
    temp_reg_size = max(((2 ** len(x)) * a, 1)).bit_length()
    assert len(y) >= temp_reg_size + 1, f'y register must be at least {temp_reg_size + 1} long'

    from qiskit import QuantumRegister
    temp = QuantumRegister(max(((2 ** len(x)) * a, 1)).bit_length(), name='c-mult-mod-temp')
    if not circuit.has_register(temp):
        circuit.add_register(temp)

    for i in range(len(x)):
        from tools import initialize_register_to_number
        initialize_register_to_number(circuit, temp, (2 ** i) * a, conditional=x[i], conditional2=c)

        add_mod_n(circuit, temp, y, n)

        from tools import initialize_register_to_number
        initialize_register_to_number(circuit, temp, (2 ** i) * a, conditional=x[i], conditional2=c)

    circuit.x(c)
    for i in range(len(x)):
        from tools import initialize_register_to_number
        initialize_register_to_number(circuit, y[i:i + 1], 1, conditional=x[i], conditional2=c)
    circuit.x(c)
