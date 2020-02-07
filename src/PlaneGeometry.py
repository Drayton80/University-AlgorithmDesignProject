import math

class PlaneGeometry:
    def getDistanceBetweenTwoPoints(self, point1X, point1Y, point2X, point2Y):
        xSubtraction = point2X - point1X
        ySubtraction = point2Y - point1Y
        
        return math.sqrt(xSubtraction * xSubtraction + ySubtraction * ySubtraction)
    