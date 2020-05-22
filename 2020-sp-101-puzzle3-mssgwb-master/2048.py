import sys
import collections
import heapq
from gbfs import *
from rgbfs import *
from gameboard import *
from gameFunction import *
from datetime import datetime
from datetime import timedelta
import cProfile




if __name__ == "__main__":
    if 1 / 2:
        print("Use python2")
        exit(1)
    # getting file name
    puzzleFile = sys.argv[1]

    if len(sys.argv) > 2:
        algoSelection = int(sys.argv[2])
    else:
        algoSelection = 0


    # movement direction macros
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    # automated direction 
    DIRECTION = [UP, DOWN, LEFT, RIGHT]


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
    StartingBoard = GameBoard(gridBoard, Width, Height, SpawnPool, "", ScoreGoal)

    if (algoSelection == 1):
        # queue the heap works off of
        PriorityQ = []

        #pushing inital board to heapq
        heapq.heappush(PriorityQ, (StartingBoard.count_nonzero(), StartingBoard))
        # # Main program Driver and AI
        start_time = datetime.now()
        Final_Board = rgbfs(PriorityQ, DIRECTION, ScoreGoal)
        
        print(Microsecond(start_time))
        if (Final_Board is not None):
            Final_Board.print_board()
    else:
        # # Main program Driver and AI
        start_time = datetime.now()
        Final_Board = gbfs(StartingBoard, DIRECTION, ScoreGoal)
        
        print(Microsecond(start_time))
        if (Final_Board is not None):
            Final_Board.print_board()

        
