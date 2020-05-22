


class GameBoard:

    def __init__(self, newBoard, newWidth, newHeight, newSpawnPool, newMoveHistory):
        self.board = [[j for j in newBoard[i]] for i in range(newHeight)] 
        self.width = newWidth
        self.height = newHeight
        self.totalMovesMade = 0
        self.moveHistory = newMoveHistory
        self.spawnPool = [i for i in newSpawnPool]


    def print_board(self):
        print(len(self.moveHistory))
        print(self.moveHistory)
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += str(self.board[i][j])
                line += " "
            print(line)

    def max_score(self):
        scores = []
        for i in range(self.height):
            scores.append(max(self.board[i]))
        return max(scores)