# Author: Xuedan ZOU
# Date: 10/28/2021

import random

class SAT:
    def __init__ (self, variables_num, cnf):
       # normally we still count index from 1
       self.variables_num = variables_num
       self.assignment = [0, ]
       for i in range(0, variables_num):
            # give the initial assignment 1 or -1 randomly
            random_value = random.uniform(0, 1)
            if random_value > 0.5:
               self.assignment.append(1)
            else:
               self.assignment.append(-1)
       self.cnf =  cnf
       # use to save the clauses that are unsatisfied during the SAT process
       self.unsatisfied = []

    # count how many clause are true given the assignment
    def clause_satisfy(self):

        clause_true = 0
        self.unsatisfied = []
        for clause in self.cnf:
            # for each clause at least one term is true
            is_true = False
            for i in clause:
                index = abs(i)
                if i > 0:
                    bool = 1
                else:
                    bool = -1
                if self.assignment[index] == bool:
                    clause_true += 1
                    is_true = True
                    break
            # if this clause is false, then add it to the unsatisfied list
            if is_true == False:
                self.unsatisfied.append(clause)

        return clause_true


    def judge_end(self):
           # all clauses should be true
           clause_true = self.clause_satisfy()
           if clause_true == len(self.cnf):
               return True
           else:
               return False

    def GSAT(self, h, max_times):
        # we have a random assignment already as we have initialized it before
        # see if it satisfies all the clauses
        count_time = 0
        self.unsatisfied = []
        found = False
        while count_time < max_times:

           if self.judge_end() == True:
               found = True
               break

           count_time += 1
           #  pick a number between 0 and 1 and see if it is greater than some
           #  threshold h
           random_pick = random.uniform(0, 1)
           if random_pick > h:
               random_flip = random.randint(1, self.variables_num)
               self.assignment[random_flip] *= -1
           else:
               flip_count = {}
               for i in range(1, self.variables_num + 1):
                  # score how many clauses can be true if one of the variable
                  # is fliped
                  self.assignment[i] *= -1
                  flip_count[i] = self.clause_satisfy()
                  self.assignment[i] *= -1
               # then we create a list to save those indexs of variable with the greatest value
               # first reorder our dictionary and store it as a list
               orderlist = sorted(flip_count.items(), key = lambda item: item[1], reverse = True)
               most_list = []
               # get the greatest value
               most_value = orderlist[0][1]
               # add those indexs of varible with the greatest value to our list
               for i in orderlist:
                   if i[1] == most_value:
                       most_list.append(i[0])
                   else:
                       break

               random_flip = random.choice(most_list)
               self.assignment[random_flip] *= -1

           print(count_time)

        return found

    def WalkSAT(self, h, max_times):
        count_time = 0
        self.unsatisfied = []
        found = False
        while count_time < max_times:

            if self.judge_end() == True:
                found = True
                break

            count_time += 1
            # pick a clause randomly from the unsatisfied clauses
            pick_clause = random.choice(self.unsatisfied)
            # the following steps are similar to GSAT
            random_pick = random.uniform(0, 1)
            if random_pick > h:
                # choose that flip value from the random picked clause
                random_flip_value = random.choice(pick_clause)
                self.assignment[abs(random_flip_value)] *= -1
            else:
                flip_count = {}
                for value in pick_clause:
                    i = abs(value)
                    self.assignment[i] *= -1
                    flip_count[i] = self.clause_satisfy()
                    self.assignment[i] *= -1

                orderlist = sorted(flip_count.items(), key=lambda item: item[1], reverse=True)
                # print(orderlist)
                most_list = []
                most_value = orderlist[0][1]
                for i in orderlist:
                    if i[1] == most_value:
                        most_list.append(i[0])
                    else:
                        break

                random_flip = random.choice(most_list)
                self.assignment[random_flip] *= -1

            print(count_time)

        return found



