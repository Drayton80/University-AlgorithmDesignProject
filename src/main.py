from random import randint
from TargetPoint import TargetPoint
from Vehicle import Vehicle
from VehicleRouting import VehicleRouting
from DisplayRoutes import DisplayRoutes

points = []
vehicles = []

for number in range(3):
    vehicles.append(Vehicle(str(number), 30))

for _ in range(30):
    x = randint(0,40)
    y = randint(0,40)
    value = randint(1,20)

    points.append(TargetPoint(x, y, value))


storehouse = TargetPoint(randint(0,40), randint(0,40), 0)


routes = VehicleRouting().closest_neighbor_heuristic(storehouse, points, vehicles)

print(routes[0])

DisplayRoutes().plot_graph(routes, storehouse, points)