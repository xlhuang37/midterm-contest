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
from tracemalloc import start
from game import Agent
from util import PriorityQueue
from searchProblems import PositionSearchProblem
from collections import namedtuple
import util
import time
import search
import random
from functools import partial


def find_shortest_food(position, gridList):
        val_list = []; least_element = 0; min_val = 99999; result = 0; 
        for element in gridList:
            val = 0;
            val += abs(position[0] - element[0])
            val += abs(position[1] - element[1])
            val_list.append(val)
            if min_val > val:
                min_val = val
                least_element = element
        if min_val != 99999:
            return least_element, min_val
        else: 
            return 0

def foodHeuristic(state, problem):

    position = state
    val = 0
    val += abs(position[0] - problem.goal[0])
    val += abs(position[1] - problem.goal[1])

    return val

def weirdHeuristic(state, problem):
    position = state
    val = 100
    for i in range(problem.Num):
        pac = problem.gameState.getPacmanPosition(i)
        val += 0.5 ** abs(position[0] - pac[0])
        val += 0.5 ** abs(position[1] - pac[1])
    return val

def manhattanHeuristic(goal, position, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])






"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent_list= ['Pioneer']):
    ret_list = []
    for i in range(num_pacmen):
        index = i%len(agent_list)
        ret_list.append(eval(agent_list[index])(index=i) )
    return ret_list


class Pioneer(Agent):
    """
    Implementation of your agent.
    """
    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        numAgent = gameState.getNumAgents()
        pacPosList = []
        
        for i in range(numAgent):
            pacPosList.append(gameState.getPacmanPosition(i))
        startPosition = pacPosList[self.index]
        pacPosList[self.index] = (999,999)
        
        global food
        gridList = food.asList()
        length = len(gridList)

        "*** YOUR CODE HERE ***"
        
        if length > 0:
            least_element, min_val = find_shortest_food(startPosition, gridList)


            self.destination[0] = least_element

            # for i in range(numAgent):
            #     pacPosList[i] = manhattanHeuristic(pacPosList[i], startPosition)
            # min_pac = min(pacPosList)
            # if min_pac < 7:
            #     decision_goAway = random.randint(0,2)
            #     if decision_goAway == 2:
            #         ran = random.randint(0, length-1)
            #         least_element = gridList[ran]
            #         self.destination[0] = least_element
            #         problem = AnyFoodSearchProblem(gameState = gameState, food = gridList, agentIndex  = self.index, goal = self.destination, goal_val = min_val, agentLocation=pacPosList)
            #         result = search.astar(problem, foodHeuristic)
            #         return result

        problem = AnyFoodSearchProblem(gameState = gameState, food = gridList, agentIndex  = self.index, goal = self.destination, goal_val = min_val, agentLocation=pacPosList)

        before = time.time()
        result = search.astar(problem, foodHeuristic)
        after = time.time()
        return result
        


    def getAction(self, state):
        global food
        food = state.getFood()
        if len(self.actionList) == 0:
            self.actionList = self.findPathToClosestDot(state)
        if food[self.destination[0][0]][self.destination[0][1]] == False:
            self.actionList = self.findPathToClosestDot(state)
        ret_val = self.actionList[0]
        self.actionList = self.actionList[1:]
        return ret_val



    def initialize(self):
        self.actionList = []
        self.destination = [(999,999)]
        self.dest_list = []
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

    def __init__(self, food, gameState, goal, agentIndex,  goal_val, agentLocation):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = food
        self.gameState = gameState
        self.goal = goal[0]
        self.goal_list = goal
        self.goal_val = goal_val
        self.Num = self.gameState.getNumAgents()
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.agentIndex = agentIndex
        self.agentLocation = agentLocation
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.foundPacman = False
        self.costFn = lambda pos: 1
        # if self.agentIndex == 2:
        #     self.costFn = lambda pos: .8 ** pos[1]
        # if self.agentIndex == 3:
        #     self.costFn = lambda pos: 1.2 ** pos[1]
        # if self.agentIndex == 6:
        #     self.costFn = lambda pos: .8 ** pos[0]
        # if self.agentIndex == 7:
        #     self.costFn = lambda pos: 1.2 ** pos[0]
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE
        self.counter = 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """

        (x,y) = state
        
            
        self.counter += 1
        if (x,y) in self.food:

            self.goal_list[0] = (x,y)
            return True
        else:   
            return False
        
        # if self.foundPacman == True:
        #     return False
        
            

        # if (x,y) in self.agentLocation:
        #     self.foundPacman == True

        "*** YOUR CODE HERE ***"