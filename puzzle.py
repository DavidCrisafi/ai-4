class Puzzle(object):
    

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.domain = []

        initDomain()

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
            if (puzzle[i][rowNum] != 0):
                if puzzle[i][rowNum] not in numList:
                    numList.append(puzzle[i][rowNum])
        return numList

    def getColNumbers(self, colNum):
        numList = []
        for j in range(0,9):
            if (puzzle[colNum][j] != 0):
                if puzzle[colNum][j] not in numList:
                    numList.append(puzzle[colNum][j])
        return numList

    # Zone number are 0, 1, 2
    #                 3, 4, 5
    #                 6, 7, 8
    def getZoneNum(self, zoneNum):
        numList = []
        if zoneNum == 0:
            for i in range(0,3):
                for j in range(0,3):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 1:
            for i in range(3,6):
                for j in range(0,3):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 2:
            for i in range(6,9):
                for j in range(0,3):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 3:
            for i in range(0,3):
                for j in range(3,6):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 4:
            for i in range(3,6):
                for j in range(3,6):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 5:
            for i in range(6,9):
                for j in range(3,6):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 6:
            for i in range(0,3):
                for j in range(6,9):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 7:
            for i in range(3,6):
                for j in range(6,9):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        elif zoneNum == 8:
            for i in range(6,9):
                for j in range(6,9):
                    if (puzzle[i][j] != 0):
                        if puzzle[i][j] not in numList:
                            numList.append(puzzle[i][j])
        return numList


