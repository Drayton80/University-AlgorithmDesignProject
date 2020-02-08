import math
from TargetPoint import TargetPoint

class PlaneGeometry:
    def get_distance_between_two_points(self, point1: TargetPoint, point2: TargetPoint):
        x_subtraction = point2.x - point1.x
        y_subtraction = point2.y - point1.y
        
        return math.sqrt(x_subtraction * x_subtraction + y_subtraction * y_subtraction)
    