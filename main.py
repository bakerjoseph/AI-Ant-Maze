from position import Position


class Path:
    time = 0
    posList = [Position()]
    path = [posList, time]
    posList.append


class AntModel:
    currentPos = Position()
    rotation = 0.0
    time = 0.0
    RNG = 0
    objective = False
    currentPath = Path()

    def __init__(self, currentPos, RNGSeed):
        self.currentPos = currentPos
        self.RNG = RNGSeed
