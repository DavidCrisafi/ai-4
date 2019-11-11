import argparse
from puzzle import Puzzle

parser = argparse.ArgumentParser(description='Sudoku Solver', prog='PROG')
parser.add_argument('-f', '--file', help='File name of sudoku puzzle', type=str, required=True)
args = parser.parse_args()


def main():    
    f = open(args.file, 'r')
    
    puzzle = Puzzle(generatePuzzle(f))
    print(puzzle.getPossibleNumbers(0,1))
    #puzzle.domain[0][0] = [7,8]
    #puzzle.domain[7][0] = [7,8]
    #puzzle.nakedPair()
    #for i in range(0,9):
    #    print(puzzle.domain[i][0])
    printPuzzle(puzzle.puzzle)


def generatePuzzle(f):
    puzzle = []
    for i in range(0, 9):
        line = f.readline().split((','))
        
        line[8] = line[8].strip('\n')
        
        intLine = []
        for n in line:
            intLine.append(int(n))
        
        puzzle.insert(i, intLine)
    
    return puzzle


#Beginner function; needs better formatting
def printPuzzle(puzzle):
    for i in range(0, 9):
        line = ""
        for j in range(0, 9):
            if (j == 0):
                line += "| "
                
            if (puzzle[i][j] != 0):
                line += "|" + str(puzzle[i][j])
            else:
                line += "|-"
            if ((j+1) % 3 == 0):
                line += "| "
            
        line += "|"
        
        if (i == 0 or i % 3 == 0):
            if (i != 0):
                print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
            print("___________________________")
        print(line)
    
    print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")


if __name__ == '__main__':
    main()
