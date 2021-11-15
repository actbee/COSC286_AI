# Author: Xuedan ZOU
# Date: 11/12/2021

from HMM import HMM
from Maze import Maze

if __name__ == "__main__":
  # change your test maze here
  test_maze = Maze("test3.maz")
  # change the test step here
  test_problem = HMM(test_maze, 20)
  test_problem.animate_process()