CHESS_RANK = ["a", "b", "c", "d", "e", "f", "g", "h"]
CHESS_FILE = ["1", "2", "3", "4", "5", "6", "7", "8"]
WHITE_CHESS_PEACES = ["P", "R", "N", "B", "Q", "K"]
BLACK_CHESS_PEACES = ["p", "r", "n", "b", "q", "k"]


def printChessBoard(chessBoard):
    count = 9
    for i in range(len(chessBoard) - 1, -1, -1):
        count -= 1
        print(count, chessBoard[i])
    print(" ",CHESS_RANK)

# parsing the fen string into a 2d matrix
def parseFenBoardList(fenBoardList):
    # reverse board so white is at 0 row
    fenBoardList.reverse()
    tmpRow = []
    newChessBoard = []
    for row in fenBoardList:
        for index in row:
            if index.isnumeric():
                for i in range(int(index)):
                    tmpRow.append(".")
            else:
                tmpRow.append(index)
        newChessBoard.append(tmpRow)
        tmpRow = []
    return newChessBoard

def uciToCoordinates(uciString):
    cRank = uciString[0]
    cFile = uciString[1]
    row = -1
    col = -1
    for i in range(8):
        if CHESS_RANK[i] == cRank:
            row = i
        if CHESS_FILE[i] == cFile:
            col = i
    return (row, col)

def coordinatesToUci(row, col):
    return (CHESS_RANK[col] + CHESS_FILE[row])


# generate moves for selected chess peace
def generateSelectedPeaceMoveList(color, chessBoard, getEnemyMoves):
    ValidMoves = []
    #my current faction
    if(color == "white"):
        MyChessPeaces = WHITE_CHESS_PEACES
        Enemy = BLACK_CHESS_PEACES
    else:
        MyChessPeaces = BLACK_CHESS_PEACES
        Enemy = WHITE_CHESS_PEACES
    

    for i in range(8):
        for j in range(8):
            # Generate all moves for Pawns
            if (chessBoard[i][j] == MyChessPeaces[0]):
                PawnValidMoves = []
                PawnValidMoves = generatePawnMoves(chessBoard, MyChessPeaces, Enemy, i, j)
                if (len(PawnValidMoves) > 0):
                    ValidMoves.append(PawnValidMoves)


            # Generating moves for Knights
            if (chessBoard[i][j] == MyChessPeaces[2]):
                KnightsValidMoves = []
                KnightsValidMoves = generateAllKnightsMoves(chessBoard, Enemy, i, j)
                if(len(KnightsValidMoves) > 0):
                    ValidMoves.append(KnightsValidMoves)

            # # Generate all moves for Bishops
            if (chessBoard[i][j] == MyChessPeaces[3]):
                BishopsValidMoves = []
                BishopsValidMoves = generateDiagonalMoves(chessBoard, MyChessPeaces, Enemy, False ,i, j)
                if (len(BishopsValidMoves) > 0):
                    ValidMoves.append(BishopsValidMoves)

            # # generate all moves for Rooks
            if (chessBoard[i][j] == MyChessPeaces[1]):
                RookValidMoves = []
                RookValidMoves = generateStrightMoves(chessBoard, MyChessPeaces, Enemy, False, i, j)
                if (len(RookValidMoves) > 0):
                    ValidMoves.append(RookValidMoves)


            # Generate all moves for Queen
            if (chessBoard[i][j] == MyChessPeaces[4]):
                QueenValidMoves = []
                QueenValidMoves = generateQueensMoves(chessBoard, MyChessPeaces, Enemy, i, j)
                if (len(QueenValidMoves) > 0):
                    ValidMoves.append(QueenValidMoves)

                
            # # Generate al moves for King  
            if (chessBoard[i][j] == MyChessPeaces[5]):
                KingValidMoves = []
                KingValidMoves = generateKingMoves(chessBoard, MyChessPeaces, Enemy, getEnemyMoves, i, j)
                if (len(KingValidMoves) > 0):
                    ValidMoves.append(KingValidMoves)
            
            # future functionality
            # ListOfMoves = [j for sub in ValidMoves for j in sub]
    return ValidMoves


