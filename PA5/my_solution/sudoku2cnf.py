from Sudoku import Sudoku
import sys

if __name__ == "__main__":
    test_sudoku = Sudoku()

    #test_sudoku.load(sys.argv[1])
    test_sudoku.load("puzzle1.sud")
    print(test_sudoku)

    # puzzle_name = sys.argv[1][:-4]
    puzzle_name = "puzzle1"
    cnf_filename = puzzle_name + ".cnf"

    test_sudoku.generate_cnf(cnf_filename)
    print("Output file: " + cnf_filename)

