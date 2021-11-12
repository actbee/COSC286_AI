# Author: Xuedan ZOU
# Date: 11/11/2021

from Maze import Maze
from time import sleep
import random
import autograd.numpy as np

class HMM:

    def __init__(self, maze, total_steps):
        self.maze = maze
        self.total_steps = total_steps
        self.robotloc = maze.robotloc

        self.movelist = {"n": (0, 1), "s": (0, -1), "w": (-1, 0), "e": (1, 0)}
        self.color_list = []
        self.action_sequence = []


        # generate the transition table based on the given maze
        size = self.maze.width * self.maze.height
        self.transition_table = []
        add_list = [0] * size
        for i in range(0, size):
            # note that to use copy() here or each line in the table will point to
            # in fact one actual list
            self.transition_table.append(add_list.copy())

        # to each of the location
        for x1 in range(0, self.maze.width):
            for y1 in range(0, self.maze.height):
               # check its nearby locations
               for key in self.movelist.keys():
                   x0 = x1 - self.movelist[key][0]
                   y0 = y1 - self.movelist[key][1]
                   from_index = self.maze.index(x0, y0)
                   to_index = self.maze.index(x1, y1)

                   if self.maze.is_floor(x0, y0):
                       self.transition_table[from_index][to_index] = 0.25
                   else:
                       self.transition_table[to_index][to_index] += 0.25


        # get probability list of each location based on the given color list
        # should be equal probability to each floor initially
        self.probability_list = [0] * size
        total_floor = 0
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if self.maze.is_floor(x, y):
                    total_floor += 1

        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if self.maze.is_floor(x, y):
                    self.probability_list[self.maze.index(x, y)] = 1/total_floor

        # use numpy to help our matrix calculation
        np.array(self.transition_table)
        np.array(self.probability_list)


    # used to update the robot's location pre single step
    def transition(self):
        # change the location of current robot randomly
        action = random.choice(list(self.movelist))
        self.action_sequence.append(action)

        next_x = self.robotloc[0] + self.movelist[action][0]
        next_y = self.robotloc[1] + self.movelist[action][1]
        if self.maze.is_floor(next_x, next_y) :
            self.robotloc[0] = next_x
            self.robotloc[1] = next_y


    # animate the whole process
    def animate_process(self):
        print(str(self.maze))
        sleep(1)
        for i in range(0, self.total_steps):
            # for each step first move the robot
            self.transition()
            self.maze.robotloc = self.robotloc

            print("______________________________________________________________")
            print("step: ", i+1)
            print("try to move: " + self.action_sequence[i])
            print(str(self.maze))

            # then calculate the probability distribution
            self.color_sensor()
            print("the color sequence the robot has got so far is: ")
            print(self.color_list, "\n")
            self.filter()

            # print out the distribution of the probability
            counter = 0
            for value in self.probability_list:
                    counter += 1
                    print(format(value, '2f') + "  ", end = "")
                    if counter == self.maze.width:
                        counter = 0
                        print("\n")
            print("\n")
            sleep(1)


    # with 0.88 probability to get the correct color
    def color_sensor(self):
         x = self.robotloc[0]
         y = self.robotloc[1]
         true_color = self.maze.get_color(x, y)

         color_chance = random.random()
         # if we get the true color
         if color_chance < 0.88:
             self.color_list.append(true_color)
         # equal probability to get each other wrong color
         else:
             remain_color = []
             for color in self.maze.color_domain:
                 if color != true_color:
                     remain_color.append(color)
             self.color_list.append(random.choice(remain_color))


    # do the filter process to get the probability distribution
    def filter(self):
        # transition
        self.probability_list = np.dot(self.probability_list, self.transition_table)
        self.probability_list.tolist()
        # update
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if self.maze.get_color(x, y) == self.color_list[-1] :
                    self.probability_list[self.maze.index(x, y)] *= 0.88
                else:
                    self.probability_list[self.maze.index(x ,y)] *= 0.04

        np.array(self.probability_list)
        # normalize
        sum = np.sum(self.probability_list)
        self.probability_list /= sum

if __name__ == "__main__":
    test_maze = Maze("maze3.maz")
    test_problem = HMM(test_maze, 20)
    # for line in test_problem.transition_table:
    #    print(line)
    print("\n")
    test_problem.animate_process()