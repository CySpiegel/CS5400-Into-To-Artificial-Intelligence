# from gameFunction import *

# swipe up on the board
def move_up(Board):
    moveSuccessful = False
    for k in range(Board.width):
        i = 0
        for j in range(1, Board.height):
            if (Board.board[j][k] == 0):
                continue
            elif (Board.board[i][k] == 0):
                Board.board[j][k], Board.board[i][k] = Board.board[i][k], Board.board[j][k]
                moveSuccessful = True
            elif (Board.board[j][k] != Board.board[i][k]):
                i += 1
                Board.board[j][k], Board.board[i][k] = Board.board[i][k], Board.board[j][k]
                moveSuccessful = True
            elif (Board.board[j][k] == Board.board[j][k]):
                Board.board[j][k] = 0
                Board.board[i][k] = Board.board[i][k] * 2
                i += 1
                moveSuccessful
    return moveSuccessful

# swipe down on the board
def move_down(Board):
    moveSuccessful = False
    for k in range(Board.width):
        i = Board.height - 1
        for j in range(Board.height - 2, -1, -1):
            if (Board.board[j][k] == 0):
                continue
            elif (Board.board[i][k] == 0):
                Board.board[j][k], Board.board[i][k] = Board.board[i][k], Board.board[j][k]
                moveSuccessful = True
            elif (Board.board[j][k] != Board.board[i][k]):
                i -= 1
                Board.board[j][k], Board.board[i][k] = Board.board[i][k], Board.board[j][k]
                moveSuccessful = True
            elif (Board.board[j][k] == Board.board[j][k]):
                Board.board[j][k] = 0
                Board.board[i][k] = Board.board[i][k] * 2
                i -= 1
                moveSuccessful
    return moveSuccessful

# swipe left on the board
def move_left(Board):
    moveSuccessful = False
    width = Board.width
    for k in range(Board.height):
        array = Board.board[k]
        i = 0
        for j in range(1, width):
            if (array[j] == 0):
                continue
            elif (array[i] == 0):
                array[j], array[i] = array[i], array[j]
                moveSuccessful = True
            elif (array[j] != array[i]):
                i += 1
                array[j], array[i] = array[i], array[j]
                moveSuccessful = True
            elif (array[j] == array[i]):
                array[j] = 0
                array[i] = array[i] * 2
                i += 1
                moveSuccessful = True
    return moveSuccessful

# swipe right on board
def move_right(Board):
    moveSuccessful = False
    width = Board.width
    for k in range(Board.height):
        array = Board.board[k]
        i = width - 1
        for j in range( width - 2, -1, -1):
            if (array[j] == 0):
                continue
            elif (array[i] == 0):
                array[j], array[i] = array[i], array[j]
                moveSuccessful = True
            elif (array[j] != array[i]):
                i -= 1
                array[j], array[i] = array[i], array[j]
                moveSuccessful = True
            elif (array[j] == array[i]):
                array[j] = 0
                array[i] = array[i] * 2
                i -= 1
                moveSuccessful = True
    return moveSuccessful


# swipe down on board
def move_direction(direction, Board):
    moveSuccessful = False
    if (direction == 'U'):
        moveSuccessful = move_up(Board)
    elif (direction == 'D'):
        moveSuccessful = move_down(Board)
    elif (direction == 'R'):
            moveSuccessful = move_right(Board)
    elif (direction == 'L'):
            moveSuccessful = move_left(Board)


    if (moveSuccessful):
        if (spawn(Board)):
            Board.moveHistory += direction

    return moveSuccessful

# spawn new value on board if space is available
# clockwise from top left corner 
def spawn(Board):
    location = 0
    max_width = Board.width
    max_height = Board.height
    height = 0
    width = 0
    didSpawn = False
    count = 0

    while(didSpawn == False and count < 4 ):
        count += 1

        if (location == 0):
            height = 0
            width = 0
            location += 1
            didSpawn = spawn_at_position(height, width, Board)

        elif (location == 1):
            height = 0
            width = max_width - 1
            location += 1
            didSpawn = spawn_at_position(height, width, Board)

        elif (location == 2):
            height = max_height - 1
            width = max_width - 1
            location += 1
            didSpawn = spawn_at_position(height, width, Board)
        
        elif (location == 3):
            height = max_height - 1
            width = 0
            location += 1
            didSpawn = spawn_at_position(height, width, Board)
        else:
            location = 0
        
    return didSpawn


# Spawn value at indicated possition from spawn function
def spawn_at_position(height, width, Board):
    if (Board.board[height][width] == 0):
        spawning = Board.spawnPool[0]
        Board.board[height][width] = spawning
        Board.spawnPool.pop(0)
        Board.spawnPool.append(spawning)
        return True
    else:
        return False

