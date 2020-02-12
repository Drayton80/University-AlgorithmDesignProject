from random import randint
from TargetPoint import TargetPoint
from Vehicle import Vehicle
from VehicleRouting import RoutePoint, VehicleRouting
from DisplayRoutes import DisplayRoutes
from ProcessInstances import ProcessInstances

processaDados = ProcessInstances()
archive = "instancias_teste/teste.txt"
processaDados.load_data(archive)
print("Dados:", processaDados.get_edgeWeightSection())

storehouse = None
points = []

distance_per_point = processaDados.get_edgeWeightSection()
value_per_point = processaDados.get_demandSection()

for i in range(len(value_per_point)):
    distances = []
    for distance in distance_per_point[i]:
        distances.append(float(distance))
    
    if i == 0:
        storehouse = RoutePoint(i, distances, None, float(value_per_point[i]))
    else:
        points.append(RoutePoint(i, distances, None, float(value_per_point[i])))


#routes = VehicleRouting().get_routes_using_nearest_neighbor(storehouse, points,)
'''
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
'''