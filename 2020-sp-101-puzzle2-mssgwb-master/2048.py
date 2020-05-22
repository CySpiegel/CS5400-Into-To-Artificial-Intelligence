import sys
import collections
from gameboard import *
from gameFunction import *
from datetime import datetime
from datetime import timedelta
import cProfile
DEBUG = False


def max_value(Board):
    maxValue = 0
    tmp = 0
    for i in range(Board.height):
        tmp = max(Board.board[i])
        if (tmp > maxValue):
            maxValue = tmp
    return maxValue


def boundedDepthFirstSearch(Board, Direction_Order, Goal, MaxDepth):
    # depth limit
    depth_hit = False

    # inital push to Start Stack
    Stack = collections.deque()
    Stack.append(Board)
    while Stack:

        # debug flag for tracing
        if DEBUG:
            print("--------------------------------------------------------------------")
            print("\nStack Length: " + str(len(Stack)))
        # Children board list
        # needed to put into stack in reverse order
        ChildrenBoards = []
        CurrentBoard = Stack.pop()

        # Debug flag for tracing
        if DEBUG:
            print("Depth: " + str(len(CurrentBoard.moveHistory)))
            print("Move Order: " + CurrentBoard.moveHistory)
            print("Board Score: " + str(CurrentBoard.max_score()))
            print("Target Depth: " + str(MaxDepth))
            CurrentBoard.print_board()

        # if at maxdepth then echeck board for goal
        if (len(CurrentBoard.moveHistory) == MaxDepth):
            CBscore = CurrentBoard.max_score()
            if (CBscore == Goal):
                return depth_hit, CurrentBoard
            else:
                depth_hit = True
        # Generate more states
        else:
            # Generates a new board
            # attemps to move in a direction using the new board
            # if move succeeds then att it to the stack
            # if fails, discard board 
            for i in range(len(Direction_Order)):
                temp = copyGameState(CurrentBoard)
                if DEBUG:
                    print("Moving: " + Direction_Order[i])
                    temp.print_board()
                moveSuccessful = move_direction(Direction_Order[i], temp)
                if (moveSuccessful):
                    if DEBUG:
                        print("Moving Filed in: " + Direction_Order[i])
                        temp.print_board()
                    ChildrenBoards.append(copyGameState(temp))


            # adding new moves to Stack
            for i in range(len(Direction_Order) -1 , -1, -1):
                if (len(ChildrenBoards) != 0):
                    Stack.append(ChildrenBoards.pop())
        # delete list of child boards
        del ChildrenBoards

    # return depth hit and current board
    return depth_hit, CurrentBoard

# iterative depening depth first search
def id_dfs(Board, Direction_Order, Goal):
    depth = 0
    depth_hit = True
    potental_solution_score = 0
    while (depth_hit):
        # returns multiple values needed for control loop and found board
        depth_hit, Board_Goal = boundedDepthFirstSearch(Board, Direction_Order, Goal, depth)
        potental_solution_score = Board_Goal.max_score()
        if potental_solution_score == Goal:
            return Board_Goal
        else:
            depth += 1
    return 




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


    # Main program Driver and AI
    # TimeTaken = datetime.now()
    start_time = datetime.now()
    Final_Board = id_dfs(StartingBoard, DIRECTION, ScoreGoal)
    # TimeTaken = datetime.now() - TimeTaken
    
    print(Microsecond(start_time))
    if (Final_Board is None):
        print("No Win State Possible")
    else:
        Final_Board.print_board()

        