# Generates all moves for selected Knight
def generateAllKnightsMoves(chessBoard, enemy, x0, y0):
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    validPositions = []
    for (x, y) in deltas:
        newXcord = x0 + x
        newYcord = y0 + y
        if -1 < newXcord < 8 and -1 < newYcord < 8:
            if(chessBoard[newXcord][newYcord] == "." or chessBoard[newXcord][newYcord] in enemy):
                validPositions.append(coordinatesToUci(x0, y0) + coordinatesToUci(newXcord, newYcord))

    return validPositions


def generateDiagonalMoves(chessBoard, MyChessPeaces, enemy, isKing, row, col):
    wholeBoard = 8
    # diagonal direction lists
    northEast = []
    northWest = []
    southEast = []
    southWest = []

    validPositions = []
    diagonalDirections = []
    straightDirections = []
    if (isKing):
        rowUpMax = row + 2
        rownDown = row - 2
        colRightMax = col + 2
        colLeftMax = col - 2
    else:
        rowUpMax = wholeBoard
        rownDown = -1
        colRightMax = wholeBoard
        colLeftMax = -1

    if (row + 1 < 8):
        # generating Diagonal Movement
        if (col + 1 < 8):
            northEast = [zip(range(row + 1, rowUpMax), range(col + 1, colRightMax))]
        if (col - 1 > -1):
            northWest = [zip(range(row + 1, rowUpMax), range(col - 1, colLeftMax, -1))]
            
    if (row - 1 > -1):
        if (col + 1 < 8):
            southEast = [zip(range(row - 1, rownDown, - 1), range(col + 1, colRightMax))]
        if (col - 1 > -1):
            southWest = [zip(range(row - 1, rownDown, - 1), range(col - 1, colLeftMax, -1))]
    
    diagonalDirections = northEast + northWest + southWest + southEast

    for direction in diagonalDirections:
        for pair in direction:
            # Stop if My peace encountered
            if (chessBoard[pair[0]][pair[1]] in MyChessPeaces):
                break

            validPositions.append(coordinatesToUci(row, col) + coordinatesToUci(pair[0], pair[1]))

            # stop if enemy peace is encountered
            if (chessBoard[pair[0]][pair[1]] in enemy):
                break
    return validPositions

# generating traight line movement in ccardenal directions
def generateStrightMoves(chessBoard, MyChessPeaces, enemy, isKing, row, col):
    wholeBoard = 8
    if (isKing):
        maxUpMove = row + 2
        maxDownMove = row - 2
        maxLeftMove = col -2
        maxRightMove = col + 2
    else:
        maxUpMove = wholeBoard
        maxDownMove = -1
        maxLeftMove = -1
        maxRightMove = wholeBoard
    # straight line lists
    validPositions = []
    rowStayRight = []
    rowStayColMoveLeft = []
    colStayRowMovingUp = []
    colStayRowMovingDown = []

    for i in range( col + 1, 8):
        rowStayRight.append(row)

    for i in range( col - 1, -1, -1):
        rowStayColMoveLeft.append(row)

    for i in range(row + 1, 8):
        colStayRowMovingUp.append(col)

    for i in range(row - 1, -1, -1):
        colStayRowMovingDown.append(col)

    directions = [  #right
                    zip(rowStayRight, range(col + 1, maxRightMove)),
                    #left
                    zip(rowStayColMoveLeft, range(col -1, maxLeftMove, -1)),
                    #up
                    zip(range(row + 1, maxUpMove), colStayRowMovingUp),
                    #down
                    zip(range(row - 1, maxDownMove, -1), colStayRowMovingDown)
                ]

    for direction in directions:
        for pair in direction:
            # Stp if My peace encountered
            if (chessBoard[pair[0]][pair[1]] in MyChessPeaces):
                break

            validPositions.append(coordinatesToUci(row, col) + coordinatesToUci(pair[0], pair[1]))

            # stop if enemy peace is encountered
            if (chessBoard[pair[0]][pair[1]] in enemy):
                break

    return validPositions

# Generates all moves for the Queen
def generateQueensMoves(chessBoard, MyChessPeaces, enemy, row, col):
    cardinalDirectionMoves = generateStrightMoves(chessBoard, MyChessPeaces, enemy, False, row, col)
    diagonalDirectionsMoves = generateDiagonalMoves(chessBoard, MyChessPeaces, enemy, False, row, col)
    validMoves = cardinalDirectionMoves + diagonalDirectionsMoves
    return validMoves

