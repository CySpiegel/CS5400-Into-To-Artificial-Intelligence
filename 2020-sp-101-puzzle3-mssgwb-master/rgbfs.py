import heapq
from gameboard import *
from gameFunction import *


# Recursive-Greedy Best-First Search
def rgbfs(PriorityQ, Direction_Order, Goal):

    # Dictionary of visited states 
    GraphVisited = {}

    # get current board
    CurrentTuple = heapq.heappop(PriorityQ)
    CurrentBoard = CurrentTuple[1]
    
    # makes key for visited node
    key = CurrentBoard.generate_key()
    # has current board been visited before
    if (GraphVisited.get(key)):
        return rgbfs(PriorityQ, Direction_Order, Goal)
    else:
        # check if oard is a winner
        CBscore = CurrentBoard.max_score()
        if (CBscore == Goal):
            # print(len(GraphVisited))
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
                    heapq.heappush(PriorityQ, (temp.heuristic(), temp))

    return rgbfs(PriorityQ, Direction_Order, Goal)