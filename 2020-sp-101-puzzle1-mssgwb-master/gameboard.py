import copy


class GameBoard:
    board = []
    totalMovesMade = 0
    spawnPool = []
    moveHistory = ""
    width = 0
    height = 0


    def __init__(self, newBoard, newWidth, newHeight, newSpawnPool):
        self.board = copy.deepcopy(newBoard)
        self.width = newWidth
        self.height = newHeight
        self.totalMovesMade = 0
        self.spawnPool = copy.deepcopy(newSpawnPool)


    def print_board(self):
        print(len(self.moveHistory))
        print(self.moveHistory)
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += str(self.board[i][j])
                line += " "
            print(line)
