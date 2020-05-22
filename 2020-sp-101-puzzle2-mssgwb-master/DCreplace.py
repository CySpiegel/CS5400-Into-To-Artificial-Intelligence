import copy
import sys
import collections
from gameboard import *
from gameFunction import *
from datetime import datetime
import cProfile
DEBUG = False



if __name__ == "__main__":
        # getting file name
    puzzleFile = sys.argv[1]

    # movement direction macros
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    # automated direction 
    DIRECTION = [UP, DOWN, LEFT, RIGHT]

    # BFS Q defined
    Q = []

    # Reading in from file
    with open(puzzleFile) as f:
        lines = [line.rstrip() for line in f]

    # getting inital information from file
    ScoreGoal = int(lines[0])
    gridDimentions = lines[1].split()
    Width = int(gridDimentions[0])
    Height = int(gridDimentions[1])
    SpawnPool = lines[2].split()
    lines = lines[3:]
    gridBoard = []

    # reading in spawn pool line
    for i in range(len(SpawnPool)):
        SpawnPool[i] = int(SpawnPool[i])

    # Reading in height
    for i in range(0, Height):
        gridBoard.append(lines[i].split())
        
    # reading in inital game board state
    for i in range(len(gridBoard)):
        for j in range(len(gridBoard[i])):
            gridBoard[i][j] = int(gridBoard[i][j])

    # Inital Starting game board state
    StartingBoard = GameBoard(gridBoard, Width, Height, SpawnPool, "")


    
    FailedMoveList = []
    ChildrenBoards = []
    # Creating 4 copies to work off of
    # for i in range(len(DIRECTION)):
    #     ChildrenBoards.append(copy.deepcopy(StartingBoard))

    
    for i in range(len(DIRECTION)):
        ChildrenBoards.append(copyGameState(StartingBoard))

    # Children moves
    for i in range(len(DIRECTION)):
        moveFiled = move_direction(DIRECTION[i], ChildrenBoards[i])
        if (moveFiled == False):
            FailedMoveList.append(i)

    print("Original Game State")
    StartingBoard.print_board()
    for i in ChildrenBoards:
        i.print_board()





