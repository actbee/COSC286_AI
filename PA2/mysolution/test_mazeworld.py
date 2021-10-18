# Author: Xuedan ZOU
# Date: 10/1/2021


from MazeworldProblem import MazeworldProblem
from Maze import Maze

from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


# Test problems

if __name__ == "__main__":

  '''
  test_maze3 = Maze("maze3.maz")
  test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
  print(test_mp.maze)
  print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
  result = astar_search(test_mp, null_heuristic)
  print(result)
  
# this should do a bit better:
  result = astar_search(test_mp, test_mp.manhattan_heuristic)
  print(result)
  test_mp.animate_path(result.path)
  '''

# Your additional tests here:

  test_maze7 = Maze("maze7.maz")
  test_mp2 = MazeworldProblem(test_maze7, (0, 3, 4, 1, 0))
  print(test_mp2.maze)
  result = astar_search(test_mp2, test_mp2.manhattan_heuristic)
  print(result)
  result2 = astar_search(test_mp2, null_heuristic)
  print(result2)
  result3 = astar_search(test_mp2, test_mp2.actual_heuristic)
  print(result3)
  test_mp2.animate_path(result.path)


  '''
  test_maze4 = Maze("maze4.maz")
  test_mp4 = MazeworldProblem(test_maze4, (0, 3, 3, 2, 4, 3, 0))
  print(test_mp4.maze)
  result = astar_search(test_mp4, null_heuristic)
  print(result)
  test_mp4.animate_path(result.path)
  '''