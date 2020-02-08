import matplotlib.pyplot as plt
from random import random
from TargetPoint import TargetPoint

class DisplayRoutes:
    def _get_coordinates_separated(self, points: list):
        x_coordinates = []
        y_coordinates = []

        for point in points:
            x_coordinates.append(point.x)
            y_coordinates.append(point.y)

        return (x_coordinates, y_coordinates)
    
    def _draw_points(self, points: list, color):
        coordinates = self._get_coordinates_separated(points)
        x_coordinates = coordinates[0]
        y_coordinates = coordinates[1]

        plt.scatter(x_coordinates, y_coordinates, s=20, color=color, zorder=1)

    def _draw_lines(self, points: list, color):
        coordinates = self._get_coordinates_separated(points)
        x_coordinates = coordinates[0]
        y_coordinates = coordinates[1]

        plt.plot(x_coordinates, y_coordinates, linewidth=2, color=color, zorder=0)

    def plot_graph(self, routes: list, storehouse, remaining_points):
        if remaining_points:
            self._draw_points(remaining_points, (0.3, 0.3, 0.3)) 
        
        for route in routes:            
            red = random()
            green = random()
            blue = random()

            self._draw_lines(route.route, (red, green, blue))
            self._draw_points(route.route, (0.3, 0.3, 0.3))  

        plt.scatter(storehouse.x, storehouse.y, s=80, color=(0.0, 0.0, 0.0))
        plt.show()
            

            




