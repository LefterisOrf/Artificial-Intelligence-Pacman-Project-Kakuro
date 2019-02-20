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

def PathFunction(diction, goal, problem):
	# Sinarthsh poy dexetai to dictionary poy paraxthike stin ekastote SearchFunction
	# kai epistrefei to monopati tis lisis diatrexontas to
	path = util.Queue()
	while (goal != None) and (goal != problem.getStartState()):
		path.push(diction[goal][1])
		goal = diction[goal][0]
	return path.list


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    from util import Queue
    fringe = Stack()
    vis = Stack() # Stack gia na gnwrizw toys komvoys poy exoyme episkefthei
    diction = {} # Dictionary gia na brw to monopati tis lisis
    """
    Sto dictionary krataw gia kathe komvo ton patera toy kai tin  
    kinisi poy ekana apo ton patera gia na brethw se ayton ton komvo
    """
    goal = None
    startn = problem.getStartState()
    diction[startn] = (None, None)
    fringe.push(startn)
    while (fringe.isEmpty() == 0):
        father = fringe.pop()
        if problem.isGoalState(father):# elegxos an o komvos einai komvos-stoxos
            goal = father
            break
        if father not in vis.list:
            vis.push(father)
            for i in problem.getSuccessors(father):
                if i[0] not in vis.list:# gia kathe successor elegxos an exei episkefthei
                    fringe.push(i[0])# an den exei episkefthei eisagetai sto fringe
                    diction[i[0]] = (father,i[1])#neo entry sto dictionary
    return PathFunction(diction, goal, problem)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Stack
    from util import Queue
    fringe = Queue()
    vis = set()
    diction = {}
    goal = None
    startn = problem.getStartState()
    diction[startn] = (None, None)
    fringe.push(startn)
    while (fringe.isEmpty() == 0):
        father = fringe.pop()
        if problem.isGoalState(father):#elegxos an o komvos einai komvos-stoxos
            goal = father
            break
        if (father not in vis) and (father not in fringe.list):
            vis.add(father)
            for child in problem.getSuccessors(father):
                if (child[0] not in vis) and (child[0] not in fringe.list):
                    fringe.push(child[0])
                    diction[child[0]] = (father,child[1])
    return PathFunction(diction, goal, problem)
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import Queue
    cost = 0
    fringe = PriorityQueue()
    itemsinheap = set()#Xrisimopoiw to itemsinheap set gia na elegksw an enas komvos brisketai sto PriorityQueue
    visited = set()
    diction = {}# To dictionary periexei ton patera, to action kai to kostos mexri ekeino ton komvo
    goal = None
    startn = problem.getStartState()
    diction[startn] = (None, None, 0)
    fringe.push(startn, cost)
    itemsinheap.add(startn)
    while (fringe.isEmpty() == 0):
        father = fringe.pop()
        itemsinheap.remove(father)
        if problem.isGoalState(father):
            goal = father
            break
        if (father not in visited) and (father not in itemsinheap):
            visited.add(father)
            for child in problem.getSuccessors(father):
                cost = diction[father][2] + child[2]#diction[father][2] the cost of the path till the father
                if (child[0] not in visited) and (child[0] not in itemsinheap):
                    fringe.push(child[0], cost)
                    itemsinheap.add(child[0])
                    diction[child[0]] = (father, child[1], cost)
                else:
                    if (child[0] in itemsinheap) and (cost < diction[(child[0])][2]):# an to neo kostos einai mikrotero tote update
                        fringe.update(child[0], cost)
                        diction[child[0]] = (father, child[1], cost)
    return PathFunction(diction, goal, problem)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import Queue
    cost = 0
    fringe = PriorityQueue()
    """
    Ta stoixeia poy eisagontai sto PriorityQueue exoyn ws timi to pragmatiko kostos
    mexri ayta + to kostos tis eyristikis mexri ton komvo-stoxo
    """
    itemsinheap = set()
    visited = set()#I use visited set to check if a node (x,y) coordinate is in the PriorityQueue
    diction = {}
    goal = None
    startn = problem.getStartState()
    diction[startn] = (None, None, 0)# father, action , cost
    fringe.push(startn, heuristic(startn,problem))
    itemsinheap.add(startn)
    while (fringe.isEmpty() == 0):
        father = fringe.pop()
        itemsinheap.remove(father)
        if problem.isGoalState(father):
            goal = father
            break
        if (father in visited) or (father in itemsinheap):
            continue
        visited.add(father)
        for child in problem.getSuccessors(father):
            if(child[0] not in visited):
                cost = diction[father][2] + child[2]# diction[father][2] the cost of the path till the father
                funcost = heuristic(child[0],problem)
                if (child[0] not in itemsinheap):
                    fringe.push(child[0], (funcost + cost))
                    itemsinheap.add(child[0])
                    diction[child[0]] = (father, child[1], cost )
                elif ((funcost + cost) < ((diction[(child[0])][2]) + heuristic(child[0], problem))):
                	# An to neo synoliko kostos einai mikrotero kane update kai to fringe kai to dictionary
                    fringe.update(child[0], funcost + cost)
                    diction[child[0]] = (father, child[1], cost)
    return PathFunction(diction, goal, problem)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
