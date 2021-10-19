# Author: Xuedan ZOU
# Date: 10/17/2021

import copy
import queue

# I put the CSP model itself and the solver to this model in one class
class CSP_Model:

    def __init__(self, variables, domains, neighbors):
       self.name = "CSP Problem"
       self.variables = variables
       self.domains = domains
       self.neighbors = neighbors

       # to decide whether those heuristic methods are used in the search part
       self.select_method = "default"
       self.order_method = "default"
       self.inference_method = "default"

       # store the assignment to the problem
       self.assignment = []
       # establish a table to store the possible domains for each variable
       self.domain_remain = {}
       # build a domain_remain stack to store the history
       self.domain_remain_stack = []



    # use this method to recover some varialbes in the class into the initial status
    # since our assignment and domain_remain value will be changed in the searching
    # process, it is a safe way to initialize them before every search
    def clean(self):
        #  default assignment's values with -1
        self.assignment = []
        for i in range(0, len(self.variables)):
            self.assignment.append(-1)

        # domain_remain saves values as ints
        self.domain_remain = {}
        for variable in range(0, len(self.variables)):
            add_list = []
            for value in self.domains[variable]:
                add_list.append(value)
            self.domain_remain[variable] = add_list
        # just in case
        self.domain_remain_stack = []


    # the constraints method varies from problem to problem
    # this is used to judge if a specific variable with a specific value
    # can be added to the assignment legally
    def constraints(self, variable, value):
        return True

    # similarly as constraints above
    # used to judge if a pair of variables with their values are legal
    def pair_constraint(self, x1, value_x1, x2, value_x2):
        return True

    # to judge if the assignment is complete
    def complete(self):
        for i in range(0, len(self.assignment)):
            if self.assignment[i] == -1:
            # -1 means it has not been valued
               return False
        return True

    def BackTracking_Search(self,
                            select_method = "default",
                            order_method = "default",
                            inference_method = "default"):
        self.clean()
        self.select_method = select_method
        self.order_method = order_method
        self.inference_method = inference_method

        result = self.Recursive_Backtracking()
        self.Print_Solution(result)

    def Recursive_Backtracking(self):
        # first check if it needs further
        if self.complete():
            return True
        # choose the next variable to be explored
        next_variable = self.Select_Unassigned_Variable()
        # order the domain of that variable
        values = self.Order_Domain_Values(next_variable)
        for value in values:
            if self.constraints(next_variable, value):
                self.assignment[next_variable] = value
                # first save the original domin_remain in a stack, we need to restore it later
                saved_remain = copy.deepcopy(self.domain_remain)
                self.domain_remain_stack.append(saved_remain)
                # need to update the domain_remain table
                self.update_domain_remain(next_variable, value)
                # make the inference to end the impossible cases immediately
                infe_res = self.Inference()
                if infe_res == True:
                   # do the steps recursively
                   result = self.Recursive_Backtracking()
                   if result == True:
                      return True
                # unexplored the next_variable and end the recursive part
                self.assignment[next_variable] = -1
                # need to recover the remain table
                self.domain_remain = self.domain_remain_stack.pop()
        return False

    # this function is used to update the domain_remain table when there is a variable been explored
    def update_domain_remain(self, next, value):
        self.domain_remain[next] = [value]
        # need to update the neighbor's remain domains in the table
        neighborlist = self.neighbors[next]
        remove = 0
        for neighbor in neighborlist:
            # if this neighbor has been explored before
            if self.assignment[neighbor] != -1:
                continue
            # for the unexplored neighbors, check if their remaining values are legal
            neighbor_remain = self.domain_remain[neighbor]
            for value in neighbor_remain:
                if self.constraints(neighbor, value) == False:
                    self.domain_remain[neighbor].remove(value)
                    remove += 1
        return remove

    def Select_Unassigned_Variable(self):
        # first we need to get all of the unassigned variables right now
        unassigned = []
        for i in range(0, len(self.assignment)):
            if self.assignment[i] == -1:
                unassigned.append(i)

        if self.select_method == "default":
            return unassigned[0]

        # with MRV we return the unexplored variable with least legal remain values
        elif self.select_method == "MRV":
            remain_min = 999999
            next_explored = unassigned[0]
            for unexplored in unassigned:
                remain = len(self.domain_remain[unexplored])
                if remain < remain_min:
                   remain_min = remain
                   next_explored = unexplored
            return next_explored

        # with degree heuristic we return the unexplored variable with most unexplored neighbors
        elif self.select_method == "degree heuristic":
            constraint_most = 0
            next_explored = unassigned[0]
            for unexplored in unassigned:
                constraint_now = 0
                # find all the unexplored neighbors
                neighborlist = self.neighbors[unexplored]
                for neighbor in neighborlist:
                    if neighbor in unassigned:
                        constraint_now += 1
                if constraint_now > constraint_most:
                    next_explored = unexplored
            return next_explored


    def Order_Domain_Values(self, variable):
        if self.order_method == "default":
            return self.domain_remain[variable]

        # with LCV we should try the value that rules out the fewest values in
        # the remaining variables first
        elif self.order_method == "LCV":
            values = self.domain_remain[variable]
            value_ruleout =[]
            for value in values:
                # we need to try to use this value and see how many values are ruled out
                self.assignment[variable] = value
                saved_remain = copy.deepcopy(self.domain_remain)
                self.domain_remain_stack.append(saved_remain)

                remove = self.update_domain_remain(variable, value)
                value_ruleout.append((value, remove))
                # recovery
                self.assignment[variable] = -1
                self.domain_remain = self.domain_remain_stack.pop()
            value_ruleout.sort(key = lambda x:x[1])
            ordered = []
            for value_pair in value_ruleout:
               ordered.append(value_pair[0])
            return ordered

    def Inference(self):
        if self.inference_method == "default":
            return True

        elif self.inference_method == "AC-3":
            arcs_queue = queue.Queue()
            # first add all the arcs to the queue
            for variable in range(0, len(self.variables)):
                neighborlist = self.neighbors[variable]
                for neighbor in neighborlist:
                    arcs_queue.put((variable, neighbor))

            while arcs_queue.empty() == False:
                arc_out = arcs_queue.get()
                x1 = arc_out[0]
                x2 = arc_out[1]
                # if we have updated the domain_remain (remove values from x1 domain)
                if self.Remove_Inconsistent_Values(x1, x2) == True:
                    # if there is no more remain values in x1
                    if len(self.domain_remain[x1]) == 0:
                        return False
                    # add all the arcs point to x1 to the queue
                    # first find all neighbors of x1
                    neighborlist = self.neighbors[x1]
                    # then add these arcs to the queue
                    for neighbor in neighborlist:
                        arcs_queue.put((neighbor, x1))

            return True

    # the assist function to AC-3, return if there is a change to remain_domain
    def Remove_Inconsistent_Values(self, x1, x2):
        # if there is any pair of values from x1 and x2 satisfies the constraint between x1 and x2
        found = False
        changed = False
        for value_x1 in self.domain_remain[x1]:
            for value_x2 in self.domain_remain[x2]:
                if self.pair_constraint(x1, value_x1, x2, value_x2) == True:
                    found = True

            if found == False:
                # no value in x2 can make a pair with this x1 value, so delete it
                self.domain_remain[x1].remove(value_x1)
                changed = True

        return changed

    # based on the specific problem this can be overwrote
    def Print_Solution(self, result):
        if (result == False):
            print("no solution found to the problem: " + self.name)
        else:
            print("the solution to the problem: " + self.name + " is: ")
            for i in range(0, len(self.variables)):
                solved_value = self.assignment[i]
                print(self.variables[i] + " : " + f"{solved_value}")



# test part
if __name__ == "__main__" :
    variables = ["WA", "NT", "SA", "QL", "NSW", "V", "T"]
    domains = {}
    for variable in range(0, len(variables)):
        domains[variable] = [1, 2, 3]
    neighbors ={}
    neighbors[0] = [1, 2]
    neighbors[1] = [0, 2, 3]
    neighbors[2] = [0, 1, 3, 4, 5]
    neighbors[3] = [1, 2, 4]
    neighbors[4] = [3, 2, 5]
    neighbors[5] = [2, 4]
    neighbors[6] = []

    test_model = CSP_Model(variables, domains, neighbors )
    print(test_model.variables)
    test_model.BackTracking_Search("degree heuristic", "LCV", "AC-3")

