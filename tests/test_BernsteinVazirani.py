import unittest


class TestBernsteinVazirani(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_find_a(self):
        from BernsteinVazirani import create_func_helper
        func = create_func_helper(5)

        from BernsteinVazirani import Solver
        result = Solver().solve(func)
        self.assertEqual(5, result)


if __name__ == '__main__':
    unittest.main()
