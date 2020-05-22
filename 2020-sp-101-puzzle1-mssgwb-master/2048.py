import copy
import sys
from gameboard import *
from gameFunction import *
from datetime import datetime

def max_value(Board):
    maxValue = 0
    tmp = 0
    for i in range(Board.height):
        tmp = max(Board.board[i])
        if (tmp > maxValue):
            maxValue = tmp
    return maxValue

def bfs(Board, Direction_Order, Goal):
    Valid_direction_move = copy.deepcopy(Direction_Order)
    FailedMoveList = []
    # define Queue for BFS
    Q = []

    # Goal reached
    Goal_Reached = False

    # inital push to Q
    Q.append(Board)
    while Q and Goal_Reached == False:
        # Reading First board in Queue
        CurrentBoard = Q.pop(0)
        Current_Score = max(map(lambda x: x[-1],CurrentBoard.board))

        # Checking Win Condition
        if ( Current_Score == Goal):
            return CurrentBoard

        # Interim Child board
        ChildrenBoards = []

        # Creating 4 copies to work off of
        for i in range(len(Direction_Order)):
            ChildrenBoards.append(copy.deepcopy(CurrentBoard))



        # Children moves
        for i in range(len(Direction_Order)):
            moveFiled = move_direction(Direction_Order[i], ChildrenBoards[i])
            if (moveFiled == False):
                FailedMoveList.append(i)

        # for i in FailedMoveList:
        #     ChildrenBoards.pop(i)
        #     for k in range(len(FailedMoveList)):
        #         FailedMoveList[k] -= 1


        for i in range(len(Direction_Order)):
            if (len(ChildrenBoards) != 0):
                Q.append(ChildrenBoards.pop(0))

        del ChildrenBoards









if __name__ == "__main__":
        # getting file name
    puzzleFile = sys.argv[1]

    # movement direction macros
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    # automated direction 
    DIRECTION = ['U', 'D', 'L', 'R']

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
    StartingBoard = GameBoard(gridBoard, Width, Height, SpawnPool)


# AI algorithm BFS
    TimeTaken = datetime.now()
    Final_Board = bfs(StartingBoard, DIRECTION, ScoreGoal)
    TimeTaken = datetime.now() - TimeTaken
    print(TimeTaken.microseconds)

    if (Final_Board is None):
        print("No Win State Possable")
    else:
        Final_Board.print_board()
        




