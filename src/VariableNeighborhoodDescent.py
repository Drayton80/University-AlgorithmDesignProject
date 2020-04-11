from NeighborhoodMovements import NeighborhoodMovements
from VehicleRouting import Route
from datetime import datetime
import copy

class VariableNeighborhoodDescent():

    def __vnd(self, route: Route):
        # print("----------------------------------")
        # print("VND")
        #Solução atual
        current_route = copy.deepcopy(route)

        #Melhor solução
        best_route = copy.deepcopy(route)

        #Número da estrutura de vizinhança
        k = 0

        #Tipos de algoritmos
        types_algorithms = ["insertion", "swap", "2-opt"]
        #Quantidade dos algoritmos
        qtd_algorithms = len(types_algorithms)

        # print("================================")

        while(k < qtd_algorithms):

            algorithm = types_algorithms[k]

            current_route = NeighborhoodMovements().apply_movement_in_route(algorithm, best_route)
            current_route.recalculate_route_values()

            # print("---------===============-------------")
            # print("current_route.total_distance:", current_route.total_distance)
            # print("best_route.total_distance):", best_route.total_distance)
            # print("----------------------------------")

            if(current_route.total_distance < best_route.total_distance):
                best_route = copy.deepcopy(current_route)
                k = 0
            else:
                k += 1

        #     print("Valor do K depois:", k)
        # print("================================")

        # print("Sai a rota:", best_route)
        # print("----------------------------------")

        return best_route

    def execute_vnd(self, routes: list):
        # print("Execute VND!")
        routes_changed = routes.copy()

        for count in range(len(routes_changed)):
            route = Route(routes_changed[count].vehicle, routes_changed[count].total_distance, routes_changed[count].points_sequence)
            route = self.__vnd(route)
            routes_changed[count] = route

        return routes_changed
