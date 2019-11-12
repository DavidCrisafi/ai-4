import unittest
from puzzle import Puzzle


class TestGetNumbers(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGetNumbers, self).__init__(*args, **kwargs)
        self.empty_puzzle = Puzzle([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0]])

        self.first_row = Puzzle([[1, 2, 3, 4, 5, 6, 7, 8, 9],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    def test_getRowNumbers(self):
        for row in range(0, 9):
            self.assertEqual(self.empty_puzzle.getRowNumbers(row), [])
        for row in range(0, 9):
            self.assertEqual(self.first_row.getRowNumbers(row), [])


    def test_getColNumbers(self):
        for col in range(0, 9):
            self.assertEqual(self.empty_puzzle.getColNumbers(col), [])
        for col in range(0, 9):
            self.assertEqual(self.first_row.getColNumbers(col), [col+1])


    def test_getZoneNumbers(self):
        for zone in range(0, 9):
            self.assertEqual(self.empty_puzzle.getZoneNumbers(zone), [])


if __name__ == '__main__':
    unittest.main()
