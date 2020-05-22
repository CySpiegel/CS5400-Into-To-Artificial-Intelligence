def predictedCost(value, countNumAppearanceOnBoard, spawnFrequencyWeighting, spawnPool):
    if countNumAppearanceOnBoard.get(value) > 0:
        countNumAppearanceOnBoard[value] -= 1
        return 0
    else:
        minSpawn = min(spawnPool)
        i = value/2
        counter = 0
        while i > 1 and i >= minSpawn:
            if i in countNumAppearanceOnBoard:
                counter += 1
            i = i/2

        if counter > 0:
            return 1 + predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting, spawnPool) + predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting, spawnPool)
        if counter == 0:
            if value in spawnFrequencyWeighting:
                return spawnFrequencyWeighting[value]
            else:
                spawnFrequencyWeighting[value] = 1 + predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting, spawnPool) + predictedCost(value/2, countNumAppearanceOnBoard, spawnFrequencyWeighting, spawnPool)
