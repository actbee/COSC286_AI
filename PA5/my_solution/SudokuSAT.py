# Author: Xuedan ZOU
# Date: 10/26/2021

# This file provides a boolean satisfiability solver

import random
from SAT import SAT

class SudokuSAT(SAT) :
    def __init__ (self, filename):
        # there are in total 729 possible variables in a sudoku problem
        self.variables_num = 729
        # our variable index runs from 1 and skip 0, each variable has 1 and -1 two values
        self.assignment = [0, ]
        for i in range(0, 729):
            # give the initial assignment 1 or -1 randomly
            random_value = random.uniform(0, 1)
            if random_value > 0.5:
               self.assignment.append(1)
            else:
               self.assignment.append(-1)

        # store the cnf as a list
        self.cnf = []
        # store a dictionary to save the map from the converted int to the original string absolute value
        self.itos = {}
        # convert the given file to the cnf
        f = open(filename, "r")
        for line in f:
            addline = []
            for s in line.split():
                addline.append(self.converter_stoi(s))
            self.cnf.append(addline)

        self.unsatisfied = []

        # used to save the given known values as constants
        self.constant = []
        for clause in self.cnf:
            if len(clause) == 1:
                self.constant.append(abs(clause[0]))

        # used to save the number of most satisfied clauses in the scoring process
        self.satisfied_history = []


    # convert the str value like 111 to the variable value like 1
    def converter_stoi(self, in_str):
        # convert this str to int value
        int_str = int(in_str)
        value = abs(int_str)
        # use abc to express a three digit number, then here index = 81*(a-1) + 9*(b-1) + c
        c = value % 10
        b = int((value % 100) / 10)
        a = int(value / 100)
        index = 81 * (a - 1) + 9 * (b - 1) + c

        self.itos[index] = int_str

        if int_str < 0:
            index = -index
        return index


    def write_solution(self, filename):
        f = open(filename, "w")
        for i in range(1, len(self.assignment)) :
            if self.assignment[i] > 0:
                f.write(str(self.itos[i]) + "\n")
            else:
                f.write(str(self.itos[i] * -1) + "\n")
        f.close()


# test
if __name__ == "__main__":
    solver = SudokuSAT("puzzle1.cnf")
    print(solver.constant)
    result = solver.WalkSAT(0.7, 100000)
    if result == True:
        print(solver.assignment)
    else:
        print("NO ANSWER")


