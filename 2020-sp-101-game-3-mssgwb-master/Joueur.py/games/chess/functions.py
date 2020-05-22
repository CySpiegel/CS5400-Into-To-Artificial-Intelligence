#Global lists needed to function
CHESS_RANK = ["a", "b", "c", "d", "e", "f", "g", "h"]
CHESS_FILE = ["1", "2", "3", "4", "5", "6", "7", "8"]
WHITE_CHESS_PEACES = ["P", "R", "N", "B", "Q", "K"]
BLACK_CHESS_PEACES = ["p", "r", "n", "b", "q", "k"]

# custom print function to show chess board
# does not return anything
def printChessBoard(chessBoard):
    count = 9
    for i in range(len(chessBoard) - 1, -1, -1):
        count -= 1
        print(count, chessBoard[i])
    print(" ",CHESS_RANK)

# parsing the fen string into a 2d matrix
# returns new chess board
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

# UCI format to grid coordinates
# returns tuple of previous grid pos and next grid pos
def uciToCoordinates(uciString):
    move = uciClenser(uciString)
    cRankOrigin = move[0]
    cFileOrigin = move[1]
    cRankDestination = move[2]
    cFileDestination = move[3]
    rowOrigin = -1
    colOrigin = -1
    rowDestination = -1
    colDestination = -1
    for i in range(8):
        if CHESS_RANK[i] == cRankOrigin:
            rowOrigin = i
        if CHESS_FILE[i] == cFileOrigin:
            colOrigin = i
        if CHESS_RANK[i] == cRankDestination:
            rowDestination = i
        if CHESS_FILE[i] == cFileDestination:
            colDestination = i
    return (colOrigin, rowOrigin, colDestination, rowDestination)

# grid coordinates to UCI format
# returns UCI format from gris pos
def coordinatesToUci(row, col):
    return (CHESS_RANK[col] + CHESS_FILE[row])

# clesnes the UCI string to 4 length format
# returns clean UCI string
def uciClenser(UCIMove):
    move = UCIMove
    if len(UCIMove) > 4:
        if "x" in UCIMove:
            move = move.replace("x", '')
        else:
            move = move[:-1]
    return move


# generate moves for selected chess peace
# returns list of all valid moves for given board state
def generateActions(color, chessBoard):
    ValidMoves = []
    KingRow = -1
    KingCol = -1
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

                
            # Generate al moves for King  
            if (chessBoard[i][j] == MyChessPeaces[5]):
                KingRow = i
                KingCol = j
                KingValidMoves = []
                KingValidMoves = generateKingMoves(chessBoard, MyChessPeaces, Enemy, i, j)
                if (len(KingValidMoves) > 0):
                    ValidMoves.append(KingValidMoves)
            
    # future functionality
    ListOfMoves = [j for sub in ValidMoves for j in sub]
    ValidMoves = []

    # play all valid moves to see if king is placed in check
    inCheck = isKingInCheck(chessBoard, MyChessPeaces, Enemy, KingRow, KingCol)
    for move in ListOfMoves:
        if checkValidMove(chessBoard, move, MyChessPeaces, Enemy, KingRow, KingCol):
            ValidMoves.append(move)

    return ValidMoves


# Generates all moves for selected Knight
# returns valid possitions for knight in uci format
def generateAllKnightsMoves(chessBoard, enemy, row, col):
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    validPositions = []
    for (x, y) in deltas:
        newXcord = row + x
        newYcord = col + y
        if -1 < newXcord < 8 and -1 < newYcord < 8:
            if(chessBoard[newXcord][newYcord] == "." or chessBoard[newXcord][newYcord] in enemy):
                validPositions.append(coordinatesToUci(row, col) + coordinatesToUci(newXcord, newYcord))

    return validPositions

# general function for generating diagonal move sets for Q, K, B peaces
# returns diagonal moves from a pos in UCI format
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
# returns stright line moves in CI format
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
# returns list of valid moves for Queen
def generateQueensMoves(chessBoard, MyChessPeaces, enemy, row, col):
    cardinalDirectionMoves = generateStrightMoves(chessBoard, MyChessPeaces, enemy, False, row, col)
    diagonalDirectionsMoves = generateDiagonalMoves(chessBoard, MyChessPeaces, enemy, False, row, col)
    validMoves = cardinalDirectionMoves + diagonalDirectionsMoves
    return validMoves

# Generates al moves for the Pawn
# returns list of valic move for pawn
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


# Generate al moves for the king
# returns list of valic move for king
def generateKingMoves(chessBoard, MyChessPeaces, enemy, row, col):
    diagonalDirections = generateDiagonalMoves(chessBoard, MyChessPeaces, enemy, True, row, col)
    cardinalDirections = generateStrightMoves(chessBoard, MyChessPeaces, enemy, True, row, col)
    needToCheckMoves = diagonalDirections + cardinalDirections

    return needToCheckMoves

