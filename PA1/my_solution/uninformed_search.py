# Author: Xuedan ZOU, 9/25/2021

from collections import deque
from SearchSolution import SearchSolution

# SearchNode class is useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
       self.state = state
       self.parent = parent

    # if the goal is found then give out the path
    def backchaining(self, pass_list=[]):
       list = pass_list
       list.append(self.state)
       if(self.parent != None):
           result_list = self.parent.backchaining(list)
           return result_list
       else:
           return list

    # a recursive way to find if the current state has been visited during dfs
    def path_checking(self, new_state):
        if(self.parent == None):
            if(self.state != new_state):
                return True
            else:
                return False
        else:
            if(self.state == new_state):
                return False
            else:
                return self.parent.path_checking(new_state)


# the bfs search method that does not explore the same state more than once
def bfs_search(search_problem):
    solution = SearchSolution(search_problem, "BFS")
    node = SearchNode(search_problem.start_state, None)
    frontier = deque()
    frontier.append(node)
    explored = set(search_problem.start_state)

    # if there is any node to expand, expand them in the order of a queue
    while len(frontier) != 0 :
        current_node = frontier.popleft()
        current_state = current_node.state
        solution.nodes_visited += 1

        # check if the checked state is the goal, if yes then backchaining to print out the result
        if current_state == search_problem.goal_state :
            path = current_node.backchaining([])
            path.reverse()
            solution.path = path
            return solution

        # add those following nodes that only has not been visited to the frontier
        next_states = search_problem.get_successors(current_state)
        for state in next_states:
            if (state in explored) == False :
                explored.add(state)
                next_node = SearchNode(state, current_node)
                frontier.append(next_node)

    return solution


#  dfs function is recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
# so that statistics like number of nodes visited or recursion depth
# might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

# follows are the base cases
    solution.nodes_visited += 1
    if(node.state == search_problem.goal_state):
        path = node.backchaining([])
        path.reverse()
        solution.path = path
        return solution

    # if the current solution depth is deeper than the limit.
    # here each recursive process the depth_limit minus 1 so when it comes to 0
    # the recursive process should be stopped
    if  depth_limit <= 0 :
        solution.path = []
        return solution

# follows are the recursive cases
    next_states = search_problem.get_successors(node.state)
    for state in next_states :
        if node.path_checking(state) == True :
            child_node = SearchNode(state, node)
            find_solution = dfs_search(search_problem, depth_limit-1, child_node, solution)
            if find_solution.path != [] :
                return find_solution

    return solution

# iterative dfs which is based on the previous dfs but controlling the depth limit
def ids_search(search_problem, depth_limit=100):
    solution = SearchSolution(search_problem, "IDS")
    depth = 0

    while(depth <= depth_limit):
        get_solution = dfs_search(search_problem, depth)
        solution.nodes_visited += get_solution.nodes_visited
        # if the path has been found
        if get_solution.path != [] :
            solution.path = get_solution.path
            return solution
        else:
            depth += 1

    return solution