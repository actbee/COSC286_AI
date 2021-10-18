# Author: Xuedan ZOU, 9/25/2021

# the class FoxProblem is used to save the constants of the problem
# and the way to generate the successor states from any given state
class FoxProblem:
    # triple refers to (chicken,fox,boat) number on one side
    def __init__(self, start_state=(3, 3, 1)):
        # check if the start_state is valid
        assert (start_state[1] <= start_state[0]), "Foxes are more than chickens at first!"

        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_chicken = start_state[0]
        self.total_fox = start_state[1]


    # get successor states for the given state
    def get_successors(self, state):
        successors_list = []
        current_chicken = state[0]
        current_fox = state[1]
        current_boat = state[2]

        # just in case, check if the given state is correct
        assert self.checksafe(state), "ERROR, current state is not safe!"

        # check the side of the boat
        # if the boat is on the current side then based on the current state:
        # 1 foxes and 1 chickens, 2 foxes, 2 chickens, 1 fox or 1 chicken can
        # be on the boat and go to the other side.
        if(current_boat == 1):
            if(current_chicken >= 2):
                next_state = (current_chicken - 2, current_fox, current_boat - 1)
                if(self.checksafe(next_state)):
                    successors_list.append(next_state)

            if(current_fox >= 2):
                next_state = (current_chicken, current_fox - 2, current_boat - 1)
                if(self.checksafe(next_state)):
                    successors_list.append(next_state)

            if(current_chicken >= 1):
                next_state = (current_chicken - 1, current_fox, current_boat - 1)
                if (self.checksafe(next_state)):
                    successors_list.append(next_state)

            if(current_fox >= 1):
                next_state = (current_chicken, current_fox - 1, current_boat - 1)
                if(self.checksafe(next_state)):
                    successors_list.append(next_state)

            if(current_fox >= 1 and current_fox >= 1):
                next_state = (current_chicken - 1, current_fox - 1, current_boat - 1)
                if (self.checksafe(next_state)):
                    successors_list.append(next_state)

        # if the boat is on the other side then at most 2 animals will be
        # added to this side.
        else:
            opposite_chicken = self.total_chicken - current_chicken
            opposite_fox = self.total_fox - current_fox
            if(opposite_chicken >= 1 and opposite_fox >= 1):
               next_state = (current_chicken + 1, current_fox + 1, current_boat + 1)
               if (self.checksafe(next_state)):
                   successors_list.append(next_state)

            if(opposite_chicken >= 1):
               next_state = (current_chicken + 1, current_fox, current_boat + 1)
               if (self.checksafe(next_state)):
                   successors_list.append(next_state)

            if(opposite_chicken >= 2):
               next_state = (current_chicken + 2, current_fox, current_boat + 1)
               if (self.checksafe(next_state)):
                   successors_list.append(next_state)

            if(opposite_fox >= 1):
               next_state = (current_chicken, current_fox + 1, current_boat + 1)
               if (self.checksafe(next_state)):
                   successors_list.append(next_state)
                # note that here since the foxes added we should check the state is
                # safe or not. The same as follows.

            if(opposite_fox >= 2):
               next_state = (current_chicken, current_fox + 2, current_boat + 1)
               if (self.checksafe(next_state)):
                   successors_list.append(next_state)

        return successors_list


    # check if current state is valid
    def checksafe(self, state):
        # if there are more foxes than the chickens on one side then this state is unsafe and foxes will eat those chickens
        chicken = state[0]
        fox = state[1]
        op_chicken = self.total_chicken - chicken
        op_fox = self.total_fox - fox

        # obviously if each side there exists chicken and foxes are more than the chickens then it is not safe
        if (fox > chicken and chicken != 0):
            return False
        elif(op_fox > op_chicken and op_chicken != 0):
            return False
        else:
            return True


    # to see if the given state arrives the goal state
    def goal_test(self, state):
        if(state == self.goal_state):
            return True
        else:
            return False


    def __str__(self):
        string = "Chickens and foxes problem: "+ str(self.start_state)
        return string

'''
if __name__ == "__main__":
     test_cp = FoxProblem((3, 3, 1))
     print(test_cp.get_successors((2, 2, 0)))
     print(test_cp)
'''


