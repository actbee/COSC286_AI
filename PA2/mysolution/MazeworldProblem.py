# Author: Xuedan ZOU
# Date: 10/1/2021


from Maze import Maze
from time import sleep
from cmath import sqrt

class MazeworldProblem:

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_state = goal_locations

        # to combine the number of moving robot with robots' position
        self.start_state = (0, ) + tuple(self.maze.robotloc)

    # to see if the current state is the goal state
    def judge_goal(self, state):
        if self.goal_state == state:
           return True
        return False

    # to get the following possible states based on the given state
    def get_successors(self, current_state):
        robot_move = current_state[0]
        robot_x = current_state[robot_move*2+1]
        robot_y = current_state[robot_move*2+2]
        successors_list = []
        robot_num = int(len(self.maze.robotloc)/2)

        # update the robot location list to the current state
        for i in range(0, robot_num):
           self.maze.robotloc[2*i] = current_state[2*i+1]
           self.maze.robotloc[2*i+1] = current_state[2*i+2]

        # robot can just stay in the same place and not move
        next_state_list = []
        for i in current_state:
           next_state_list.append(i)
        next_state_list[0] += 1

        if next_state_list[0] >= robot_num:
            next_state_list[0] = 0

        next_state = tuple(next_state_list)
        successors_list.append(next_state)

        # robot can move left, check it
        can_move = True
        if self.maze.is_floor(robot_x-1, robot_y):
            for i in range(0, robot_num):
               if self.maze.has_robot(robot_x-1, robot_y):
                    can_move = False
        else:
            can_move = False

        if can_move == True:
           next_state_llist = next_state_list.copy()
           next_state_llist[robot_move*2+1] -= 1
           next_state_l = tuple(next_state_llist)
           successors_list.append(tuple(next_state_l))

        # robot can move right, check it
        can_move = True
        if self.maze.is_floor(robot_x+1, robot_y):
            for i in range(0, robot_num):
               if self.maze.has_robot(robot_x+1, robot_y):
                    can_move = False
        else:
            can_move = False

        if can_move == True:
           next_state_rlist = next_state_list.copy()
           next_state_rlist[robot_move*2+1] += 1
           next_state_r = tuple(next_state_rlist)
           successors_list.append(tuple(next_state_r))


        # robot can move up, check it
        can_move = True
        if self.maze.is_floor(robot_x, robot_y+1):
            for i in range(0, robot_num):
               if self.maze.has_robot(robot_x, robot_y+1):
                    can_move = False
        else:
            can_move = False

        if can_move == True:
           next_state_ulist = next_state_list.copy()
           next_state_ulist[robot_move*2+2] += 1
           next_state_u = tuple(next_state_ulist)
           successors_list.append(tuple(next_state_u))


        # robot can move down, check it
        can_move = True
        if self.maze.is_floor(robot_x, robot_y-1):
            for i in range(0, robot_num):
               if self.maze.has_robot(robot_x, robot_y-1):
                    can_move = False
        else:
            can_move = False

        if can_move == True:
           next_state_dlist = next_state_list.copy()
           next_state_dlist[robot_move*2+2] -= 1
           next_state_d = tuple(next_state_dlist)
           successors_list.append(tuple(next_state_d))


        return successors_list


    def __str__(self):
        string =  "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)


    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))


    # to get a capture of the maze image in the given state
    def print_state(self, state):
        robot_num = int(len(self.maze.robotloc)/2)
        for i in range(0, robot_num):
           self.maze.robotloc[2*i] = state[2*i+1]
           self.maze.robotloc[2*i+1] = state[2*i+2]
        print(self.maze)

    # to calculate the manhattan distance between two following states
    def get_distance(self, state_a, state_b):
        move_robot = state_a[0]
        addx = abs(state_b[move_robot*2+1] - state_a[move_robot*2+1])
        addy = abs(state_b[move_robot*2+2] - state_a[move_robot*2+2])
        distance = addx + addy
        return distance

    def manhattan_heuristic(self, state):
       # get the robot that is moving
       move = state[0]
       robot_x = state[move*2+1]
       robot_y = state[move*2+2]
       goal_x = self.goal_state[move*2]
       goal_y = self.goal_state[move*2+1]
       manhanttan = abs(robot_x - goal_x) + abs(robot_y - goal_y)
       return manhanttan

    def actual_heuristic(self, state):
       move = state[0]
       robot_x = state[move*2+1]
       robot_y = state[move*2+2]
       goal_x = self.goal_state[move*2]
       goal_y = self.goal_state[move*2+1]
       actual = (pow((robot_x - goal_x), 2) + pow(abs(robot_y - goal_y), 2)) ** 0.5
       return actual

## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_mp)
    print(test_mp.start_state)
    print(test_mp.maze)

    test_mp.print_state((2, 1, 0, 1, 2, 2, 1))
    print(test_mp.get_successors((2, 1, 0, 1, 2, 2, 1)))
    print(test_mp.get_distance((2, 1, 0, 1, 2, 2, 1), (0, 1, 0, 1, 2, 2, 2)))