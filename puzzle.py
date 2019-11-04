class Puzzle(object):
    

    def __init__(self, puzzle):
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




