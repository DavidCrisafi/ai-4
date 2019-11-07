class Puzzle(object):
    """
        Puzzle Class creates an object that has a
        sudoku board state and some functions for
        manipulating sudoku boards and returning
        information about them.
    """
    
    PUZZLE_MODE = 0
    DOMAIN_MODE = 1
    
    def __init__(self, puzzle):
        """ Sudoku board as a 2D array[9][9] (9x9 grid) of integers """
        self.puzzle = puzzle
        """ Domain is also a 2D array which has the values from the puzzle,
            but wherever there is a missing value, it inserts a list of
            potenial values in the missing values position."""
        self.domain = []

        self.initDomain()

    # initilizing the domain puzzle (0 to a list and number values to set values.
    """ Initializes the domain list with the actual puzzle values, or if a value is missing
        it finds a list of potential values."""
    def initDomain(self):
        for i in range(0, 9):
            newRow = []
            for j in range(0,9):
                if self.puzzle[i][j] == 0:
                    newRow.insert(j, self.getPossibleNumbers(i, j))
                    # newRow.insert(j, [1,2,3,4,5,6,7,8,9])
                else:
                    newRow.insert(j, self.puzzle[i][j])

            self.domain.insert(i, newRow)

    """ Returns the potential values for a given square 
        based on its position in the sudoku board.
        Input the row and column of the sudoku square, 
        and the function will calculate the rest. """
    def getPossibleNumbers(self, row, col):
        """ Figures out which zone its in based on the row and column."""
        zone = None
        if row in [0, 1, 2]:
            zone = [0, 1, 2]
        elif row in [3, 4, 5]:
            zone = [3, 4, 5]
        elif row in [6, 7, 8]:
            zone = [6, 7, 8]

        if col in [0, 1, 2]:
            zone = set(zone).intersection([0, 3, 6]).pop()
        elif col in [3, 4, 5]:
            zone = set(zone).intersection([1, 4, 7]).pop()
        elif col in [6, 7, 8]:
            zone = set(zone).intersection([2, 5, 8]).pop()

        """ Gets the current values from the sudoku board's rows, columns, and grids.
            Finds the difference between those values and all the potential values
            for a sudoku board and returns that difference in a list form.
            ex. The Union of row's, col's, and zone's values unioned returned [1,2,3,4,5].
                The potential values returned would be [6,7,8,9]."""
        numList = self.getRowNumbers(row)
        numList = set(numList).union(self.getColNumbers(col))
        numList = set(numList).union(self.getZoneNumbers(zone, Puzzle.PUZZLE_MODE))
        return list(set([1, 2, 3, 4, 5, 6, 7, 8, 9]).difference(numList))

    """ Gets all the values from a single sudoku board row 
        and returns them as a list """
    def getRowNumbers(self, rowNum):
        numList = []
        for i in range(0,9):
            if (self.puzzle[rowNum][i] != 0):
                if self.puzzle[rowNum][i] not in numList:
                    numList.append(self.puzzle[rowNum][i])
        return numList

    """ Gets all the values from a single sudoku board column 
        and returns them as a list """
    def getColNumbers(self, colNum):
        numList = []
        for j in range(0,9):
            if (self.puzzle[j][colNum] != 0):
                if self.puzzle[j][colNum] not in numList:
                    numList.append(self.puzzle[j][colNum])
        return numList
      
    """ Gets all the values for a certain sudoku board grid/zone 
        and returns them as a list. Valid inputs:   
        0,1,2
        3,4,5
        6,7,8
        
        Whether it returns values from the puzzle or from the domain
        depends on its mode flag. Puzzle.PUZZLE_MODE returns the puzzle
        values, and Puzzle.DOMAIN_MODE returns the domain values.   """
    def getZoneNumbers(self, zoneNum, mode):
        numList = []
        listToScan = []
        
        if mode == Puzzle.PUZZLE_MODE:
            listToScan = self.puzzle
        elif mode == Puzzle.DOMAIN_MODE:
            listToScan = self.domain
        else:
            raise Exception("Invalid mode flag passed to getZoneNumbers")
        
        if zoneNum == 0:
            for j in range(0,3):
                for i in range(0,3):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 1:
            for j in range(3,6):
                for i in range(0,3):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 2:
            for j in range(6,9):
                for i in range(0,3):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 3:
            for j in range(0,3):
                for i in range(3,6):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 4:
            for j in range(3,6):
                for i in range(3,6):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 5:
            for j in range(6,9):
                for i in range(3,6):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 6:
            for j in range(0,3):
                for i in range(6,9):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 7:
            for j in range(3,6):
                for i in range(6,9):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        elif zoneNum == 8:
            for j in range(6,9):
                for i in range(6,9):
                    if (listToScan[i][j] != 0):
                        if listToScan[i][j] not in numList:
                            numList.append(listToScan[i][j])
        return numList

    """ Checks the domain at the specified rowNum and colNum. If
        it only has one value, the board and domain is set to the
        value at that position and returns True. Otherwise, returns
        False. """
    def setSingleValue(self, rowNum, colNum):
        if type(self.domain[rowNum][colNum]) is not list or len(self.domain[rowNum][colNum]) != 1:
            return False
        
        self.domain[rowNum][colNum] = self.domain[rowNum][colNum][0]
        self.puzzle[rowNum][colNum] = self.domain[rowNum][colNum]
        return True
