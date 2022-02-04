import time

scaler = 1
scale = scaler


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return("x: " + str(self.x) + " y: " + str(self.y))

    def movePosition(self, xmove, ymove):
        self.x = self.x + xmove
        self.y = self.y + ymove

    def print(self):
        posString = "(" + str(self.x) + ", " + str(self.y) + ")"

        print(posString)

    def setPosition(self, position):
        self.x = position.x
        self.y = position.y

    def Colliding(self, tilePos):

        posX = self.x
        posY = self.y

        tileRangeStart = [scale*(tilePos.position.x),
                          scale*(tilePos.position.y)]
        tileRangeEnd = [scale*(tilePos.position.x + (100/3)),
                        scale*(tilePos.position.y + (100/3))]

        # print(str(posX) + " " + str(posY) + "\n" + str(tileRangeStart) + " " + str(tileRangeEnd))
        # time.sleep(2)

        cm = 2
        if (posX >= tileRangeStart[0] - cm and posX <= tileRangeEnd[0] + cm and posY >= tileRangeStart[1] - cm and posY <= tileRangeEnd[1] + cm):

            # time.sleep(60)
            return True

        return False
