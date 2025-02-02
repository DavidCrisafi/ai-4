import collections
import copy

""" A dictionary where the key is the zone index,
    and the value is a tuple of the row indices as a list
    and the column indices as a list. This lets you know
    the boundaries for a given zone.
    Ex. ZONE_INDICES(0) would return ([0, 1, 2], [0, 1, 2])

    rowIndices = ZONE_INDICES[zoneNum][0]
    colIndices = ZONE_INDICES[zoneNum][1]
    for row in rowIndices:
        for col in colIndices:
            access value in domain[row][col]
    """
ZONE_INDICES = {0: ([0, 1, 2], [0, 1, 2]), 1: ([0, 1, 2], [3, 4, 5]), 2: ([0, 1, 2], [6, 7, 8]),
                3: ([3, 4, 5], [0, 1, 2]), 4: ([3, 4, 5], [3, 4, 5]), 5: ([3, 4, 5], [6, 7, 8]),
                6: ([6, 7, 8], [0, 1, 2]), 7: ([6, 7, 8], [3, 4, 5]), 8: ([6, 7, 8], [6, 7, 8])}


class Puzzle(object):
    """
        Puzzle Class creates an object that has a
        sudoku board state and some functions for
        manipulating sudoku boards and returning
        information about them.
    """
    
    PUZZLE_MODE = 0
    DOMAIN_MODE = 1
   
    # ---------------------------- INITIALIZATION ----------------------------
   
    def __init__(self, puzzle):
        """ Sudoku board as a 2D array[9][9] (9x9 grid) of integers """
        self.puzzle = puzzle
        """ Domain is also a 2D array which has the values from the puzzle,
            but wherever there is a missing value, it inserts a list of
            potential values in the missing values position."""
        self.domain = []

        self.initDomain()

    """ Creates a new puzzle object with the same board state. """
    def __deepcopy__(self, memodict={}):
        new_puzzle = Puzzle(copy.deepcopy(self.puzzle))
        new_puzzle.domain = copy.deepcopy(self.domain)
        return new_puzzle

    """ Initializes the domain list with the actual puzzle values, or if a value is missing
        it finds a list of potential values."""
    def initDomain(self):
        for i in range(0, 9):
            newRow = []
            for j in range(0, 9):
                if self.puzzle[i][j] == 0:
                    newRow.insert(j, self.getPossibleNumbers(i, j, self.PUZZLE_MODE))
                else:
                    newRow.insert(j, self.puzzle[i][j])

            self.domain.insert(i, newRow)

    # ---------------------------- SOLVER FUNCTIONS ----------------------------
    
    def solve(self):
        def getNewBoards():
            board_states = []
            for row in range(0, 9):
                for col in range(0, 9):
                    if type(self.domain[row][col]) == list:
                        for val in self.domain[row][col]:
                            new_board = self.__deepcopy__()
                            new_board.domain[row][col] = [val]
                            new_board.setSingleValue(row, col)
                            board_states.append(new_board)
                        return board_states

        newChanges = True
        while (newChanges):
            newChanges = False
            for row in range(0, 9):
                for column in range(0, 9):
                    if not self.puzzle[row][column]:
                        result = self.getUniqueCandidate(row, column)

                        if type(result) == int:
                            self.domain[row][column] = result
                            self.puzzle[row][column] = result
                            self.recalculateDomain(row, column)
                            newChanges = True
            if self.triples():
                newChanges = True
            if self.nakedPair():
                newChanges = True
            if self.findSingles():
                newChanges = True
        if self.isSolved() is False:
            board_states = getNewBoards()

            for board in board_states:
                if board.solve():
                    self.puzzle = board.puzzle
                    return True
            return False
        else:
            return True

    """ Combines all the unique candidate functions and finds out if there
        is only one unique value between them all. If so, that is our unique
        candidate and it gets returned."""
    def getUniqueCandidate(self, row, col):
        
        if type(self.domain[row][col]) is int:
            return self.domain[row][col]
        elif len(self.domain[row][col]) == 1:
            return self.domain[row][col][0]
        
        rowCand = self.getRowUniqueCandidate(row, col)
        colCand = self.getColUniqueCandidate(row, col)
        zoneCand = self.getZoneUniqueCandidate(row, col)
        numList = []

        if rowCand != None and type(numList) == list:
            numList = getUnion(set(numList), rowCand)
        elif colCand != None and type(numList) == list:
            numList = getUnion(set(numList), colCand)
        elif zoneCand != None and type(numList) == list:
            numList = getUnion(set(numList), zoneCand)
        if numList == []:
            return None

        if (type(numList) == list):
            uniqueCandidate = set(self.domain[row][col]).difference(numList)
        else:
            return numList
        
        if len(uniqueCandidate) == 1:
            return uniqueCandidate.pop()
        elif len(uniqueCandidate) > 1:
            return uniqueCandidate
        return None

    """ Checks the domain at the specified rowNum and colNum. If
        it only has one value, the board and domain is set to the
        value at that position and returns True. Otherwise, returns
        False. """
    def setSingleValue(self, rowNum, colNum):
        if type(self.domain[rowNum][colNum]) is not list or len(self.domain[rowNum][colNum]) != 1:
            return False
        
        self.domain[rowNum][colNum] = self.domain[rowNum][colNum][0]
        self.puzzle[rowNum][colNum] = self.domain[rowNum][colNum]
        self.recalculateDomain(rowNum, colNum)
        return True

    """ Looks for single values until it stops finding any. 
    Returns True if it makes a change. False otherwise"""
    def findSingles(self):
        changed = False
        for row in range(0, 9):
            for col in range(0, 9):
                if self.setSingleValue(row, col):
                    changed = True

        if changed:
            self.findSingles()

        return changed

    """ Figures out if 3 cells are in a triple configuration.
        Looks at all possible combinations of cells.
        Returns true if it makes a change. """
    def triples(self):
        """ Triple Union
        Takes the tuple of each lists indices and finds the domain for you
        and the union of the lists. """
        def triple_union(list1, list2, list3):
            return list(set(self.domain[list1[0]][list1[1]])
                        .union(self.domain[list2[0]][list2[1]])
                        .union(self.domain[list3[0]][list3[1]]))

        """ Returns the number of elements the subset shares with the superset"""
        def num_in_set(superset, subset):
            num = 0
            for elem in subset:
                if elem in superset:
                    num += 1
            return num

        """ Returns true if the lists share x elements with the superset. x is a list of any size."""
        def lists_share_x_elems(list1, list2, list3, superset, x):
            if num_in_set(superset, self.domain[list1[0]][list1[1]]) in x \
                    and num_in_set(superset, self.domain[list2[0]][list2[1]]) in x \
                    and num_in_set(superset, self.domain[list3[0]][list3[1]]) in x:
                return True
            return False

        """ Returns true if all three lists share only 1 elements"""
        def lists_share_one_elem(list1, list2, list3):
            if num_in_set(self.domain[list1[0]][list1[1]], self.domain[list2[0]][list2[1]]) == 1 and \
                    num_in_set(self.domain[list1[0]][list1[1]], self.domain[list3[0]][list3[1]]) == 1 and \
                    num_in_set(self.domain[list2[0]][list2[1]], self.domain[list1[0]][list1[1]]) == 1 and \
                    num_in_set(self.domain[list2[0]][list2[1]], self.domain[list3[0]][list3[1]]) == 1 and \
                    num_in_set(self.domain[list3[0]][list3[1]], self.domain[list1[0]][list1[1]]) == 1 and \
                    num_in_set(self.domain[list3[0]][list3[1]], self.domain[list2[0]][list2[1]]) == 1:
                return True
            return False

        """ Finds the intersect between the lists and the superset. 
        Changes the lists to be the intersection.
        If the lists all remained the same, return False. """
        def intersected_with_superset(list1, list2, list3, superset):
            temp1 = self.domain[list1[0]][list1[1]]
            temp2 = self.domain[list2[0]][list2[1]]
            temp3 = self.domain[list3[0]][list3[1]]

            self.domain[list1[0]][list1[1]] = list(set(superset).intersection(self.domain[list1[0]][list1[1]]))
            self.domain[list2[0]][list2[1]] = list(set(superset).intersection(self.domain[list2[0]][list2[1]]))
            self.domain[list3[0]][list3[1]] = list(set(superset).intersection(self.domain[list3[0]][list3[1]]))

            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

            """ If they didn't change, return False """
            if compare(self.domain[list1[0]][list1[1]], temp1)\
                    and compare(self.domain[list2[0]][list2[1]], temp2)\
                    and compare(self.domain[list3[0]][list3[1]], temp3):
                return False
            return True

        """ Find triple function finds triples, applies the changes, lets you know if anything changed."""
        def find_triple(cell_indices):
            changed = False

            for i, cell_1 in enumerate(cell_indices):
                if type(self.domain[cell_1[0]][cell_1[1]]) == int:
                    continue
                for j, cell_2 in enumerate(cell_indices[i + 1:]):
                    if type(self.domain[cell_2[0]][cell_2[1]]) == int:
                        continue
                    for cell_3 in cell_indices[i + j + 2:]:
                        if type(self.domain[cell_3[0]][cell_3[1]]) == int:
                            continue

                        super_set = triple_union(cell_1, cell_2, cell_3)
                        for cell in cell_indices:
                            if cell == cell_1 or cell == cell_2 or cell == cell_3 or \
                                    type(self.domain[cell[0]][cell[1]]) == int:
                                continue

                            super_set = list(set(super_set).difference(self.domain[cell[0]][cell[1]]))

                        if lists_share_x_elems(cell_1, cell_2, cell_3, super_set, [2]):
                            if lists_share_one_elem(cell_1, cell_2, cell_3):
                                if intersected_with_superset(cell_1, cell_2, cell_3, super_set):
                                    changed = True
                        elif lists_share_x_elems(cell_1, cell_2, cell_3, super_set, [2, 3]):
                            if intersected_with_superset(cell_1, cell_2, cell_3, super_set):
                                changed = True
            return changed

        has_changed = False

        """ Check the rows """
        for row in range(0, 9):
            cellindices = []
            for col in range(0, 9):
                cellindices.append((row, col))
            if find_triple(cellindices):
                has_changed = True

        """ Check the columns """
        for col in range(0, 9):
            cellindices = []
            for row in range(0, 9):
                cellindices.append((row, col))
            if find_triple(cellindices):
                has_changed = True

        """ Check the zone """
        for zone in range(0, 9):
            rowBounds = ZONE_INDICES[zone][0]
            colBounds = ZONE_INDICES[zone][1]
            cellindices = []

            for row in rowBounds:
                for col in colBounds:
                    cellindices.append((row, col))
            if find_triple(cellindices):
                has_changed = True

        return has_changed

    def nakedPair(self):
        changed = False
        for j in range(0,9):
            for i in range(0,9):
                if isinstance(self.domain[i][j], int) or len(self.domain[i][j]) != 2:
                    continue
                zoneNum = self.getZone(i,j)
                zoneRowBounds = ZONE_INDICES[zoneNum][0]
                zoneColBounds = ZONE_INDICES[zoneNum][1]
                for z in range(i+1,9):

                    if self.domain[i][j] == self.domain[z][j]:
                        for t in range(0,9):
                            if t == i or t == z or isinstance(self.domain[t][j], int):
                                continue
                            else:
                                for x in self.domain[i][j]:
                                    if x in self.domain[t][j]:
                                        self.domain[t][j].remove(x)
                                        changed = True
                for z in range(j+1,9):
                    
                    if self.domain[i][j] == self.domain[i][z]:
                        for t in range(0,9):
                            if t == j or t == z or isinstance(self.domain[i][t], int):
                                continue
                            else:
                                for x in self.domain[i][j]:
                                    if x in self.domain[i][t]:
                                        self.domain[i][t].remove(x)
                                        changed = True

                for row in zoneRowBounds:
                    for col in zoneColBounds:
                        if i == row and j == col:
                            continue
                        elif (col < j and row == i) or row < i:
                            continue
                        elif self.domain[i][j] == self.domain[row][col]:
                            for row2 in zoneRowBounds:
                                for col2 in zoneColBounds:
                                    if (i == row2 and col2 == j) or (row == row2 and col == col2) or isinstance(self.domain[row2][col2], int):
                                        continue
                                    else:
                                        for x in self.domain[i][j]:
                                            if x in self.domain[row2][col2]:
                                                self.domain[row2][col2].remove(x)
                                                changed = True

        return changed

    # ---------------------------- GET VALUES ----------------------------
    """ Returns true if there is a value in each cell of the puzzle.
        Assumes that the sudoku values are legally placed.
        Could be changed to check for legality across row, col, and zone. """
    def isSolved(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if self.puzzle[row][col] == 0 or type(self.puzzle[row][col]) == list:
                    return False
        return True

    """ Based on your row and column, it returns your zone index as an int. """
    def getZone(self, row, col):
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
        return zone

    """ Returns the potential values for a given cell 
        based on its position in the sudoku board.
        Input the row and column of the sudoku cell, 
        and the function will calculate the rest. 
        
        The MODE determines which sudoku board it gets the numbers
        from. It defaults to the domain board.
        """
    def getPossibleNumbers(self, row, col, MODE=DOMAIN_MODE):
        if MODE != Puzzle.PUZZLE_MODE and MODE != Puzzle.DOMAIN_MODE:
            raise Exception("Invalid mode flag passed to getPossibleNumbers")

        """ Figures out which zone it's in based on the row and column."""
        zone = self.getZone(row, col)

        """ Gets the current values from the sudoku board's rows, columns, and grids.
            Finds the difference between those values and all the potential values
            for a sudoku board and returns that difference in a list form.
            ex. The Union of row's, col's, and zone's values unioned returned [1,2,3,4,5].
                The potential values returned would be [6,7,8,9]."""
        numList = self.getRowNumbers(row, MODE)
        numList = list(set(numList).union(self.getColNumbers(col, MODE)))
        numList = list(set(numList).union(self.getZoneNumbers(zone, MODE)))
        return list(set([1, 2, 3, 4, 5, 6, 7, 8, 9]).difference(numList))

    """ Gets all the values from a single sudoku board row 
        and returns them as a list. Ignores any values that are
        a list or an int value '0'.
        
        The MODE determines which sudoku board it gets the numbers
        from. It defaults to the domain board."""
    def getRowNumbers(self, rowNum, MODE=DOMAIN_MODE):
        numList = []
        listToScan = []

        if MODE == Puzzle.PUZZLE_MODE:
            listToScan = self.puzzle
        elif MODE == Puzzle.DOMAIN_MODE:
            listToScan = self.domain
        else:
            raise Exception("Invalid mode flag passed to getRowNumbers")

        for i in range(0,9):
            if listToScan[rowNum][i] != 0 and type(listToScan[rowNum][i]) != list:
                if listToScan[rowNum][i] not in numList:
                    numList.append(listToScan[rowNum][i])
        return numList

    """ Gets all the values from a single sudoku board column 
        and returns them as a list. Ignores any values that are
        a list or an int value '0'.
        
        The MODE determines which sudoku board it gets the numbers
        from. It defaults to the domain board. """
    def getColNumbers(self, colNum, MODE=DOMAIN_MODE):
        numList = []
        listToScan = []

        if MODE == Puzzle.PUZZLE_MODE:
            listToScan = self.puzzle
        elif MODE == Puzzle.DOMAIN_MODE:
            listToScan = self.domain
        else:
            raise Exception("Invalid mode flag passed to getColNumbers")

        for j in range(0, 9):
            if listToScan[j][colNum] != 0 and type(listToScan[j][colNum]) != list:
                if listToScan[j][colNum] not in numList:
                    numList.append(listToScan[j][colNum])
        return list(numList)
      
    """ Gets all the values for a certain sudoku board grid/zone 
        and returns them as a list. Valid inputs:   
        0,1,2
        3,4,5
        6,7,8
        
        Ignores any values that are a list or an int value '0'.
        
        Whether it returns values from the puzzle or from the domain
        depends on its mode flag. Puzzle.PUZZLE_MODE returns the puzzle
        values, and Puzzle.DOMAIN_MODE returns the domain values.
       It defaults to the domain board."""
    def getZoneNumbers(self, zoneNum, MODE=DOMAIN_MODE):
        numList = []
        listToScan = []
        
        if MODE == Puzzle.PUZZLE_MODE:
            listToScan = self.puzzle
        elif MODE == Puzzle.DOMAIN_MODE:
            listToScan = self.domain
        else:
            raise Exception("Invalid mode flag passed to getZoneNumbers")

        zoneRowBounds = ZONE_INDICES[zoneNum][0]
        zoneColBounds = ZONE_INDICES[zoneNum][1]

        for row in zoneRowBounds:
            for col in zoneColBounds:
                if listToScan[row][col] != 0 and type(listToScan[row][col]) != list:
                    if listToScan[row][col] not in numList:
                        numList.append(listToScan[row][col])

        return numList

    def getRowUniqueCandidate(self, rowNum, colNum):
        """ If it is already an int, don't change it at all."""
        if type(self.domain[rowNum][colNum]) == int:
            return self.domain[rowNum][colNum]

        numList = []
        for i in range(0, 9):
            if i == colNum:
                continue
            elif type(self.domain[rowNum][i]) == list:
                numList = set(numList).union(self.domain[rowNum][i])

        uniqueCandidate = set(self.domain[rowNum][colNum]).difference(numList)
        if len(uniqueCandidate) == 1:
            return uniqueCandidate.pop()
        elif len(uniqueCandidate) > 1:
            return uniqueCandidate
        return None

    """ Find the only possibility for a number based on its column position.
        If there is only one option, it returns that option as an INT.
        If there are multiple options, it returns a list of the options. """
    def getColUniqueCandidate(self, rowNum, colNum):
        """ If it is already an int, don't change it at all."""
        if type(self.domain[rowNum][colNum]) == int:
            return self.domain[rowNum][colNum]

        numList = []
        for i in range(0, 9):
            if i == rowNum:
                continue
            elif type(self.domain[i][colNum]) == list:
                numList = set(numList).union(self.domain[i][colNum])

        uniqueCandidate = set(self.domain[rowNum][colNum]).difference(numList)
        if len(uniqueCandidate) == 1:
            return uniqueCandidate.pop()
        elif len(uniqueCandidate) > 1:
            return uniqueCandidate
        return None

    """ Find the only possibility for a number based on its zone position.
        If there is only one option, it returns that option as an INT.
        If there are multiple options, it returns a list of the options. 
        
        NOTE: Requires ROW index and COL index as args since we need to 
        know which candidate we are looking at."""
    def getZoneUniqueCandidate(self, rowNum, colNum):
        """ Finds the zone index based on row and column. """
        zoneNum = self.getZone(rowNum, colNum)

        """ If it is already an int, don't change it at all."""
        if type(self.domain[rowNum][colNum]) == int:
            return self.domain[rowNum][colNum]

        numList = []
        rowIndices = ZONE_INDICES[zoneNum][0]
        colIndices = ZONE_INDICES[zoneNum][1]
        for i in rowIndices:
            for j in colIndices:
                if i == rowNum and j == colNum:
                    continue
                elif type(self.domain[i][j]) == list:
                    numList = set(numList).union(self.domain[i][j])

        uniqueCandidate = set(self.domain[rowNum][colNum]).difference(numList)
        if len(uniqueCandidate) == 1:
            return uniqueCandidate.pop()
        elif len(uniqueCandidate) > 1:
            return uniqueCandidate
        return None

    """ Based on a row and column of a cell, it recalculates the adjacent 
        cells values for the domain. It never adds possibilities, only 
        removes possibilities based on the context.
        
        This should be called every time a cell is set to a value.
        Input the cell's row and col coordinates."""
    def recalculateDomain(self, row, col):
        """ Recalculate everything in the same row """
        for i in range(0, 9):
            if type(self.domain[row][i]) == int:
                continue
            valList = list(self.getPossibleNumbers(row=row, col=i, MODE=self.DOMAIN_MODE))
            self.domain[row][i] = list(set(self.domain[row][i]).intersection(valList))

        """ Recalculate everything in the same column """
        for j in range(0, 9):
            if type(self.domain[j][col]) == int:
                continue
            valList = list(self.getPossibleNumbers(row=j, col=col, MODE=self.DOMAIN_MODE))
            self.domain[j][col] = list(set(self.domain[j][col]).intersection(valList))

        """ Recalculate everything in the same zone """
        zone = self.getZone(row, col)
        zoneRowBounds = ZONE_INDICES[zone][0]
        zoneColBounds = ZONE_INDICES[zone][1]

        for zoneRow in zoneRowBounds:
            for zoneCol in zoneColBounds:
                if type(self.domain[zoneRow][zoneCol]) == int:
                    continue
                valList = self.getPossibleNumbers(row=zoneRow, col=zoneCol, MODE=self.DOMAIN_MODE)
                self.domain[zoneRow][zoneCol] = list(set(self.domain[zoneRow][zoneCol]).intersection(valList))
    
# ---------------------------- HELPER FUNCTIONS ----------------------------


def getUnion(set1, set2):
    if (type(set2) == set):
        return set1.union(set2)
    elif (type(set2) == int):
        return set2
    
    return None
