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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    def enumerate_valid_node(list_of_successor, frontier, expanded_node):
        counter = 0; branching_counter = 0; 
        while(counter < len(list_of_successor)): # Don't know if I should add it in reverse order
            if list_of_successor[counter][0] not in expanded_node:
                frontier.push(list_of_successor[counter])
                branching_counter += 1
            counter += 1
        return branching_counter
    expanded_node = []; frontier = util.Stack(); list_of_action = []; branching_frame = []
    curr_node = problem.getStartState(); expanded_node.append(curr_node);  # NOTICE THAT LIST OF ACTION IS ONE SMALLER!

    for i in range(400):
        if(problem.isGoalState(curr_node) == True):
            break
        list_of_successor = problem.getSuccessors(curr_node);
        branching_counter = enumerate_valid_node(list_of_successor, frontier, expanded_node)
        while branching_counter == 0:
            list_of_action.pop()
            if len(list_of_action) == 0:
                break
            else:
                successors = problem.getSuccessors(list_of_action[-1][0])
            branching_counter = enumerate_valid_node(successors, frontier, expanded_node)
        successor_to_expand = frontier.pop()
        expanded_node.append(successor_to_expand[0])
        list_of_action.append(successor_to_expand)
        curr_node = expanded_node[-1]
    answer_list = []
    for element in list_of_action:
        answer_list.append(element[1])
   


    return answer_list



    


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    class Node():
        def __init__(self):
            self.prev = None
            self.val = (None,None,None)
    
    def find_path(node, answer_list):
        while node.val[1] != None:
            tem_list = []
            tem_list.append(node.val[1])
            answer_list = tem_list + answer_list
            node = node.prev
        return answer_list
    
        
    expanded_node = []; frontier = util.Queue(); list_of_action = []; curr_node = Node()
    curr_node.val= (problem.getStartState(),None,None); 
    counter = 0; end_node = curr_node;
    list_of_successor = problem.getSuccessors(curr_node.val[0])
    expanded_node.append(curr_node.val[0])

    while(counter < len(list_of_successor)): 
        if list_of_successor[counter][0] not in expanded_node:
            new_node = Node()
            new_node.val = list_of_successor[counter]
            new_node.prev = curr_node
            frontier.push(new_node)
            end_node = new_node
            expanded_node.append(new_node.val[0])
        counter += 1
    for i in range(1000): # I am monitoring steps. use while true in real implementation
        tem_list = []
        while(len(frontier.list) != 0):
            pop_node = frontier.list.pop()
            tem_list.append(pop_node)
        for node in tem_list:
            if problem.isGoalState(node.val[0]) == True:
                end_node = node
                break

            list_of_successor = problem.getSuccessors(node.val[0])
            counter = 0; 
            while(counter < len(list_of_successor)): 
                if list_of_successor[counter][0] not in expanded_node:
                    new_node = Node()
                    new_node.val = list_of_successor[counter]
                    new_node.prev = node
                    frontier.push(new_node)
                    expanded_node.append(new_node.val[0])
                counter += 1
        print(expanded_node)
           

            
        if problem.isGoalState(end_node.val[0]) == True:
            break


    answer_list = []
    answer_list = find_path(end_node, answer_list)
    return answer_list


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    class Node():
        def __init__(self):
            self.prev = None
            self.val = None
            self.cost = None
    
    def find_path(node, answer_list):
        while node != None:
            tem_list = []
            tem_list.append(node.val[1])
            answer_list = tem_list + answer_list
            node = node.prev
        return answer_list
    
    expanded_node = []; frontier = util.PriorityQueue(); list_of_action = []; curr_node = Node()
    curr_node.val= (problem.getStartState(),None,None); 
    counter = 0; end_node = curr_node;
    list_of_successor = problem.getSuccessors(curr_node.val[0])
    expanded_node.append(curr_node.val[0])
    print("before frontier push works")
    while(counter < len(list_of_successor)): 
        new_node = Node()
        new_node.val = (list_of_successor[counter][0], list_of_successor[counter][1], problem.agentIndex)
        cost_list = []; cost_list = find_path(new_node, cost_list)
        new_node.cost = problem.getCostOfActions(cost_list)
        frontier.push(new_node, new_node.cost)
        counter += 1
    chosen_node = frontier.pop()
    end_node = chosen_node
    curr_node = chosen_node

    while True: # I am monitoring steps. use while true in real implementation
        if problem.isGoalState(curr_node.val[0]) == True:
            end_node = curr_node
            break
        if curr_node.val[0] not in expanded_node:
            
            list_of_successor = problem.getSuccessors(curr_node.val[0])
            
            expanded_node.append(curr_node.val[0]);  
            
        else:
            list_of_successor = [];   
        counter = 0;
        while(counter < len(list_of_successor)): 
            if list_of_successor[counter][0] not in expanded_node:
                new_node = Node()
                new_node.val = list_of_successor[counter]
                new_node.prev = curr_node
                cost_list = []; cost_list = find_path(new_node, cost_list)
                new_node.cost = problem.getCostOfActions(cost_list)
                frontier.push(new_node, new_node.cost)
            counter += 1
        chosen_node = frontier.pop()
        end_node = chosen_node
        curr_node = chosen_node
    print("huage while loop  works")


    answer_list = []
    answer_list = find_path(end_node,answer_list)
    return answer_list;


 


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    class Node():
        def __init__(self):
            self.prev = None
            self.val = None
            self.cost = None
    
    def find_path(node, answer_list):
        while node != None:
            tem_list = []
            tem_list.append(node.val[1])
            answer_list = tem_list + answer_list
            node = node.prev
        return answer_list

    expanded_node = []; frontier = util.PriorityQueue(); list_of_action = []; curr_node = Node()
    curr_node.val= (problem.getStartState(),None,None); 
    counter = 0; end_node = curr_node;
    list_of_successor = problem.getSuccessors(curr_node.val[0])
    expanded_node.append(curr_node.val[0])

    
    while(counter < len(list_of_successor)): 
        if list_of_successor[counter][0] not in expanded_node:
            new_node = Node()
            new_node.val = list_of_successor[counter]
            cost_list = []; cost_list = find_path(new_node, cost_list)
            new_node.cost = problem.getCostOfActions(cost_list)
            heuristic_cost = heuristic(new_node.val[0], problem)
            new_node.cost += heuristic_cost
            frontier.push(new_node, new_node.cost)
        counter += 1
    chosen_node = frontier.pop()
    end_node = chosen_node
    curr_node = chosen_node


    while True: # I am monitoring steps. use while true in real implementation
        if problem.isGoalState(curr_node.val[0]) == True:
            end_node = curr_node
            break
        if curr_node.val[0] not in expanded_node:
            list_of_successor = problem.getSuccessors(curr_node.val[0])
            expanded_node.append(curr_node.val[0]);  
        else:
            list_of_successor = [];
        counter = 0;
        while(counter < len(list_of_successor)): 
            if list_of_successor[counter][0] not in expanded_node:
                new_node = Node()
                new_node.val = list_of_successor[counter]
                new_node.prev = curr_node
                cost_list = []; cost_list = find_path(new_node, cost_list)
                new_node.cost = problem.getCostOfActions(cost_list)
                heuristic_cost = heuristic(new_node.val[0], problem)
                new_node.cost += heuristic_cost
                frontier.push(new_node, new_node.cost)
            counter += 1
        chosen_node = frontier.pop()
        end_node = chosen_node
        curr_node = chosen_node

    print("end of astar")
    answer_list = []
    answer_list = find_path(end_node,answer_list)
    print(answer_list)
    return answer_list;




    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
