class TargetPoint:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def get_coordinates(self):
        return (self.x, self.y)

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
        