# Checking to see if the king is currently in check
# returns bool if king is in check
def isKingInCheck(chessBoard, MyChessPeaces, enemy, row, col):

    knightPossitions = kingCheckForKights(chessBoard, enemy, row, col)
    kingStraightLineOfSight = kingCheckStraight(chessBoard, MyChessPeaces, enemy, row, col)
    kingDiagonalLineOfSight = kingCheckDiagonal(chessBoard, MyChessPeaces, enemy, row, col)

    if( knightPossitions or kingStraightLineOfSight or kingDiagonalLineOfSight):
        return True
    else:
        return False

# helper function for king possition checking for enemy knights
# returns bool for king in check from knights
def kingCheckForKights(chessBoard, enemy, kingRow, kingCol):
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    for (x, y) in deltas:
        newXcord = kingRow + x
        newYcord = kingCol + y
        if -1 < newXcord < 8 and -1 < newYcord < 8:
            if(chessBoard[newXcord][newYcord] == enemy[2]):
                return True
    return False

# helper function for king possition checking for enemy in line of sight
# of the kind from straight lines, rook, queen
# returns bool for in check from traght line
def kingCheckStraight(chessBoard, MyChessPeaces, enemy, row, col):
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

    directions = [  
                    #right
                    zip(rowStayRight, range(col + 1, 8)),
                    #left
                    zip(rowStayColMoveLeft, range(col -1, -1, -1)),
                    #up
                    zip(range(row + 1, 8), colStayRowMovingUp),
                    #down
                    zip(range(row - 1, -1, -1), colStayRowMovingDown)
                ]

    for direction in directions:
        for pair in direction:
            # Stp if My peace encountered
            if (chessBoard[pair[0]][pair[1]] in MyChessPeaces):
                break

            # stop if enemy peace is encountered
            if (chessBoard[pair[0]][pair[1]] in enemy):
                if (chessBoard[pair[0]][pair[1]] == enemy[1] or chessBoard[pair[0]][pair[1]] == enemy[4]):
                    return True
                break

    return False

# checking Kings Diagonal Directions for possable check
# returns bool from diagonal check
def kingCheckDiagonal(chessBoard, MyChessPeaces, enemy, row, col):
    kingDelta = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    if MyChessPeaces[0].islower():
        side = -1
    else:
        side = 1
    
    pawnDelta = [(1 * side,-1),(1 * side,1)]
    directions = [
                    zip(range(row + 1, 8), range(col + 1, 8)),
                    zip(range(row + 1, 8), range(col - 1, -1, -1)),
                    zip(range(row - 1, -1, -1), range(col + 1, 8)),
                    zip(range(row - 1, -1, -1), range(col - 1, -1, -1)),
                ]

    for (x, y) in pawnDelta:
        newRow = row + x
        newCol = col + y
        if -1 < newRow < 8 and -1 < newCol < 8:
            if(chessBoard[newRow][newCol] == enemy[0]):
                return True

    for (x, y) in kingDelta:
        newRow = row + x
        newCol = col + y
        if -1 < newRow < 8 and -1 < newCol < 8:
            if(chessBoard[newRow][newCol] == enemy[5]):
                return True
    

    for direction in directions:
        for pair in direction:
            # Stp if My peace encountered
            if (chessBoard[pair[0]][pair[1]] in MyChessPeaces):
                break

            # stop if enemy peace is encountered
            if (chessBoard[pair[0]][pair[1]] in enemy):
                if (chessBoard[pair[0]][pair[1]] == enemy[3] or chessBoard[pair[0]][pair[1]] == enemy[4]):
                    return True
                break

    return False

# check if move being made is valid
# returns bool if move is valid
def checkValidMove(chessBoard, moveToMake, MyChessPeaces, enemy, kingRow, kingCol):
    newChessBoard  = [[j for j in chessBoard[i]] for i in range(len(chessBoard))] 
    moveToMakeCoordiantes = uciToCoordinates(moveToMake)

    oldPossition = (moveToMakeCoordiantes[0], moveToMakeCoordiantes[1])
    chessPeaceToMove = newChessBoard[oldPossition[0]][oldPossition[1]]

    newChessBoard[oldPossition[0]][oldPossition[1]] = "."

    newPossiton = (moveToMakeCoordiantes[2], moveToMakeCoordiantes[3])
    newChessBoard[newPossiton[0]][newPossiton[1]] = chessPeaceToMove

    if (chessPeaceToMove == MyChessPeaces[5]):
        isInCheck = isKingInCheck(newChessBoard, MyChessPeaces, enemy, newPossiton[0], newPossiton[1])
    else:
        isInCheck = isKingInCheck(newChessBoard, MyChessPeaces, enemy, kingRow, kingCol)

    if isInCheck:
        return False
    else:
        return True


