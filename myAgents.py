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
import random


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
        if min_val != 99999:
            return least_element, min(val_list)
        else: 
            return 0



def foodHeuristic(state, problem):
    position = state
    val = 0
    for i in range(1):
        val += abs(position[0] - problem.goal[0])
        val += abs(position[1] - problem.goal[1])
    return val


def manhattanHeuristic(position, goal, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])






"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent_1='MyAgent'):
    return [eval(agent_1)(index=i) for i in range(num_pacmen)]


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
        wall = gameState.getWalls()
        wallList = wall.asList()
        "*** YOUR CODE HERE ***"
        if len(gridList) > 0:
            least_element, min_val = find_shortest_food(startPosition, gridList)
        # least_in_range = 0; least_val = 99999;
        # if min_val > 6:
        #     for i in range(-3,7):
        #         for j in range(-3,7):
        #             if (least_element[0]+i) >= 0 and (least_element[1]+j) >= 0:
        #                 some_ele = ((least_element[0]+i), (least_element[1]+j))
        #                 val = manhattanHeuristic(some_ele, least_element)
        #                 if least_val > val and some_ele not in wallList:
        #                     least_val = val
        #                     least_in_range = some_ele

        #     problem = AnyFoodSearchProblem(gameState = gameState, food = gridList, agentIndex  = self.index, goal = least_in_range)
        problem = AnyFoodSearchProblem(gameState = gameState, food = gridList, agentIndex  = self.index, goal = least_element)
       
        startPosition = least_element

        result = search.astar(problem, foodHeuristic)
        print(result)
        return result

    def getAction(self, state):
        if len(self.actionList)== 0:
            self.actionList = self.findPathToClosestDot(state)
        ret_val = self.actionList[0]
        self.actionList = self.actionList[1:]
        return ret_val


    


    def initialize(self):
        self.actionList = []
        self.counter
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
        problem = AnyFoodSearchProblem(gameState = gameState, food = gridList, agentIndex  = self.index, goal = least_element)
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

    def __init__(self, food, gameState, goal, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        numAgent = gameState.getNumAgents()
        print("Afterfood")
        self.food = food
        
        self.gameState = gameState
        self.goal = goal
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
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

