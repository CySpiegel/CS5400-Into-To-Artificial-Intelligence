import heapq
from gameboard import *
from gameFunction import *

# Greedy Best-First Search
def gbfs(Board, Direction_Order, Goal):
    # queue the heap works off of
    Q = []

    #pushing inital board to heapq
    heapq.heappush(Q, (Board.count_nonzero(), Board))

    # Dictionary of visited states 
    GraphVisited = {}

    while Q:
        # get current board
        CurrentTuple = heapq.heappop(Q)
        CurrentBoard = CurrentTuple[1]
        
        # makes key for visited node
        key = CurrentBoard.generate_key()
        # has current board been visited before
        if (GraphVisited.get(key)):
            continue
        else:
            # check if oard is a winner
            CBscore = CurrentBoard.max_score()
            if (CBscore == Goal):
                return CurrentBoard
            
            # adding current board to history
            GraphVisited[CurrentBoard.generate_key()] = 1

            # Generates a new board
            # attemps to move in a direction using the new board
            # if move succeeds then att it to the stack
            # if fails, discard board 
            for i in range(len(Direction_Order)):
                    temp = copyGameState(CurrentBoard)
                    moveSuccessful = move_direction(Direction_Order[i], temp)
                    if (moveSuccessful):
                        # adding to priority queue
                        heapq.heappush(Q, (temp.heuristic(), temp))

    return