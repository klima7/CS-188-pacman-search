# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    visited_states = []
    stack = util.Stack()

    stack.push((problem.getStartState(), []))

    while not stack.isEmpty():
        state, moves = stack.pop()

        if problem.isGoalState(state):
            return moves

        if state not in visited_states:
            visited_states.append(state)

            successors = problem.getSuccessors(state)

            for successor_state, direction, cost in successors:
                if successor_state not in visited_states:
                    stack.push((successor_state, [*moves, direction]))


def breadthFirstSearch(problem):
    visited_states = []
    queue = util.Queue()

    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():
        state, moves = queue.pop()

        if problem.isGoalState(state):
            return moves

        if state not in visited_states:
            visited_states.append(state)

            successors = problem.getSuccessors(state)

            for successor_state, direction, cost in successors:
                if successor_state not in visited_states:
                    queue.push((successor_state, [*moves, direction]))


def uniformCostSearch(problem):
    visited_states = []
    queue = util.PriorityQueue()

    queue.push((problem.getStartState(), [], 0), 0)

    while not queue.isEmpty():
        state, moves, cost = queue.pop()

        if problem.isGoalState(state):
            return moves

        if state not in visited_states:
            visited_states.append(state)

            successors = problem.getSuccessors(state)

            for successor_state, direction, successor_cost in successors:
                if successor_state not in visited_states:
                    queue.push((successor_state, [*moves, direction], cost + successor_cost), cost + successor_cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    start_state = problem.getStartState()

    queue = util.PriorityQueue()
    queue.push(start_state, heuristic(start_state, problem))

    prev_dict = {start_state: None}
    cost_so_far = {start_state: 0}
    closed = set()

    while not queue.isEmpty():
        state = queue.pop()

        if problem.isGoalState(state):
            return _reconstructPath(prev_dict, state)

        if state not in closed:
            for neighbor_state, direction, cost in problem.getSuccessors(state):
                neighbor_cost = cost_so_far[state] + cost
                if neighbor_state not in cost_so_far or neighbor_cost <= cost_so_far[neighbor_state]:
                    cost_so_far[neighbor_state] = neighbor_cost
                    prev_dict[neighbor_state] = (state, direction)
                    queue.push(neighbor_state, neighbor_cost + heuristic(neighbor_state, problem))

        closed.add(state)


def _reconstructPath(prev_dict, goal_state):
    path = []
    current = prev_dict[goal_state]
    while True:
        path.append(current[1])
        current = prev_dict[current[0]]
        if current is None:
            break
    path.reverse()
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
