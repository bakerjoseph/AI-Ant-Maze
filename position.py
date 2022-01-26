class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def movePosition(self, xmove, ymove):
        self.x = self.x + xmove
        self.y = self.y + ymove

    def printPos(self):
        posString = "(" + str(self.x) + ", " + str(self.y) + ")"

        print(posString)

    def setPosition(self, position):
        self.x = position.x
        self.y = position.y
