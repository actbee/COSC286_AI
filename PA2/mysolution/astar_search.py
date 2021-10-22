# Author: Xuedan ZOU
# Date: 10/1/2021

from SearchSolution import SearchSolution
from heapq import heappush, heappop, heapify

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        return self.transition_cost + self.heuristic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []

    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # visited_cost are stored as dictionary, note that states should be tuple to be hashed
    visited_cost = {}
    visited_cost[tuple(start_node.state)] = 0
    # note that here we can not make sure every state is saved as a tuple so we first transfer them to tuple in visited_cost

    while 1:
        # if there is no new node from the frontier
        if len(pqueue) == 0 :
            solution.path = []
            return solution

        # get the new node
        current_node = heappop(pqueue)
        current_state = current_node.state
        solution.nodes_visited += 1

        # mark that we have visited this node with its cost
        visited_cost[tuple(current_node.state)] = current_node.transition_cost

        # if we find the goal
        if search_problem.judge_goal(current_state) :
            solution.path = backchain(current_node)
            solution.cost = visited_cost[tuple(current_node.state)]
            return solution

        # get the successor states
        for next_state in search_problem.get_successors(current_state):
            # use node to save the successor states
            child_node = AstarNode(next_state, heuristic_fn(next_state), current_node,
                                   visited_cost[tuple(current_state)] + search_problem.get_distance(current_state, next_state))
            child_state = child_node.state

            # we only add those unvisited nodes
            if  tuple(child_state) in visited_cost:
               continue

            else:
              # to see if the child_node is in the heap
              found_child = False
              for i in pqueue:
                if child_node.state == i.state:
                    found_child = True
                    # when the new one costs less than the old one
                    if child_node < i:
                        # replace the old node with the new one:
                        i = pqueue[-1]
                        pqueue.pop()
                        heapify(pqueue)
                        heappush(pqueue, child_node)

              if found_child == False :
                  heappush(pqueue, child_node)





