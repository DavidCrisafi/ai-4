class Puzzle(object):
    """
        Puzzle Class creates an object that has a
        sudoku board state and some functions for
        manipulating sudoku boards and returning
        information about them.
    """

    def __init__(self, puzzle):
        """ Sudoku board as a 2D array (9x9 grid) of integers """
        self.puzzle = puzzle
        self.domain = []

        self.initDomain()

    # initilizing the domain puzzle (0 to a list and number values to set values.
    def initDomain(self):
        for i in range(0,9):
            newRow = []
            for j in range(0,9):
                if (self.puzzle[i][j] == 0):
                    newRow.insert(j, [1,2,3,4,5,6,7,8,9])
                else:
                    newRow.insert(j, self.puzzle[i][j])

            self.domain.insert(i, newRow)

    """ Gets all the values from a single sudoku board row 
        and returns them as a list """
    def getRowNumbers(self, rowNum):
        numList = []
        for i in range(0,9):
            if (self.puzzle[i][rowNum] != 0):
                if self.puzzle[i][rowNum] not in numList:
                    numList.append(self.puzzle[i][rowNum])
        return numList

    """ Gets all the values from a single sudoku board column 
        and returns them as a list """
    def getColNumbers(self, colNum):
        numList = []
        for j in range(0,9):
            if (self.puzzle[colNum][j] != 0):
                if self.puzzle[colNum][j] not in numList:
                    numList.append(self.puzzle[colNum][j])
        return numList

    def getPossibleNumbers(self, row, col):
        rowsZones = []
        colsZones = []

        if row in [0, 1, 2]:
            rowsZones = [0, 1, 2]
        elif row in [3, 4, 5]:
            rowsZones = [3, 4, 5]
        elif row in [6, 7, 8]:
            rowsZones = [6, 7, 8]

        if col in [0, 1, 2]:
            colsZones = [0, 3, 6]
        elif col in [3, 4, 5]:
            colsZones = [1, 4, 7]
        elif col in [6, 7, 8]:
            colsZones = [2, 5, 8]

        zone = set(rowsZones).intersection(colsZones).pop()
        numList = self.getRowNumbers(row)
        numList = set(numList).intersection(self.getColNumbers(col))
        numList = set(numList).intersection(self.getZoneNumbers(zone))
        return numList
      
    """ Gets all the values for a certain sudoku board grid/zone 
        and returns them as a list. Valid inputs:   
        0,1,2
        3,4,5
        6,7,8   """
    def getZoneNumbers(self, zoneNum):
        numList = []
        if zoneNum == 0:
            for i in range(0,3):
                for j in range(0,3):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 1:
            for i in range(3,6):
                for j in range(0,3):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 2:
            for i in range(6,9):
                for j in range(0,3):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 3:
            for i in range(0,3):
                for j in range(3,6):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 4:
            for i in range(3,6):
                for j in range(3,6):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 5:
            for i in range(6,9):
                for j in range(3,6):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 6:
            for i in range(0,3):
                for j in range(6,9):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 7:
            for i in range(3,6):
                for j in range(6,9):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        elif zoneNum == 8:
            for i in range(6,9):
                for j in range(6,9):
                    if (self.puzzle[i][j] != 0):
                        if self.puzzle[i][j] not in numList:
                            numList.append(self.puzzle[i][j])
        return numList
