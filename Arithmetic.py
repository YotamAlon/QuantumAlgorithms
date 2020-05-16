from qiskit import QuantumCircuit


def make_instruction(name, func, qbits):
    from qiskit import QuantumRegister
    q = QuantumRegister(qbits)

    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(q, name=name)

    func(circuit, *[q[i] for i in range(qbits)])

    return circuit.to_instruction()


def left_carry(circuit: QuantumCircuit, q0, q1, q2, q3):
    """Upwards carry"""
    circuit.ccx(q1, q3, q0)
    circuit.cx(q2, q1)
    circuit.ccx(q1, q2, q0)
    circuit.barrier()


LCarry = make_instruction('LCarry', left_carry, 4)


def right_carry(circuit: QuantumCircuit, q0, q1, q2, q3):
    """Downwards carry"""
    circuit.ccx(q1, q2, q3)
    circuit.cx(q1, q2)
    circuit.ccx(q0, q2, q3)
    circuit.barrier()


RCarry = make_instruction('RCarry', right_carry, 4)


def left_sum(circuit: QuantumCircuit, q0, q1, q2):
    """Upwards sum"""
    circuit.cx(q2, q0)
    circuit.cx(q1, q0)
    circuit.barrier()


LSum = make_instruction('LSum', left_sum, 3)


def right_sum(circuit: QuantumCircuit, q0, q1, q2):
    """Downwards sum"""
    circuit.cx(q1, q2)
    circuit.cx(q0, q2)
    circuit.barrier()


RSum = make_instruction('RSum', right_sum, 3)


def right_add(circuit: QuantumCircuit, a, b, c):
    """Downwards add"""
    assert a.size + 1 <= b.size, 'b register must be at least a.size + 1 long'
    assert a.size <= c.size, 'c register must be at least a.size long'

    n = a.size - 1

    circuit.barrier()

    for i in range(n):
        circuit.append(RCarry, [c[i], a[i], b[i], c[i + 1]])
        # right_carry(circuit, c[i], a[i], b[i], c[i + 1])
    circuit.append(RCarry, [c[n], a[n], b[n], b[n + 1]])
    # right_carry(circuit, c[n], a[n], b[n], b[n + 1])

    circuit.cx(a[n], b[n])
    circuit.barrier()

    circuit.append(RSum, [c[n], a[n], b[n]])
    # right_sum(circuit, c[n], a[n], b[n])
    for i in reversed(range(n)):
        circuit.append(LCarry, [c[i], a[i], b[i], c[i + 1]])
        # left_carry(circuit, c[i], a[i], b[i], c[i + 1])
        circuit.append(RSum, [c[i], a[i], b[i]])
        # right_sum(circuit, c[i], a[i], b[i])


def left_add(circuit: QuantumCircuit, a, b, c):
    """Upwards substract"""
    assert a.size >= b.size + 1, 'a register must be at least b.size + 1 long'
    assert b.size <= c.size, 'c register must be at least b.size long'

    n = a.size - 1

    for i in reversed(range(n)):
        left_sum(circuit, a[i], b[i], )
