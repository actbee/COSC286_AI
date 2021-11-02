# Author: Xuedan ZOU
# Date: 10/27/2021

from display import display_sudoku_solution
import random, sys
from SudokuSAT import SudokuSAT

# used to draw lines
# import matplotlib.pyplot as plt

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    # puzzle_name = str(sys.argv[1][:-4])
    # here change the file name to yours to solve your problem
    puzzle_name = "puzzle2"
    puzzle_file = puzzle_name + ".cnf"
    sol_filename = puzzle_name + ".sol"

    # sat = SAT(sys.argv[1])
    sat = SudokuSAT(puzzle_file)
    # you can change the solving method, h and max_iterate times here
    result = sat.WalkSAT(0.7, 1000000)

    # set the third parameter to be True if you'd like to consider constants
    # result = sat.WalkSAT(0.7, 1000000, True)

    if result:
        print(sat.assignment)
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
        # plt.plot(sat.satisfied_history)
        # plt.ylim(len(sat.cnf) - 50, len(sat.cnf))
        # plt.show()

    else:
        print("No Solution!")