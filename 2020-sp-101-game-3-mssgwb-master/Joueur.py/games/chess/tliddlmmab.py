from games.chess.functions import *
import time
import random

#global chess peaces for iddlmm to function off of
CHESS_PEACES = ["p", "r", "n", "b", "q", "k"]


# itterative deepining depth-limited miniMax
# main driver
# returns best move calculated by the algorithm
def tliddlmmab(chessBoard, playerColor, timeRemaining, moveHistory):
    # settings for iddlmm
    scoredMovesDictionary = {}
    initalMove = ""
    initalScore = 0
    startingDepth = 0
    alpha = -9999999999
    beta = 9999999999
    maxDepthToGo = 100
    TimeTaken = 0
    lastAction = predictMoveTime
    maxTimeInNanoseconds = 900000000000

    # set time limit
    AllotedTime = (predictMoveTime(moveHistory, timeRemaining, maxTimeInNanoseconds)) / (10**9)

    # Generate inital actions for root node
    #   wrap in for loop to gradually increase to maxDeapth
    for maxDepth in range(0, maxDepthToGo):
        start = time.time()
        if maxDepth == 0:
            actions = generateActions(playerColor, chessBoard)
            scoredMovesDictionary = calculateBoardScoring(chessBoard, actions)
            initalScore, initalMove = minMaxValueSet(scoredMovesDictionary, startingDepth)

        actionPair = miniMax(chessBoard, playerColor, initalMove, initalScore, alpha, beta, startingDepth, maxDepth)
        
        # tracking time
        TimeElapsed = time.time() - start
        TimeTaken = TimeTaken + TimeElapsed

        # if 5 timex time taken gt allotedTime (timeLimit) then dont go to next level
        # on avrage each increase in depth is 4 times the previous level
        if (5*TimeTaken > AllotedTime):
            break
    return actionPair

# recursive function for minimax
# returns score and move combination of the max depth
def miniMax(chessBoard, playerColor, parentNodeMove, currentScore, alpha, beta, depth, maxDepth):
    selectedPair = ()
    # dictionary of moves
    scoredMovesDictionary = {}
    bestMoves = {}
    miniMaxScore = 0
    heuristicValue = 0

    # basecase recursion combo breaker
    if (depth == maxDepth):
        return (currentScore, parentNodeMove)


    # who is enemy 
    if (playerColor == "white"):
        Enemy = "black"
    else:
        Enemy = "white"

    # generate all actions for the current board
    actions = generateActions(playerColor, chessBoard)

    # board failed to generate Moves so its trashed
    if len(actions) == 0:
        return (currentScore, parentNodeMove)
    # make score of all moves 
    scoredMovesDictionary = calculateBoardScoring(chessBoard, actions)


    # itterate through all actions to create child nodes from indavidual moves
    for action in actions:
        #build child board
        newChessBoard = postMoveBoardGenerator(chessBoard, action)
        # actionValue from move in child board
        for key, values in scoredMovesDictionary.items(): 
            if action in values:
                actionScore = key
                break
        
        childrenScoreMovePair = miniMax(newChessBoard, Enemy, action, actionScore, alpha, beta, depth + 1, maxDepth)
        heuristicValue = heuristicCalculation(depth, actionScore, childrenScoreMovePair[0])

        # alpha beta calculations
        if depth % 2 == 0:
            alpha = max(alpha, heuristicValue)
        else:
            beta = min(beta, heuristicValue)

        if beta <= alpha:
            return (heuristicValue, action)

        # # add heuristicValue to dictionary
        if heuristicValue not in bestMoves:
            bestMoves[heuristicValue] = []
        bestMoves[heuristicValue] = bestMoves[heuristicValue] + [action]

        # min max value of bestMoves
        selectedPair = minMaxValueSet(bestMoves, depth)

        bestMoves = {}
        # only need ot keep the last best move for the next loop
        bestMoves[selectedPair[0]] = [selectedPair[1]]
    return selectedPair


# evaluates moves and stores them according to score
# returns dictionary score: listOfMoves
def calculateBoardScoring(chessBoard, actions):
    CHESS_PEACE_VALUES = {"p": 1, "n":3, "b": 3, "r": 5, "q": 9, "k":10}
    scoreDictionary = {}
    for action in actions:
        move = uciToCoordinates(action)
        capturedValue = 0
        capturedPeace = chessBoard[move[2]][move[3]]
        if capturedPeace.lower() in CHESS_PEACES:
            capturedValue = CHESS_PEACE_VALUES[capturedPeace.lower()]
            if capturedValue not in scoreDictionary:
                scoreDictionary[capturedValue] = []
            scoreDictionary[capturedValue] = scoreDictionary[capturedValue] + [action]
        elif capturedPeace == ".":
            if capturedValue not in scoreDictionary:
                scoreDictionary[capturedValue] = []
            scoreDictionary[capturedValue] = scoreDictionary[capturedValue] + [action]

    return scoreDictionary

# heuristic calculation based on lecture video of zeroSumGain
# returns heuristiv value
def heuristicCalculation(depth, parentScore, childScore):
    zeroSumGain = 0
    if depth % 2 == 0:
        zeroSumGain = childScore + parentScore
    else:
        zeroSumGain = childScore - parentScore
    return zeroSumGain

# Generate a new Board after playing a single move
# returns chess board after move has been made
def postMoveBoardGenerator(chessBoard, moveToMake):
    newChessBoard  = [[j for j in chessBoard[i]] for i in range(len(chessBoard))] 
    moveToMakeCoordiantes = uciToCoordinates(moveToMake)
    oldPossition = (moveToMakeCoordiantes[0], moveToMakeCoordiantes[1])
    chessPeaceToMove = newChessBoard[oldPossition[0]][oldPossition[1]]
    newChessBoard[oldPossition[0]][oldPossition[1]] = "."
    newPossiton = (moveToMakeCoordiantes[2], moveToMakeCoordiantes[3])
    newChessBoard[newPossiton[0]][newPossiton[1]] = chessPeaceToMove
    return newChessBoard

# select min or max depending on who is playing
# returns tuple of score, move
def minMaxValueSet(scoreDictionary, depth):
    score = 0
    selectedMove = ""
    # find max
    if depth % 2 == 0:
        score = max(scoreDictionary)
    else:
        score = min(scoreDictionary)
    
    listOfMoveForScore = scoreDictionary[score]

    if len(listOfMoveForScore) > 1:
        selectedMove = random.choice(listOfMoveForScore)
    else:
        selectedMove = listOfMoveForScore[0]

    return (score, selectedMove)


# predict move time
# returns a time
def predictMoveTime(moveHistory, timeRemaining, TotalTime):
    averageMovesPerGame = 50
    start = time.time()
    TotalMoves = round(len(moveHistory) / 2)
    #Beginning Game give less time for starting moves
    if(TotalMoves <= 10):
        GivenTime = TotalTime/(2*averageMovesPerGame)
    #Middle Game give most time for moves
    elif(TotalMoves <= 30):
        GivenTime = (timeRemaining) * (1/averageMovesPerGame)    
    #End Game speed chess to end game
    else:
        GivenTime = (timeRemaining) * (1/2*averageMovesPerGame)
    timeElapsed = time.time() - start
    GivenTime = GivenTime - timeElapsed
    return GivenTime