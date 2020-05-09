import unittest


class TestBernsteinVazirani(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_find_a(self):
        res = []
        values = list(range(1, 32))
        for i in values:
            from BernsteinVazirani import create_func_helper
            func = create_func_helper(i)

            from BernsteinVazirani import Solver
            res.append(Solver().solve(func))
        self.assertListEqual(res, values)


import warnings
if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=DeprecationWarning)
        unittest.main()
