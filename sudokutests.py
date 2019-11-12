import unittest
from puzzle import Puzzle
from puzzle import ZONE_INDICES


class TestGetNumbers(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGetNumbers, self).__init__(*args, **kwargs)

        self.remove_zeros = lambda puzzle_list: list(set(puzzle_list).difference([0]))

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

        self.first_col = Puzzle([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                               [2, 0, 0, 0, 0, 0, 0, 0, 0],
                               [3, 0, 0, 0, 0, 0, 0, 0, 0],
                               [4, 0, 0, 0, 0, 0, 0, 0, 0],
                               [5, 0, 0, 0, 0, 0, 0, 0, 0],
                               [6, 0, 0, 0, 0, 0, 0, 0, 0],
                               [7, 0, 0, 0, 0, 0, 0, 0, 0],
                               [8, 0, 0, 0, 0, 0, 0, 0, 0],
                               [9, 0, 0, 0, 0, 0, 0, 0, 0]])

        self.first_zone = Puzzle([[1, 2, 3, 0, 0, 0, 0, 0, 0],
                                 [4, 5, 6, 0, 0, 0, 0, 0, 0],
                                 [7, 8, 9, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0]])

        self.random_dist = Puzzle([[0, 0, 0, 0, 0, 0, 5, 8, 0],
                                  [7, 0, 0, 6, 0, 0, 0, 0, 0],
                                  [0, 0, 9, 0, 0, 0, 0, 4, 0],
                                  [0, 9, 5, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 2, 0, 0, 0, 0, 7],
                                  [0, 4, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 5, 4, 0, 0, 0],
                                  [6, 0, 0, 0, 9, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 8, 0, 0, 3]])

        self.solved_puzzle = Puzzle([[1, 4, 5, 7, 9, 3, 8, 6, 2],
                                    [6, 2, 7, 8, 4, 1, 5, 9, 3],
                                    [8, 9, 3, 5, 6, 2, 4, 1, 7],
                                    [7, 6, 2, 4, 1, 8, 9, 3, 5],
                                    [3, 1, 4, 2, 5, 9, 6, 7, 8],
                                    [9, 5, 8, 3, 7, 6, 2, 4, 1],
                                    [2, 8, 9, 1, 3, 4, 7, 5, 6],
                                    [5, 3, 6, 9, 2, 7, 1, 8, 4],
                                    [4, 7, 1, 6, 8, 5, 3, 2, 9]])

    def test_getRowNumbers(self):
        """ Empty Puzzle """
        for row in range(0, 9):
            self.assertEqual(self.empty_puzzle.getRowNumbers(row),
                             self.remove_zeros(self.empty_puzzle.puzzle[row]))

        """ Only 1 full row in puzzle """
        for row in range(0, 9):
            self.assertEqual(self.first_row.getRowNumbers(row),
                             self.remove_zeros(self.first_row.puzzle[row]))

        """ Only 1 full column in puzzle"""
        for row in range(0, 9):
            self.assertEqual(self.first_col.getRowNumbers(row),
                             self.remove_zeros(self.first_col.puzzle[row]))

        """ Only 1 full zone in puzzle"""
        for row in range(0, 9):
            for val in self.first_zone.getRowNumbers(row):
                self.assertIn(val, self.remove_zeros(self.first_zone.puzzle[row]))

        """ Random distribution of values"""
        for row in range(0, 9):
            for val in self.random_dist.getRowNumbers(row):
                self.assertIn(val, self.remove_zeros(self.random_dist.puzzle[row]))

        """ Solved Sudoku Puzzle"""
        for row in range(0, 9):
            for val in self.solved_puzzle.getRowNumbers(row):
                self.assertIn(val, self.remove_zeros(self.solved_puzzle.puzzle[row]))

    def test_getColNumbers(self):
        """ Empty Puzzle """
        for col in range(0, 9):
            column = []
            for row in range(0, 9):
                column.append(self.empty_puzzle.puzzle[row][col])
            self.assertEqual(self.empty_puzzle.getColNumbers(col),
                             self.remove_zeros(column))

        """ Only 1 full row in puzzle """
        for col in range(0, 9):
            column = []
            for row in range(0, 9):
                column.append(self.first_row.puzzle[row][col])
            self.assertEqual(self.first_row.getColNumbers(col),
                             self.remove_zeros(column))

        """ Only 1 full column in puzzle"""
        for col in range(0, 9):
            column = []
            for row in range(0, 9):
                column.append(self.empty_puzzle.puzzle[row][col])
            self.assertEqual(self.empty_puzzle.getColNumbers(col),
                             self.remove_zeros(column))

        """ Only 1 full zone in puzzle"""
        for col in range(0, 9):
            column = []
            for row in range(0, 9):
                column.append(self.first_zone.puzzle[row][col])
            for val in self.first_zone.getColNumbers(col):
                self.assertIn(val, column)


        """ Random distribution of values"""
        for col in range(0, 9):
            column = []
            for row in range(0, 9):
                column.append(self.random_dist.puzzle[row][col])
            for val in self.random_dist.getColNumbers(col):
                self.assertIn(val, column)

        """ Solved Sudoku Puzzle"""
        for col in range(0, 9):
            column = []
            for row in range(0, 9):
                column.append(self.solved_puzzle.puzzle[row][col])
            for val in self.solved_puzzle.getColNumbers(col):
                self.assertIn(val, column)

    def test_getZoneNumbers(self):
        """ Empty Puzzle """
        for zone in range(0, 9):
            rows = ZONE_INDICES[zone][0]
            cols = ZONE_INDICES[zone][1]

            zoneVals = []
            for row in rows:
                for col in cols:
                    zoneVals.append(self.empty_puzzle.puzzle[row][col])
            for val in self.empty_puzzle.getZoneNumbers(zone):
                self.assertIn(val, zoneVals)

        """ Only 1 full row in puzzle """
        for zone in range(0, 9):
            rows = ZONE_INDICES[zone][0]
            cols = ZONE_INDICES[zone][1]

            zoneVals = []
            for row in rows:
                for col in cols:
                    zoneVals.append(self.first_row.puzzle[row][col])
            for val in self.first_row.getZoneNumbers(zone):
                self.assertIn(val, zoneVals)

        """ Only 1 full column in puzzle"""
        for zone in range(0, 9):
            rows = ZONE_INDICES[zone][0]
            cols = ZONE_INDICES[zone][1]

            zoneVals = []
            for row in rows:
                for col in cols:
                    zoneVals.append(self.first_col.puzzle[row][col])
            for val in self.first_col.getZoneNumbers(zone):
                self.assertIn(val, zoneVals)

        """ Only 1 full zone in puzzle"""
        for zone in range(0, 9):
            rows = ZONE_INDICES[zone][0]
            cols = ZONE_INDICES[zone][1]

            zoneVals = []
            for row in rows:
                for col in cols:
                    zoneVals.append(self.first_zone.puzzle[row][col])
            for val in self.first_zone.getZoneNumbers(zone):
                self.assertIn(val, zoneVals)

        """ Random distribution of values"""
        for zone in range(0, 9):
            rows = ZONE_INDICES[zone][0]
            cols = ZONE_INDICES[zone][1]

            zoneVals = []
            for row in rows:
                for col in cols:
                    zoneVals.append(self.random_dist.puzzle[row][col])
            for val in self.random_dist.getZoneNumbers(zone):
                self.assertIn(val, zoneVals)

        """ Solved Sudoku Puzzle"""
        for zone in range(0, 9):
            rows = ZONE_INDICES[zone][0]
            cols = ZONE_INDICES[zone][1]

            zoneVals = []
            for row in rows:
                for col in cols:
                    zoneVals.append(self.solved_puzzle.puzzle[row][col])
            for val in self.solved_puzzle.getZoneNumbers(zone):
                self.assertIn(val, zoneVals)

    def test_getPossibleNumbers(self):
        
        pass

if __name__ == '__main__':
    unittest.main()
