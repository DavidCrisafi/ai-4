class Puzzle(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.domain = []

        self.initDomain()

    # initilizing the domain puzzle (0 to a list and number values to set values.
    def initDomain(self):
        for i in range(0,9):
            for j in range(0,9):
                if (self.puzzle[i][j] == 0):
                    self.domain[i][j] = [1,2,3,4,5,6,7,8,9]
                else:
                    self.domain[i][j] = self.puzzle[i][j]

    def getRowNumbers(self, rowNum):
        numList = []
        for i in range(0,9):
            if (self.puzzle[i][rowNum] != 0):
                if self.puzzle[i][rowNum] not in numList:
                    numList.append(self.puzzle[i][rowNum])
        return numList

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
