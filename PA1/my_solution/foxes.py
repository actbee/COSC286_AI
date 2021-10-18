# Author: Xuedan ZOU, 9/25/2021
from FoxProblem import FoxProblem
from uninformed_search import bfs_search, dfs_search, ids_search
# import time

# Create a few test problems:
problem331 = FoxProblem((3, 3, 1))
problem541 = FoxProblem((5, 4, 1))
problem551 = FoxProblem((5, 5, 1))
problem631 = FoxProblem((6, 3, 1))

# Run the searches.
#  Each of the search algorithms should return a SearchSolution object,
#  even if the goal was not found.


if __name__ == "__main__":
  print("running!")

# has commented out the codes to test the running time.
# need to import time before test running time.

# time_begin = time.time()
  print(bfs_search(problem331))
# time_end = time.time()
# print("time past: ")
# print(time_end-time_begin)

  print(dfs_search(problem331))
  print(ids_search(problem331))



  print(bfs_search(problem551))
  print(dfs_search(problem551))
  print(ids_search(problem551))

  print(bfs_search(problem541))
  print(dfs_search(problem541))
  print(ids_search(problem541))

  print(bfs_search(problem631))
  print(dfs_search(problem631))
  print(ids_search(problem631))
