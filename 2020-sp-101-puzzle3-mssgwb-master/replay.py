import sys
import collections
import heapq
from gbfs import *
from gameboard import *
from gameFunction import *
from datetime import datetime
from datetime import timedelta
import cProfile




if __name__ == "__main__":
        # getting file name
    puzzleFile = sys.argv[1]

    # past in moves made
    replay = raw_input("Input move history: ")
    replay = str(replay)

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

    print("Starting Trace")
    # # Main program Driver and AI
    for i in range(len(replay)):
        move_direction(replay[i], StartingBoard)
        StartingBoard.print_board()

        
