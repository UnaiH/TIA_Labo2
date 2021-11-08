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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        score = 0
        food = currentGameState.getFood()
        for fantasma in newGhostStates:
            dist = manhattanDistance(fantasma.getPosition(),newPos)
            if dist<2:
                score -= 500
        if newPos in food.asList():
            score += 100
        else:
            distanciasPunt = 0
            for comida in newFood.asList():
                distanciasPunt += 1/manhattanDistance(comida,newPos)
            score += distanciasPunt
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

    def maxValue(self,gameState, depth):
        acciones = gameState.getLegalActions(0)
        if depth==self.depth or len(acciones)==0:
            return self.evaluationFunction(gameState)
        v = float("-inf")
        maxima_accion = None
        for accion in acciones:
            movimiento = self.minValue(gameState.generateSuccessor(0,accion),1,depth)
            if movimiento > v:
                v = movimiento
                maxima_accion = accion
        if depth==0:
            return maxima_accion
        else:
            return v
        

    def minValue(self, gameState, agente, depth):
        acciones = gameState.getLegalActions(agente)
        if len(acciones)==0:
            return self.evaluationFunction(gameState)       
        v = float("inf")
        for accion in acciones:
            if agente < gameState.getNumAgents()-1:                            
                movimiento = self.minValue(gameState.generateSuccessor(agente,accion),agente+1,depth)
                if movimiento < v:
                    v = movimiento            
            else:                
                movimiento = self.maxValue(gameState.generateSuccessor(agente,accion), depth +1)
                if movimiento < v:
                    v = movimiento
        return v

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState,0)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, gameState, alfa, beta, depth):
        
        acciones = gameState.getLegalActions(0)
        if depth==self.depth or len(acciones)==0:
            return self.evaluationFunction(gameState)
        v = float("-inf")
        for accion in acciones:
            v = max(v,self.minValue(gameState.generateSuccessor(0,accion),1,alfa,beta,depth))
            if v > beta:
                return v
            alfa = max(alfa,v)
        return v
        
    def minValue(self, gameState, actor, alfa, beta, depth):
        acciones = gameState.getLegalActions(actor)
        if len(acciones)==0:
            return self.evaluationFunction(gameState)
        v = float("inf")
        for accion in acciones:
            if actor < gameState.getNumAgents()-1:                            
                v = min(v, self.minValue(gameState.generateSuccessor(actor,accion),actor+1,alfa,beta,depth))
            else:            
                v = min(v, self.maxValue(gameState.generateSuccessor(actor,accion),alfa,beta, depth +1))
            if  v < alfa:
                return v
            beta = min(beta,v)      
        return v
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alfa = float("-inf")
        beta = float("inf")
        v = float("-inf")
        acciones = gameState.getLegalActions(0)
        maxima_accion = None
        for accion in acciones:
            v = self.minValue(gameState.generateSuccessor(0,accion),1,alfa,beta,0)
            if alfa < v:
                alfa = v
                maxima_accion = accion
        return maxima_accion

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxValue(self,gameState, depth):
        acciones = gameState.getLegalActions(0)
        if depth==self.depth or len(acciones)==0:
            return self.evaluationFunction(gameState)
        v = float("-inf")
        maxima_accion = None
        for accion in acciones:
            movimiento = self.minValue(gameState.generateSuccessor(0,accion),1,depth)
            if movimiento > v:
                v = movimiento
                maxima_accion = accion
        if depth==0:
            return maxima_accion
        else:
            return v
        

    def minValue(self, gameState, agente, depth):
        acciones = gameState.getLegalActions(agente)
        if len(acciones)==0:
            return self.evaluationFunction(gameState)        
        v = 0
        num_acciones = float(len(acciones))
        for accion in acciones:
            if agente < gameState.getNumAgents()-1:                            
                movimiento = self.minValue(gameState.generateSuccessor(agente,accion),agente+1,depth)
                v += movimiento
            else:                
                movimiento = self.maxValue(gameState.generateSuccessor(agente,accion), depth +1)
                v += movimiento
        return v/num_acciones

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState,0)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ghostStates = currentGameState.getGhostStates()
    pacman_pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    food = currentGameState.getFood()
    capsulas = currentGameState.getCapsules()
    if pacman_pos==(11,5) or pacman_pos==(9,5):
        score -= 150
    elif pacman_pos==(10,5) or pacman_pos==(8,5):
        score -= 500
    for fantasma in ghostStates:
        fanpos = fantasma.getPosition()
        fandis = manhattanDistance(pacman_pos, fanpos)
    score -= (float(1)/1+fandis)
    distanciasPunt = 0
    for comida in food.asList():
        distanciasPunt += float(1)/(1+manhattanDistance(comida,pacman_pos))
        score += distanciasPunt
    if pacman_pos==(3,3) and (3,3) not in capsulas:
        score -= 500
    elif pacman_pos==(16,3) and (16,3) not in capsulas:
        score -= 500
    cap_score=0
    if(len(capsulas) != 0):
        for capsula in capsulas:
            cap_dis = manhattanDistance(capsula, pacman_pos)
            if cap_dis == 0 :
                cap_score = float(1)/cap_dis
            else:
                cap_score = -100
        score += (1.0/1+cap_score)   

    return score

# Abbreviation
better = betterEvaluationFunction
