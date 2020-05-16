from qiskit import QuantumCircuit


def make_instruction(name, func, qbits):
    from qiskit import QuantumRegister
    q = QuantumRegister(qbits)

    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(q, name=name)

    func(circuit, *[q[i] for i in range(qbits)])

    return circuit.to_instruction()


def left_carry(circuit: QuantumCircuit, q0, q1, q2, q3):
    circuit.ccx(q0, q2, q3)
    circuit.cx(q1, q2)
    circuit.ccx(q1, q2, q3)
    circuit.barrier()


LCarry = make_instruction('LCarry', left_carry, 4)


def right_carry(circuit: QuantumCircuit, q0, q1, q2, q3):
    circuit.ccx(q1, q2, q3)
    circuit.cx(q1, q2)
    circuit.ccx(q0, q2, q3)
    circuit.barrier()


RCarry = make_instruction('RCarry', right_carry, 4)


def sum_(circuit: QuantumCircuit, q0, q1, q2):
    circuit.cx(q1, q2)
    circuit.cx(q0, q2)
    circuit.barrier()


Sum = make_instruction('Sum', sum_, 3)


def add(circuit: QuantumCircuit, a, b, c):
    assert a.size + 1 <= b.size, 'b register must be at least a.size + 1 long'
    assert a.size <= c.size, 'c register must be at least a.size long'

    n = a.size - 1

    for i in range(n):
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
    circuit.append(RCarry, [c[n], a[n], b[n], b[n + 1]])

    circuit.cx(a[n], b[n])

    circuit.append(Sum, [c[n], a[n], b[n]])
    for i in reversed(range(n)):
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
        circuit.append(Sum, [c[i], a[i], b[i]])


def substract(circuit: QuantumCircuit, a, b, c):
    assert a.size + 1 <= b.size, 'b register must be at least a.size + 1 long'
    assert a.size <= c.size, 'c register must be at least a.size long'

    n = a.size - 1

    for i in range(n):
        circuit.append(Sum, [c[i], a[i], b[i]])
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
    circuit.append(Sum, [c[n], a[n], b[n]])

    circuit.cx(a[n], b[n])

    circuit.append(RCarry, [c[n], a[n], b[n], b[n + 1]])
    for i in reversed(range(n)):
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])

