# Author: Xuedan ZOU
# Date: 10/17/2021

from CSP_Model import CSP_Model

class map_coloring_problem(CSP_Model):

    def __init__(self, variables, domains, neighbors):
        super().__init__(variables, domains, neighbors)
        self.name = "Map Coloring Problem"


    # we overwrite the constraints function for map coloring problem
    def constraints(self, variable, value):
        # get the name of our variable
        variable_name = self.variables[variable]
        neighborlist =  self.neighbors[variable_name]
        # if there is no neighbor for the current variable
        if len(neighborlist) == 0:
            return True
        # the value of this variable can not be equal to any neighbor's value
        for neighbor in neighborlist:
            neighbor_value = self.assignment[self.variable_stoi[neighbor]]
            if neighbor_value == value:
                return False
        return True


    # overwrite pair_constraint
    def pair_constraint(self, x1, value_x1, x2, value_x2):
        x1_name = self.variables[x1]
        x2_name = self.variables[x2]
        x1_neighborlist = self.neighbors[x1_name]

        if x2_name not in x1_neighborlist:
            # they are mot neighbor
            return True

        if value_x1 != value_x2:
            return True
        else:
            return False


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
    print(test_model.domain_stoi)
    test_model.BackTracking_Search("MRV", "LCV","AC-3")
