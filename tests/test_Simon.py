import unittest


class TestSimon(unittest.TestCase):

    def test_find_period(self):
        num = 5
        from Simon import create_func_helper
        func = create_func_helper(num)

        from Simon import Solver
        result = Solver().solve(func)
        self.assertEqual(result, num)


if __name__ == '__main__':
    unittest.main()
