# Author: Xuedan ZOU
# Date: 10/27/2021

from Sudoku import Sudoku
import sys

if __name__ == "__main__":
    test_sudoku = Sudoku()

    #test_sudoku.load(sys.argv[1])
    # test_sudoku.load("puzzle2.sud")
    # print(test_sudoku)

    # puzzle_name = sys.argv[1][:-4]
    # change the puzzle_name to yours to generate its .cnf file
    puzzle_name = "puzzle2"
    load_filename = puzzle_name + ".sud"
    cnf_filename = puzzle_name + ".cnf"

    test_sudoku.load(load_filename)
    print(test_sudoku)
    test_sudoku.generate_cnf(cnf_filename)
    print("Output file: " + cnf_filename)

