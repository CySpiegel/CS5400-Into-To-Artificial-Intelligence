from games.chess.functions import *
import time
import random

#global chess peaces for iddlmm to function off of
CHESS_PEACES = ["p", "r", "n", "b", "q", "k"]


# itterative deepining time-limited alpha beta pruning history table quiescent search miniMax
# main driver
# Paramaters
# Chess board: current chess board in list of list
# PlayerColor: Current players color
# TineRemaining: Remaining time in game
# MoveHistory: history of moves made in the game from server
# returns best move calculated by the algorithm
def tliddlmmabhtqs(chessBoard, playerColor, timeRemaining, moveHistory):
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
    quiescentLimit = 2
    HistoryTable = []

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
            

        actionPair = miniMax(chessBoard, playerColor, initalMove, initalScore, alpha, beta, HistoryTable,  False, quiescentLimit, startingDepth, maxDepth)
        
        # tracking time
        TimeElapsed = time.time() - start
        TimeTaken = TimeTaken + TimeElapsed

        # if 5 timex time taken gt allotedTime (timeLimit) then dont go to next level
        # on avrage each increase in depth is 4 times the previous level
        if (5*TimeTaken > AllotedTime):
            break
    return actionPair

# recursive function for minimax
# Paramaters
# ChessBoard: current chess board in list of list
# PlayerColor: side makingthe move
# ParentNodeMove: parents action
# CurrentScore: current material advantage 
# Alpha: alpha score
# Beta: beta score
# HistoryTable: holds the history of good moves for the current search, persists from driver function for increasing depths
# nonQuescence: is nonQuiescence search occuring
# quiescentLimit: maximum addition depth search allowedpast max depth if nonQuescence is true
# Depth: current depth 
# MaxDdepth: Max depth for current iterative search
# returns score and move combination of the max depth
def miniMax(chessBoard, playerColor, parentNodeMove, currentScore, alpha, beta, HistoryTable, nonQuiescence, quiescentLimit, depth, maxDepth):
    selectedPair = ()
    # dictionary of moves
    scoredMovesDictionary = {}
    bestMoves = {}
    miniMaxScore = 0
    heuristicValue = 0
    
    
    # who is enemy 
    if (playerColor == "white"):
        Enemy = "black"
    else:
        Enemy = "white"
    
    # If max depth reached and the incoming state was quiescent then contine to search quiecent
    if(depth == maxDepth and nonQuiescence):
        quiescentLimit = quiescentLimit - 1
    
    
    # basecase recursion combo breaker
    if (depth == maxDepth and not(nonQuiescence and quiescentLimit >= 0)):
        return (currentScore, parentNodeMove)




    # generate all actions for the current board
    actions = generateActions(playerColor, chessBoard)

    # board failed to generate Moves so its trashed
    if len(actions) == 0:
        return (currentScore, parentNodeMove)
    # make score of all moves 
    scoredMovesDictionary = calculateBoardScoring(chessBoard, actions)

    # Sort the actions found based on the value of good moves in the History Table to try good moves
    # at the current depth first
    SortedActions = sorted(actions, reverse = True, key=lambda move: FindValueInHistoryTable(HistoryTable, move, chessBoard))

    # itterate through all actions to create child nodes from indavidual moves
    for action in SortedActions:
        #build child board
        newChessBoard = postMoveBoardGenerator(chessBoard, action)
        # actionValue from move in child board
        for key, values in scoredMovesDictionary.items(): 
            if action in values:
                actionScore = key
                break

        nonQuiescence = notQuiescence(action, chessBoard)
        
        # if search has reached here with current depth == maxDepth then a quiescence search is taking place
        # this will allow the exploration of the next 2 levels according to the quiescentLimit set in the tliddlmmabhtqs
        # driver function else incrament depth counter as max depth has not been reached yet.
        if (depth == maxDepth):
            childrenScoreMovePair = miniMax(newChessBoard, Enemy, action, actionScore, alpha, beta, HistoryTable, nonQuiescence, quiescentLimit, depth, maxDepth)
        else:
            childrenScoreMovePair = miniMax(newChessBoard, Enemy, action, actionScore, alpha, beta, HistoryTable, nonQuiescence, quiescentLimit, depth + 1, maxDepth)
        heuristicValue = heuristicCalculation(depth, actionScore, childrenScoreMovePair[0])

        # alpha beta calculations
        if depth % 2 == 0:
            alpha = max(alpha, heuristicValue)
        else:
            beta = min(beta, heuristicValue)

        if beta <= alpha:
            # add history
            AddToHistoryTable(HistoryTable, chessBoard, selectedPair[1])
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
# Paramaters
# ChessBoard: current chess board
# actions: list of actions
# returns dictionary score: listOfMoves with material advantages from actions taken
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

# Simple Heuristic calculation based on lecture video of zeroSumGain
# Paramaters
# Depth: current search depth
# ParentScore: material advantage from parent
# ChildScore: material advantage from child
# returns heuristic calculated value value
def heuristicCalculation(depth, parentScore, childScore):
    zeroSumGain = 0
    if depth % 2 == 0:
        zeroSumGain = childScore + parentScore
    else:
        zeroSumGain = childScore - parentScore
    return zeroSumGain

# Generate a new Board after playing a single move
# Paramaters
# ChessBoard: current chess board in list of list form
# MoveToMake: current move to apply to the board
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
# paramaters
# ScoreDictionary: list of moves with material advantage
# Depth: current depth being searched
# returns tuple of (score, move)
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


# Predict move time it will take for the next depth to be searched
# Paramaters:
# MoveHistory: games hostory of mast moves from server
# TimeRemaining: time left
# TotalTime: 15min in nanoseconds 
# returns the predicted time
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

# Adds entry into history table
# Paramaters:
# HistoryTable: total collection is history table
# Board: current board
# Move: Move to apply to current board
# Returns: nothing
def AddToHistoryTable(HistoryTable, Board, move):
    for list in HistoryTable:
        if list[0] == Board:
            if list[1] == move:
                Index = HistoryTable.index(list)
                HistoryTable[Index][2] = HistoryTable[Index][2] + 1
                return
    Board = [x[:] for x in Board]
    HistoryTable.append([Board, move, 1])

# Finds the value of the good move stored in the history table
# Paramaters:
# HistoryTable: HistoryTable list
# Move: Move to be applied to board
# Board: Current chess board as list of list
def FindValueInHistoryTable(HistoryTable, move, Board):
    for list in HistoryTable:
        if list[0] == Board:
            if list[1] == move:
                Index = HistoryTable.index(list)
                return HistoryTable[Index][2]
    return 0   


# Determins if move to apply to board is notQuiescence
# if action to be taken has a material advantage >= 3
# meaning a peace other than pawn has been captured
# Then state is not Quescent and shoud be explored past
# current maxDepth.

# Paramaters:
# Move: action to be taken on current board
# ChessBoard: current chess board as list of list for which move is to be applied to.
# return true if state is non-Quiescence, false if otherwise
def notQuiescence(Move, chessBoard):

    moveScoreDctionary =  calculateBoardScoring(chessBoard, [Move])
    for key in moveScoreDctionary:
        scoreOfMove = key

    if scoreOfMove >= 3:
        return True
    return False
