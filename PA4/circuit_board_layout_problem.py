# Author: Xuedan ZOU
# Date: 10/17/2021

from CSP_Model import CSP_Model
import copy

class circuit_board_layout(CSP_Model):
    def __init__(self, variables, domains, neighbors = {}):
        super().__init__(variables, domains, neighbors)
        self.name = "circuit board layout problem"

        # to memorize the size of our circuit board
        board = self.get_property(domains)
        self.width = board[0]
        self.height = board[1]

        # to map our tuple variable to their index
        self.variable_ttoi = {}
        number = 0
        for variable in self.variables:
            self.variable_ttoi[variable] = number
            number += 1

        # generate our domains
        self.domains = {}
        for variable in self.variables:
            mykey = self.variable_ttoi[variable]
            self.domains[mykey] = []

            pro = self.get_property(variable)
            xmax = self.width - pro[0]
            ymax = self.height - pro[1]
            for j in range(0, ymax+1):
                for i in range(0, xmax+1):
                    index = self.cor_to_index(i, j)
                    self.domains[mykey].append(index)

        # generate our neighbors, all of these variables should be
        # constraint with each other
        for variable in self.variables:
            mykey = self.variable_ttoi[variable]
            self.neighbors[mykey] = []
            for other_variable in self.variables:
                if variable != other_variable:
                    other = self.variable_ttoi[other_variable]
                    self.neighbors[mykey].append(other)

    # to transfer the coordinate to the index
    def cor_to_index(self, x, y):
        index = self.width * y + x
        return index

    # to transfer the index to the coordinate
    def index_to_cor(self, index):
        x = index % self.width
        y = int((index - x)/self.width)
        cor = (x, y)
        return cor

    # to get the length and height from a tuple
    def get_property(self, input):
        height = len(input)
        length = len(input[0])
        property = [length, height]
        return property

    # modify the constraint function
    def constraints(self, variable, value):
        neighborlist = self.neighbors[variable]
        # if there is no neighbor for the current variable
        if len(neighborlist) == 0:
            return True
        # the value of this variable can not be equal to any neighbor's value
        for neighbor in neighborlist:
            neighbor_value = self.assignment[neighbor]
            # we jump the neighbors that has not been given a position
            if neighbor_value == -1:
                continue
            test = self.pair_constraint(variable, value, neighbor, neighbor_value)
            if test == False:
               return False
        return True

    # overwrite pair_constraint
    def pair_constraint(self, x1, value_x1, x2, value_x2):
        # get the properties and coordinates of each value
        x1_pro = self.get_property(self.variables[x1])
        x1_cor = self.index_to_cor(value_x1)
        x2_pro = self.get_property(self.variables[x2])
        x2_cor = self.index_to_cor(value_x2)

        x1_left = x1_cor[0]
        x1_right = x1_cor[0] + x1_pro[0] - 1
        x1_down = x1_cor[1]
        x1_up = x1_cor[1] + x1_pro[1] - 1

        x2_left = x2_cor[0]
        x2_right = x2_cor[0] + x2_pro[0] - 1
        x2_down = x2_cor[1]
        x2_up = x2_cor[1] + x2_pro[1] - 1

        # judge if they dont intersect
        if (x1_right < x2_left or x1_down > x2_up) or\
                (x2_right < x1_left or x2_down > x1_up):
          return True
        else:
          return False

    # based on the specific problem this can be overwrote
    def Print_Solution(self, result):
        if (result == False):
            print("no solution found to the problem: " + self.name)
        else:
            print("the solution to the problem: " + self.name + " is: " + "\n")
            # board is used to save the rendered layout, with the lowest row in the first line
            board = []
            line = []
            for i in range(0, self.width):
                line.append(".")
            for i in range(0, self.height):
                addline = copy.deepcopy(line)
                board.append(addline)

            for i in range(0, len(self.variables)):
                solution = self.assignment[i]
                cor = self.index_to_cor(solution)
                xmin = cor[0]
                ymin = cor[1]
                pro = self.get_property(self.variables[i])
                xmax = xmin + pro[0] - 1
                ymax = ymin + pro[1] - 1
                for x in range(xmin, xmax+1):
                    for y in range(ymin, ymax+1):
                        board[y][x] = self.variables[i][0][0]

            # render the board
            for j in range(self.height-1, -1, -1):
                for i in range(0, self.width):
                    print(board[j][i], end = "")
                print("\n")


# test part
if __name__ == "__main__" :
    variables = []
    a = ("aaa",
         "aaa")
    b = ("bbbbb",
         "bbbbb")
    c = ("cc",
         "cc",
         "cc")
    e = ("eeeeeee",)
    variables.append(a)
    variables.append(b)
    variables.append(c)
    variables.append(e)
    board = ("..........",
             "..........",
             "..........")
    domains = board
    test_model = circuit_board_layout(variables, domains)
    test_model.BackTracking_Search("MRV", "LCV","AC-3")
    test_model.BackTracking_Search()