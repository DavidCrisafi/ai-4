import argparse

parser = argparse.ArgumentParser(description='Sudoku Solver', prog='PROG')
parser.add_argument('-f', '--file', help='File name of sudoku puzzle', type=str, required=True)
args = parser.parse_args()

def main():    
    f = open(args.file, 'r')

    puzzle = generatePuzzle(f)
    printPuzzle(puzzle)

def generatePuzzle(f):
    puzzle = []
    for i in range(0, 9):
        line = f.readline().split((','))
        
        line[8] = line[8].strip('\n')
        
        puzzle.insert(i, line)
    
    return puzzle

#Beginner function; needs better formatting
def printPuzzle(puzzle):
    for p in puzzle:
        print(p)

if __name__ == '__main__':
    main()
