# Author: Xuedan ZOU
# Date: 10/1/2021

from SensorlessProblem import SensorlessProblem
from Maze import Maze

from astar_search import astar_search

def null_heuristic(state):
    return 0

# Test problems

if __name__ == "__main__":
    '''
    test_maze = Maze("maze_sensor6.maz")
    test_sl = SensorlessProblem(test_maze)
    print(test_sl.maze)
    result = astar_search(test_sl, test_sl.area_heuristic)
    print(result)
    test_sl.animate_path(result.path)
    '''
    test_maze = Maze("maze_sensor6.maz")
    test_sl = SensorlessProblem(test_maze)
    print(test_sl.maze)
    # result = astar_search(test_sl, test_sl.distance_heuristic)
    result = astar_search(test_sl, test_sl.area_heuristic)
    print(result)
    test_sl.animate_path(result.path)