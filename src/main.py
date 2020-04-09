from random import randint
from TargetPoint import TargetPoint
from Vehicle import Vehicle
from VehicleRouting import RoutePoint, VehicleRouting
from DisplayRoutes import DisplayRoutes
from ProcessInstances import ProcessInstances
from NeighborhoodMovements import NeighborhoodMovements
from VariableNeighborhoodDescent import VariableNeighborhoodDescent

processaDados = ProcessInstances()
archive = "instancias_teste/P-n51-k10.txt"
processaDados.load_data(archive)
#print("Dados:", processaDados.get_edgeWeightSection())

storehouse = None
points = []

distance_per_point = processaDados.get_edgeWeightSection()
value_per_point = processaDados.get_demandSection()

for i in range(len(value_per_point)):
    distances = []
    for distance in distance_per_point[i]:
        distances.append(float(distance))

    points.append(RoutePoint(i, distances, None, float(value_per_point[i][1])))

routes = VehicleRouting().get_routes_using_nearest_neighbor(points, 0, float(processaDados.get_capacity()[0]))

# for route in routes:
#     print(route)

#routes = NeighborhoodMovements().apply_movement_in_routes("2-opt", routes)
routes = VariableNeighborhoodDescent().execute_vnd(routes)

for route in routes:
    print(route)

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
