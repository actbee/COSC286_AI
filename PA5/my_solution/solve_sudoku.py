# Author: Xuedan ZOU
# Date: 10/27/2021

from display import display_sudoku_solution
import random, sys
from SudokuSAT import SudokuSAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    # puzzle_name = str(sys.argv[1][:-4])
    # here change the file name to yours to solve your problem
    puzzle_name = "puzzle1"
    puzzle_file = puzzle_name + ".cnf"
    sol_filename = puzzle_name + ".sol"

    # sat = SAT(sys.argv[1])
    sat = SudokuSAT(puzzle_file)
    print(len(sat.cnf))
    # you can change the solving method, h and max_iterate times here
    result = sat.WalkSAT(0.7, 1000000)

    if result:
        print(sat.assignment)
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)

    else:
        print("No Solution!")