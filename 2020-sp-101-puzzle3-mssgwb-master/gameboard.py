


class GameBoard:

    def __init__(self, newBoard, newWidth, newHeight, newSpawnPool, newMoveHistory, currentGoal):
        self.board = [[j for j in newBoard[i]] for i in range(newHeight)] 
        self.width = newWidth
        self.height = newHeight
        self.totalMovesMade = 0
        self.moveHistory = newMoveHistory
        self.spawnPool = [i for i in newSpawnPool]
        self.Goal = currentGoal

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

    def count_nonzero(self):
        temp = [[j for j in self.board[i] if j > 0] for i in range(self.height)]
        count = 0
        for i in range(len(temp)):
            count += len(temp[i])
        return count

    def generate_key(self):
        flatten = [element for sublist in self.board for element in sublist]
        return ''.join([str(elem) for elem in flatten])
        
    def sum_board(self):
        return sum([element for sublist in self.board for element in sublist])

    def heuristic(self):
        current_highest_value = self.max_score()
        board_sum = self.sum_board()
        average = board_sum / (self.height * self.width)

        return ((board_sum + current_highest_value) + average + ((self.Goal - current_highest_value))) * -1