# myAgents.py
# ---------------
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
from game import Agent
from searchProblems import PositionSearchProblem
from collections import namedtuple
import util
import time
import search

def mazeDistance(point1, point2, gameState) -> int:
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))


def find_shortest_food(position, gridList):
        val_list = []; least_element = 0; min_val = 99999; result = 0
        for element in gridList:
            val = 0;
            val += abs(position[0] - element[0])
            val += abs(position[1] - element[1])
            val_list.append(val)
            if min_val > val:
                min_val = val
                least_element = element
        gridList.remove(least_element)
        if min_val != 99999:
            return least_element, min(val_list)
        else: 
            return 0


def foodHeuristic(state, problem):
    position = state[0]
    gridList = problem.food
    val = 0
    if len(gridList) > 0:
        for element in gridList:
            val += abs(position[0] - element[0])
            val += abs(position[1] - element[1])
        return val/len(gridList)
    else: 
        return 0







"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='ClosestDotAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]


class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        gridList = food.asList()
        "*** YOUR CODE HERE ***"
        if len(gridList) > 0:
            least_element, min_val = find_shortest_food(startPosition, gridList)
        problem = AnyFoodSearchProblem(gameState, self.index)
        startPosition = least_element
        result = search.ucs(problem)
        return result


    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

    


    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        



"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        gridList = food.asList()
        
        "*** YOUR CODE HERE ***"
        if len(gridList) > 0:
            least_element, min_val = find_shortest_food(startPosition, gridList)
        problem = AnyFoodSearchProblem(gameState, self.index)
        startPosition = least_element
        result = search.ucs(problem)
        return result

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        food = gameState.getFood()
        food = food.asList()
        numAgent = gameState.getNumAgents()
        list_1 = []
        for i in range(numAgent):
            list_1.append(gameState.getPacmanPosition(i))
        self.pacLocation = list_1

        self.food = food
        self.gameState = gameState
        # Store info for the PositionSearchProblem (no need to change this)
        self.agentIndex = agentIndex
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE
    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        (x,y) = state

        "*** YOUR CODE HERE ***"
        if (x,y) in self.food:
            return True
        else:   
            return False

