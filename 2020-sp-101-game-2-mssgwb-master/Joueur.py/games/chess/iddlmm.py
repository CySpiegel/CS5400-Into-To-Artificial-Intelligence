from games.chess.functions import *

import random


#global chess peaces for iddlmm to function off of
CHESS_PEACES = ["p", "r", "n", "b", "q", "k"]


# itterative deepining depth-limited miniMax
# main driver
def iddlmm(chessBoard, playerColor):
    # settings for iddlmm
    scoredMovesDictionary = {}
    initalMove = ""
    initalScore = 0
    startingDepth = 0
    maxDepth = 2

    actions = generateActions(playerColor, chessBoard)
    scoredMovesDictionary = calculateBoardScoring(chessBoard, actions)

    initalScore, initalMove = minMaxValueSet(scoredMovesDictionary, startingDepth)

    # Generate inital actions for root node
    actionPair = miniMax(chessBoard, playerColor, initalMove, initalScore, startingDepth, maxDepth)

    # actions = generateActions(playerColor, chessBoard)
    # randomMove = random.choice(actions)
    return actionPair

# recursive function for minimax
def miniMax(chessBoard, playerColor, parentNodeMove, currentScore, depth, maxDepth):
    selectedPair = ()
    # dictionary of moves
    scoredMovesDictionary = {}
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

        childrenScoreMovePair = miniMax(newChessBoard, Enemy, action, actionScore, depth + 1, maxDepth)
        heuristicValue = heuristicCalculation(depth, actionScore, childrenScoreMovePair[0])

        # add heuristicValue to dictionary
        if heuristicValue not in scoredMovesDictionary:
            scoredMovesDictionary[heuristicValue] = []
        scoredMovesDictionary[heuristicValue] = scoredMovesDictionary[heuristicValue] + [action]

    # min max value of scoredMovesDictionary
    selectedPair = minMaxValueSet(scoredMovesDictionary, depth)
    return selectedPair


# evaluates moves and stores them according to score, returns dictionary score: listOfMoves
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
def heuristicCalculation(depth, parentScore, childScore):
    zeroSumGain = 0
    if depth % 2 == 0:
        zeroSumGain = childScore + parentScore
    else:
        zeroSumGain = childScore - parentScore
    return zeroSumGain

# Generate a new Board after playing a single move
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