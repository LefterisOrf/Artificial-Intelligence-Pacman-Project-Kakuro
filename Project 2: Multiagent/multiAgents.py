# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        #calculate min distance from ghost
        ghostdistances = []
        for ghost in newGhostStates:
            ghostdistances.append(manhattanDistance(newPos,ghost.getPosition()))
        if ghostdistances:
            score += min(ghostdistances)
        """
        Prosthetw sto score thn apostasi ths neas katastasis apo to kontinotero ghost
        etsi wste, an brisketai makria apo to ghost na thelw na thn epileksw , enw an brisketai
        konta na  mhn prosthetei sxedon tipota (px. 1,2,3)
        """
        #calculate min distance from food
        fooddistances = []
        for food in newFood.asList():
            fooddistances.append(manhattanDistance(newPos,food))
        if fooddistances:
            score -= min(fooddistances)
        """
        Omoiws me to apo panw, an brisketai konta se trofi afairw poly mikro poso, enw an brisketai
        makria afairw megalo , opote tha epilexthei dyskola to neo state
        """
        return score
        
          

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, depth, agentnum, totalagents):
            # Elegxos an pesame se komvo fylo
            if (depth == 0) or (gameState.isLose()) or (gameState.isWin()):
                return self.evaluationFunction(gameState)


            if agentnum == (totalagents - 1): newdepth = depth -1 ##if this agent is the last one , reduce depth by 1
            else : newdepth = depth # else we continue on the same depth until all agents make a move
            actions = gameState.getLegalActions(agentnum)
            succs = []
            for act in actions:
                succs.append(gameState.generateSuccessor(agentnum,act))
            values = []
            for successor in succs:
                values.append(minimax(successor, newdepth, (agentnum+1)%totalagents, totalagents))
            if agentnum == 0: # if our agent is pacman
                return max(values)
            else: # if our agent is a ghost
                return min(values)

        totalagents = gameState.getNumAgents() 
        agentnum = 0
        actions = gameState.getLegalActions(agentnum)
        succs = []
        for act in actions:
            succs.append(gameState.generateSuccessor(agentnum,act))
        values = []
        for successor in succs:
            values.append(minimax(successor, self.depth, (agentnum+1)%totalagents, totalagents))
        maxvalue = max(values)
        #for x in range(len(values)):
        #    print "Action: ",actions[x],"will result in score:",values[x]
        bestpos = [x for x in range(len(values)) if values[x] == maxvalue]
        chosenx = random.choice(bestpos)
        #print "Chosen x is:",chosenx,", with action[x]=",actions[chosenx]
        return actions[chosenx]
        
        util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimax_ab(gameState, depth, agentnum, totalagents, alpha, beta):
            # Elegxos an pesame se komvo fylo
            if (depth == 0) or (gameState.isLose()) or (gameState.isWin()):
                return self.evaluationFunction(gameState)
            if agentnum == (totalagents - 1): newdepth = depth -1 ##if this agent is the last one , reduce depth by 1
            else : newdepth = depth # else we continue on the same depth until all agents make a move
            actions = gameState.getLegalActions(agentnum)
            succs = []
            value = float('inf')
            for act in actions:
                newstate = gameState.generateSuccessor(agentnum, act)
                returnval = minimax_ab(newstate, newdepth, ((agentnum+1)%totalagents), totalagents, alpha, beta)
                if agentnum == 0: # If its pacman run the minimax_ab for max agent
                    if value == float('inf'): value *= -1 # set value to -infinity
                    value = max(value, returnval)
                    if value > beta:
                        return value
                    alpha = max(value, alpha)
                else: # Else if its a ghost run it like a min agent
                    value = min(value, returnval)
                    if value < alpha:
                        return value
                    beta = min(value, beta)
            return value

        totalagents = gameState.getNumAgents()
        agentnum = 0
        actions = gameState.getLegalActions(agentnum)
        alpha = float('-inf')
        beta = float('inf')
        succs = []
        for act in actions:
            succs.append(gameState.generateSuccessor(agentnum,act))
        v = float('-inf')
        values = []
        for successor in succs:
            returnval = minimax_ab(successor, self.depth, (agentnum+1)%totalagents, totalagents, alpha, beta)
            values.append(returnval)
            v = max(v, returnval)
            if v > beta: break
            alpha = max(alpha, v)
        maxvalue = max(values)
        #for x in range(len(values)):
        #    print "Action: ",actions[x],"will result in score:",values[x]
        bestpos = [x for x in range(len(values)) if values[x] == maxvalue]
        chosenx = random.choice(bestpos)
        #print "Chosen x is:",chosenx,", with action[x]=",actions[chosenx]
        return actions[chosenx]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(gameState, depth, agentnum, totalagents):
            # Elegxos an pesame se komvo fylo
            if (depth == 0) or (gameState.isLose()) or (gameState.isWin()):
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentnum)
            succs = []
            for act in actions:
                succs.append(gameState.generateSuccessor(agentnum,act))
            values = []
            if agentnum == 0: # if our agent is pacman
                for successor in succs:
                    values.append(expectimax(successor, depth, (agentnum+1)%totalagents, totalagents))#kalw anadromika gia ton agent 1
                return max(values)
            else: # if our agent is a ghost
                if agentnum == (totalagents - 1): newdepth = depth -1 ##if this agent is the last one , reduce depth by 1
                else : newdepth = depth # else we continue on the same depth until all agents make a move
                for successor in succs:
                    values.append(expectimax(successor, newdepth, ((agentnum+1)%totalagents), totalagents))#kalw anadromika gia ton epomeno agent (eite ghost eite pali ton pacman)
                return sum(values) / len(succs)

        totalagents = gameState.getNumAgents() 
        agentnum = 0
        actions = gameState.getLegalActions(agentnum)
        succs = []
        for act in actions:
            succs.append(gameState.generateSuccessor(agentnum,act))
        values = []
        for successor in succs:
            values.append(expectimax(successor, self.depth, (agentnum+1)%totalagents, totalagents))
        maxvalue = max(values)
        #for x in range(len(values)):
        #    print "Action: ",actions[x],"will result in score:",values[x]
        bestpos = [x for x in range(len(values)) if values[x] == maxvalue]
        chosenx = random.choice(bestpos)
        #print "Chosen x is:",chosenx,", with action[x]=",actions[chosenx]
        return actions[chosenx]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: H ylopoihsh tou betterEvaluationFunction einai arketa paromoia
      me thn evaluationFunction tou erotimatos 1 me moni diafora oti stin sygkekrimeni
      synartisi exw eisagei kai tin pithanotita o pacman na mporei na kanei consume ta
      scared ghosts.
    """
    "*** YOUR CODE HERE ***"


    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    eataghost = 80.0     #if pacman can eat the ghost then give it a high priority
    ghostpriority = 15.0 #Distance from nearest ghost has a higher priority than
    foodpriority = 7.5   #distance from the nearest food (survivability comes first)
    ghostSum = 0
    score = currentGameState.getScore()
    #calculate min distance from ghost
    for ghost in newGhostStates:
        dist = manhattanDistance(newPos,ghost.getPosition())
        if dist != 0:
            if ghost.scaredTimer > 0:
                score += eataghost / dist 
                """ if i can eat the ghost and the ghost is near (dist close to 1)
                then add to score a high value so that the Agent will chose this state"""
            else:                         
                score -= ghostpriority / dist 
    # if a ghost is near pacman then reduce the score value by a lot, so the agent doesnt pick this state
    fooddistances = []
    for food in newFood.asList():
        fooddistances.append(manhattanDistance(newPos,food))
    if fooddistances:
        minfood = min(fooddistances)
        if minfood != 0:
            score += foodpriority / minfood
        """
        Omoiws me to apo panw, an brisketai konta se trofi afairw poly mikro poso, enw an brisketai
        makria afairw megalo , opote tha epilexthei dyskola to neo state
        """
    return score



    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

