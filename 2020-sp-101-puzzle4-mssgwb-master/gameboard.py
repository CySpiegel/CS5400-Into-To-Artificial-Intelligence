
from collections import Counter
import math

class GameBoard:

    def __init__(self, newBoard, newWidth, newHeight, newSpawnPool, newMoveHistory, currentGoal, currentH):
        self.board = [[j for j in newBoard[i]] for i in range(newHeight)] 
        self.width = newWidth
        self.height = newHeight
        self.totalMovesMade = 0
        self.moveHistory = newMoveHistory
        self.spawnPool = [i for i in newSpawnPool]
        self.Goal = currentGoal
        self.numApperanceCount = {}
        self.spawnFrequencyWeights = {}
        self.h = currentH

    def spawnFrequencyMapping(self, SpawnPool):
        # Spawn Frequancy mapping
        spawnFrequency = {}
        uniqueValues = list(set(SpawnPool))
        for i in uniqueValues:
            spawnFrequency[i] = 0

        for i in spawnFrequency:
            for j in range(len(SpawnPool)):
                count = 0
                for k in range(len(SpawnPool)):
                    count += 1
                    if i == SpawnPool[(k + j) % len(SpawnPool)]:
                        spawnFrequency[i] += count
                        break

        for i in uniqueValues:
            spawnFrequency[i] =  int(spawnFrequency[i] / float(len(SpawnPool)))
        
        self.spawnFrequencyWeights =  spawnFrequency
        return spawnFrequency

    # Printing board
    def print_board(self):
        print(len(self.moveHistory))
        print(self.moveHistory)
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                line += str(self.board[i][j])
                line += " "
            print(line)


    # gives max score
    def max_score(self):
        scores = []
        for i in range(self.height):
            scores.append(max(self.board[i]))
        return max(scores)

    # counts non zero numbers
    def count_nonzero(self):
        temp = [[j for j in self.board[i] if j > 0] for i in range(self.height)]
        count = 0
        for i in range(len(temp)):
            count += len(temp[i])
        return count

    # turns board into list
    def flatten_board(self):
        return [element for sublist in self.board for element in sublist]

    #generates dictionary key
    def generate_key(self):
        flatten = self.flatten_board()
        return ''.join([str(elem) for elem in flatten])

    # sum of all values on board
    def sum_board(self):
        return sum([element for sublist in self.board for element in sublist])

    # number of distinct values
    def count_distinct(self):
        flattened_list = self.flatten_board()
        return len(set(flattened_list))

    # makes dictionary of values and counts duplicates
    def countNumAppearanceOnBoard(self):
        flatten_board = self.flatten_board()
        dictNumAppearance = {}

        for i in range(len(flatten_board)):
            dictNumAppearance[flatten_board[i]] = dictNumAppearance.get(flatten_board[i], 0) + 1

        self.numApperanceCount = dictNumAppearance
        return self.numApperanceCount

    # main consistant and admissible heuristic movement left to goal
    def predictedCost(self, value, countNumAppearanceOnBoard, spawnFrequencyWeighting):
        if value in countNumAppearanceOnBoard and countNumAppearanceOnBoard[value] > 0:
            countNumAppearanceOnBoard[value] -= 1
            return 0
        else:
            minSpawn = min(self.spawnPool)
            halfedValue = value/2
            counter = 0
            while halfedValue > 1 and halfedValue >= minSpawn:
                if halfedValue in countNumAppearanceOnBoard:
                    counter += 1
                halfedValue = halfedValue/2

            if counter > 0:
                return 1 + self.predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting) + self.predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting)
            if counter == 0:
                if value in spawnFrequencyWeighting:
                    return spawnFrequencyWeighting[value]
                else:
                    spawnFrequencyWeighting[value] = 1+  self.predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting) + self.predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting)

    # heuristic driver for astar
    def heuristic(self, spawnFrequencyWeighting, SpawnPool, Goal, algoSelection):
        current_highest_value = self.max_score()
        board_sum = self.sum_board()
        average = float(board_sum) / (self.height * self.width)
        if algoSelection == 1:
            num_of_zero = (self.height * self.width) - self.count_nonzero()
            moves_left = ((self.Goal - current_highest_value))
            penalty = self.count_distinct()

            # non consistant admissible heuristic 
            heuristic = moves_left * 3 + penalty - num_of_zero - (float(self.Goal) / average) + len(self.moveHistory)
        else:
            # 2^a -1
            a = math.log(min(SpawnPool)) / math.log(2)
            b = math.log(Goal) / math.log(2)
            discount = pow(2, b - a) - (b - a)
            countNumAppearanceOnBoard = self.countNumAppearanceOnBoard()
            # admissible consistant heuristic
            heuristic = self.predictedCost(Goal, countNumAppearanceOnBoard, spawnFrequencyWeighting)  - int(discount / current_highest_value)

        return heuristic + len(self.moveHistory)