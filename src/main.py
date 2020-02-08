from random import randint
from TargetPoint import TargetPoint
from Vehicle import Vehicle
from VehicleRouting import VehicleRouting
from DisplayRoutes import DisplayRoutes

points = []
vehicles = []

for number in range(10):
    vehicles.append(Vehicle(str(number), 30))

for _ in range(30):
    x = randint(0,40)
    y = randint(0,40)
    value = randint(5,20)

    points.append(TargetPoint(x, y, value))


storehouse = TargetPoint(randint(18,22), randint(18,22), 0)


routes = VehicleRouting().get_all_routes_using_nearest_neighbor(storehouse, points, vehicles)

print(routes[0])

DisplayRoutes().plot_graph(routes, storehouse, points)