# Author: Xuedan ZOU
# Date: 10/17/2021

from CSP_Model import CSP_Model

class map_coloring_problem(CSP_Model):

    def __init__(self, variables, domains, neighbors):
        super().__init__(variables, domains, neighbors)
        self.name = "Map Coloring Problem"

        # we should map the values in variable(string) to the ints
        self.variable_stoi = {}
        number = 0
        for variable in self.variables:
            self.variable_stoi[variable] = number
            number += 1

        # we should map the values in the domain(string) to the ints
        self.domain_stoi = {}
        number = 1
        for variable in self.variables:
            for value in self.domains[variable]:
                # if we have not this value into our mapper
                if value not in self.domain_stoi.keys():
                    self.domain_stoi[value] = number
                    number += 1

        # we can also map the values in from ints to domain(string)
        self.domain_itos = {v: k for k, v in self.domain_stoi.items()}

        # convert our domain and neighbors from string into ints to store
        self.domains = {}
        for name, list in domains.items():
            mykey = self.variable_stoi[name]
            self.domains[mykey] = []
            for value in list:
                self.domains[mykey].append(self.domain_stoi[value])

        self.neighbors = {}
        for name, list in neighbors.items():
            mykey = self.variable_stoi[name]
            self.neighbors[mykey] = []
            for value in list:
                self.neighbors[mykey].append(self.variable_stoi[value])


    # we overwrite the constraints function for map coloring problem
    def constraints(self, variable, value):
        neighborlist =  self.neighbors[variable]
        # if there is no neighbor for the current variable
        if len(neighborlist) == 0:
            return True
        # the value of this variable can not be equal to any neighbor's value
        for neighbor in neighborlist:
            neighbor_value = self.assignment[neighbor]
            if neighbor_value == value:
                return False
        return True


    # overwrite pair_constraint
    def pair_constraint(self, x1, value_x1, x2, value_x2):

        x1_neighborlist = self.neighbors[x1]

        if x2 not in x1_neighborlist:
            # they are mot neighbor
            return True

        if value_x1 != value_x2:
            return True
        else:
            return False


    # based on the specific problem this can be overwrote
    def Print_Solution(self, result):
        if (result == False):
            print("no solution found to the problem: " + self.name)
        else:
            print("the solution to the problem: " + self.name + " is: ")
            for i in range(0, len(self.variables)):
                solved_value = self.assignment[i]
                print(self.variables[i] + " : " + self.domain_itos[solved_value])


if __name__ == "__main__" :
    variables = ["WA", "NT", "SA", "QL", "NSW", "V", "T"]
    domains = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue"]
    neighbors ={}
    neighbors["WA"] = ["NT", "SA"]
    neighbors["NT"] = ["WA", "SA", "QL"]
    neighbors["SA"] = ["WA", "NT", "QL", "NSW", "V"]
    neighbors["QL"] = ["NT", "SA", "NSW"]
    neighbors["NSW"] = ["QL", "SA", "V"]
    neighbors["V"] = ["SA", "NSW"]
    neighbors["T"] = []

    test_model = map_coloring_problem(variables, domains, neighbors )
    print(test_model.neighbors)
    print(test_model.domains)
    test_model.BackTracking_Search("MRV", "LCV","AC-3")
