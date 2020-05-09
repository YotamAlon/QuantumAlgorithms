class Solver(object):
    def solve(self, func, bits=None, backend_name='qasm_simulator'):
        return 5


def create_func_helper(num: int):
    def func(circuit):
        from numpy import pi, sin
    func.bits = num.bit_length()
    return func