# Generates al moves for the Pawn
def generatePawnMoves(chessBoard, MyChessPeaces, enemy, row, col):
    validPositions = []
    stayInColum = []
    movementRange = 2
    forwardDirections = []
    diagonalDirections = []
    diagonalRight = []
    diagonalLeft = []
    if (MyChessPeaces[0].isupper()):
        # if pawn is stil at starting row add possable movement to
        # move 2 spaces on first move
        if (row == 1):
            movementRange = 3

        # itterate list for range of movement
        for i in range(movementRange):
            stayInColum.append(col)

        #moving white pawn forword
        if(row + 1 < 8):
            forwardDirections = [zip(range(row + 1, row + movementRange), stayInColum)]
            # checking forward to the right
            if (col + 1 < 8):
                diagonalRight = [zip(range(row + 1, row + 2), range(col + 1, col + 2))]
            # checking forward to the left
            if (col - 1 > -1):
                diagonalLeft = [zip(range(row + 1, row + 2), range(col - 1, col - 2, -1)),]
                
            # adding to combined diagonal directions
            diagonalDirections = diagonalRight + diagonalLeft
    else:
        # if pawn is stil at starting row add possable movement to
        # move 2 spaces on first move
        if (row == 6):
            movementRange = 3

        # itterate list for range of movement
        for i in range(movementRange):
            stayInColum.append(col)

        #moving black pawn forword
        if(row - 1 > -1):
            forwardDirections = [zip(range(row - 1, row - movementRange, - 1), stayInColum)]

            for direction in diagonalDirections:
                for pair in direction:
                    print(pair)
            # # checking forward to the right
            if (col + 1 < 8):
                diagonalRight = [zip(range(row - 1, row - 2, - 1), range(col + 1, col + 2))]
            # checking forward to the left
            if (col - 1 > -1):
                diagonalLeft = [zip(range(row - 1, row - 2, - 1), range(col - 1, col - 2, -1)),]
                
            # adding to combined diagonal directions
            diagonalDirections = diagonalRight + diagonalLeft
            


    # # building list of forward moves
    for direction in forwardDirections:
        for pair in direction:
            # Stop if pawn encounters any chess peace in front of it
            if (chessBoard[pair[0]][pair[1]] in MyChessPeaces or chessBoard[pair[0]][pair[1]] in enemy):
                break

            validPositions.append(coordinatesToUci(row, col) + coordinatesToUci(pair[0], pair[1]))
    
    #building list of diagonal moves if enemy is found
    for direction in diagonalDirections:
        for pair in direction:
            if (chessBoard[pair[0]][pair[1]] in enemy):
                validPositions.append(coordinatesToUci(row, col) + coordinatesToUci(pair[0], pair[1]))

    return validPositions

#
# Generate al moves for the king
# prototyping future optimizations 
def generateKingMoves(chessBoard, MyChessPeaces, enemy, getEnemyMoves, row, col):
    EnemyColor = ""
    validPositions  = []
    EnmyMoves = []
    # Generating king diagonal moves
    diagonalDirections = generateDiagonalMoves(chessBoard, MyChessPeaces, enemy, True, row, col)
    cardinalDirections = generateStrightMoves(chessBoard, MyChessPeaces, enemy, True, row, col)
    needToCheckMoves = diagonalDirections + cardinalDirections

    if enemy[0].islower:
        EnemyColor = "black"
    else:
        EnemyColor = "white"

    # the goal of thie function is to generate a list of all possitions under attack
    # if the possition is under attack the King can not put himself in check
    if (getEnemyMoves == False and len(needToCheckMoves) > 0):
        EnmyMoves = generateSelectedPeaceMoveList(EnemyColor, chessBoard, True)

    for move in needToCheckMoves:
        if move not in EnmyMoves:
            validPositions.append(move)

    return validPositions

def isInCheck(chessBoard, MyChessPeaces, enemy, getEnemyMoves, row, col):
    #do nothing if true
    EnemyMoves = []

    if enemy[0].islower:
        EnemyColor = "black"
    else:
        EnemyColor = "white"

    if(getEnemyMoves == False):
        EnmyMoves = generateSelectedPeaceMoveList(EnemyColor, chessBoard, True)


    return