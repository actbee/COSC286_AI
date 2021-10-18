# Author: Xuedan ZOU
# Date: 10/1/2021


from Maze import Maze
from time import sleep

class SensorlessProblem:

    def __init__(self, maze):
        self.maze = maze
        self.start_state = set()
        for i in range(0, self.maze.width):
            for j in range(0, self.maze.height):
                if self.maze.is_floor(i, j):
                    self.start_state.add((i, j))


    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def judge_goal(self, state):
        if len(state) == 1:
            return True
        return False

    def get_successors(self, state):
        successors_list = []
        # check all of the four directions
        # first move up
        state_up = set()
        for i in state:
               x = i[0]
               y = i[1] + 1
               if self.maze.is_floor(x, y):
                   state_up.add((x, y))
               else:
                   state_up.add((i[0], i[1]))
        successors_list.append(state_up)

        # then move down
        state_down = set()
        for i in state:
                x = i[0]
                y = i[1] - 1
                if self.maze.is_floor(x, y):
                    state_down.add((x, y))
                else:
                    state_down.add((i[0], i[1]))
        successors_list.append(state_down)

        # then move left
        state_left = set()
        for i in state:
                x = i[0] - 1
                y = i[1]
                if self.maze.is_floor(x, y):
                    state_left.add((x, y))
                else:
                    state_left.add((i[0], i[1]))
        successors_list.append(state_left)

        # finally right
        state_right = set()
        for i in state:
            x = i[0] + 1
            y = i[1]
            if self.maze.is_floor(x, y):
                state_right.add((x, y))
            else:
                state_right.add((i[0], i[1]))
        successors_list.append(state_right)

        return successors_list

    # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        # set the maze's node to -1 so that it only prints out "R" to show the
        # possible robot's location rather than "A","B",...
        self.maze.mode = -1
        for state in path:
            self.maze.robotloc.clear()
            for i in state:
                self.maze.robotloc.append(i[0])
                self.maze.robotloc.append(i[1])
            print(str(self))
            sleep(1)
            print(str(self.maze))

    def get_distance(self, state_a, state_b):
       # each move cost the equal unit of fuel
        return 1

    def area_heuristic(self, state):
       # since all the states should in final be one state, so they should move to the same place finally
       x_max = -1
       x_min = 999
       y_max = -1
       y_min = 999
       for i in state:
           x = i[0]
           y = i[1]
           if(x < x_min):
               x_min = x
           if(x > x_max):
               x_max = x
           if(y < y_min):
               y_min = y
           if(y > y_max):
               y_max = y

       heuristic = abs(x_max - x_min) + abs(y_max - y_min)

       return heuristic

    def distance_heuristic(self, state):
        x_max = -1
        x_min = 999
        y_max = -1
        y_min = 999
        for i in state:
            x = i[0]
            y = i[1]
            if (x < x_min):
                x_min = x
            if (x > x_max):
                x_max = x
            if (y < y_min):
                y_min = y
            if (y > y_max):
                y_max = y

        heuristic = (pow((x_max - x_min), 2) + pow((y_max - y_min), 2)) ** 0.5
        return heuristic

## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)

