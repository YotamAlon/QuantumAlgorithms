import unittest


class TestTools(unittest.TestCase):
    def test_split_result_by_register(self):
        from tools import split_result_by_register
        res_list = split_result_by_register('0010001', [4, 3])
        self.assertEqual(['0001', '001'], res_list)


if __name__ == '__main__':
    unittest.main()
