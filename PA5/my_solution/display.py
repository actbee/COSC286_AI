# Author: Xuedan ZOU
# Date: 10/27/2021

# to print out the solution

from Sudoku import Sudoku
import sys

def display_sudoku_solution(filename):

    test_sudoku = Sudoku()
    test_sudoku.read_solution(filename)
    print(test_sudoku)

if __name__ == "__main__":
    display_sudoku_solution(sys.argv[1])