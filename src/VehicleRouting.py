from PlaneGeometry import PlaneGeometry
from TargetPoint import TargetPoint

class Vehicle:
    def __init__(self, name: str, max_value: float):
        self.name = name
        self.max_value = max_value

    def __str__(self):
        return 'Nome: ' + str(self.name) + ', Valor Restante: ' + str(self.max_value) + ';'


class RoutePoint:
    def __init__(self, number_id: int, all_points_distances: list, next_point_distance: float, value: float):
        self.number_id = number_id
        self.all_points_distances = all_points_distances
        self.next_point_distance = next_point_distance
        self.value = value
    
    def __str__(self):
        return 'ID: ' + str(self.number_id) + ', Distância para o Próximo Ponto: ' + str(self.next_point_distance) + ', Valor:' + str(self.value) + '\n'

    def copy(self):
        return RoutePoint(self.number_id, self.all_points_distances, self.next_point_distance, self.value)


class Route:
    def __init__(self, vehicle: Vehicle, total_distance: float, route_points_sequence: list):
        self.vehicle = vehicle
        self.total_distance = total_distance
        self.route_points_sequence = route_points_sequence

    def __str__(self):
        route_points = ''

        for route_point in self.route_points_sequence:
            route_points += route_point.__str__()

        return 'Veículo: ' + self.vehicle.__str__() + '\nPontos da Rota:\n' + route_points + 'Distância Percorrida Total da Rota: ' + str(self.total_distance) + '\n'

    '''
    def __init__(self, vehicle: Vehicle, route: list, distance: float):
        self.vehicle = vehicle
        self.route = route
        self.distance = distance
    '''


class VehicleRouting:    
    # Dado um conjunto de veiculos e uma matriz de distâncias entre cada ponto, retorna as
    # possíveis rotas que cada veiculo poderia fazer baseado na Heurística do Vizinho mais Próximo
    # 
    # Parâmetros:
    #   storehouse_index: um inteiro que indica na lista de pontos qual é o centro de distribuição (aqui denomidado de storehouse)
    #   points: uma lista de RoutePoint, o qual contém todas as informações disponível para cada ponto
    #   vehicle_max_value: o número de veículos é ilimitado, então aqui é passado apenas o máximo que eles conseguem carregar
    def get_routes_using_nearest_neighbor(self, points: list, storehouse_index: int, vehicle_max_value: float):
        # Cria uma lista com todos os indices dos pontos que não foram visitados ainda:
        not_visited_points_indexes = list(range(len(points)))
        # Como os veiculos sempre saem do storehouse, ele certamente já foi visitado:
        not_visited_points_indexes.remove(storehouse_index)
        # Cria-se uma lista de rotas vazias:
        routes = []

        vehicle_number = 0

        while not_visited_points_indexes:
            # Inicializa uma rota com o storehouse como ponto de partida:
            route = [RoutePoint(points[storehouse_index].number_id, points[storehouse_index].all_points_distances, 0, 0)]
            total_distance = 0
            current_vehicle = Vehicle(vehicle_number, vehicle_max_value)
            
            vehicle_returned_to_storehouse = False

            while not vehicle_returned_to_storehouse:
                # É checado a distância para todos os pontos com relação ao ponto anterior da sequência:
                all_points_distances = route[-1].all_points_distances
                
                closest_point_distance = None
                closest_point_index = None

                for index in not_visited_points_indexes:
                    if (not closest_point_distance or all_points_distances[index] < closest_point_distance) and points[index].value < current_vehicle.max_value:
                        closest_point_distance = all_points_distances[index]
                        closest_point_index = index

                # Se não houver um vizinho que seja possível o veiculo visitar 
                # ou se todos os pontos já foram visitados não haverá outro ponto na sequência:
                if not closest_point_distance or not not_visited_points_indexes:
                    # Então restará ao veiculo apenas retornar para o centro de distribuição:
                    closest_point_distance = route[-1].all_points_distances[storehouse_index]
                    closest_point_index = storehouse_index
                    vehicle_returned_to_storehouse = True
                else:
                    # Caso ainda haja pontos, remove da lista o ponto que foi visitado:
                    not_visited_points_indexes.remove(closest_point_index)
                
                route[-1].next_point_distance = closest_point_distance

                route.append(points[closest_point_index].copy())
                total_distance += closest_point_distance
                current_vehicle.max_value -= points[closest_point_index].value

            route[-1].next_point_distance = 0
            routes.append(Route(current_vehicle, total_distance, route))

            vehicle_number += 1

        return routes


    '''
    def get_route_using_nearest_neighbor(self, storehouse: TargetPoint, previous_point: TargetPoint, points: list, vehicle: list):       
        vehicle_route = [storehouse]
        route_distance = 0

        while points and vehicle.max_value > 0:
            closest_neighbor_point = None
            closest_neighbor_index = None
            distance_to_closest_neighbor = 0

            i = 0
            for point in points:
                if not closest_neighbor_point:
                    closest_neighbor_point = point
                    closest_neighbor_index = i
                else:
                    distance_to_closest_neighbor = PlaneGeometry().get_distance_between_two_points(previous_point, closest_neighbor_point)
                    distance_to_current_point = PlaneGeometry().get_distance_between_two_points(previous_point, point)

                    if distance_to_current_point < distance_to_closest_neighbor and point.value < vehicle.max_value:
                        closest_neighbor_point = point
                        closest_neighbor_index = i
                
                i += 1
            
            vehicle.max_value -= closest_neighbor_point.value
            route_distance += distance_to_closest_neighbor
            vehicle_route.append(closest_neighbor_point)
            previous_point = points.pop(closest_neighbor_index)
        
        # É preciso fazer a ligação com o primeiro ponto para fechar o ciclo da rota:
        route_distance += PlaneGeometry().get_distance_between_two_points(previous_point, storehouse)
        vehicle_route.append(storehouse)

        return Route(vehicle, vehicle_route, route_distance)

    def get_route_using_nearest_neighbor_head_and_tail(self, storehouse: TargetPoint, head_point: TargetPoint, tail_point: TargetPoint, points: list, vehicle: list):       
        route = [storehouse]
        distance = 0

        while points and vehicle.max_value > 0:
            head_closest_neighbor_point = None
            head_closest_neighbor_index = None
            head_distance_to_closest_neighbor = 0

            tail_closest_neighbor_point = None
            tail_closest_neighbor_index = None
            tail_distance_to_closest_neighbor = 0
            
            i = 0
            for point in points:
                if not head_closest_neighbor_point:
                    head_closest_neighbor_point = point
                    head_closest_neighbor_index = i
                else:
                    head_distance_to_closest_neighbor = PlaneGeometry().get_distance_between_two_points(head_point, head_closest_neighbor_point)
                    head_distance_to_current_point = PlaneGeometry().get_distance_between_two_points(head_point, point)

                    if head_distance_to_current_point < head_distance_to_closest_neighbor and point.value < vehicle.max_value:
                        head_closest_neighbor_point = point
                        head_closest_neighbor_index = i
                
                i += 1
            
            j = 0
            for point in points:
                if not tail_closest_neighbor_point:
                    tail_closest_neighbor_point = point
                    tail_closest_neighbor_index = j
                else:
                    tail_distance_to_closest_neighbor = PlaneGeometry().get_distance_between_two_points(tail_point, tail_closest_neighbor_point)
                    tail_distance_to_current_point = PlaneGeometry().get_distance_between_two_points(tail_point, point)

                    if tail_distance_to_current_point < tail_distance_to_closest_neighbor and point.value < vehicle.max_value:
                        tail_closest_neighbor_point = point
                        tail_closest_neighbor_index = j
                
                j += 1

            if head_distance_to_closest_neighbor < tail_distance_to_closest_neighbor:
                route.append(head_closest_neighbor_point)
                vehicle.max_value -= head_closest_neighbor_point.value
                distance += head_distance_to_closest_neighbor
                head_point = points.pop(head_closest_neighbor_index)
                distance += PlaneGeometry().get_distance_between_two_points(head_point, storehouse)
            else:
                route.append(tail_closest_neighbor_point)
                vehicle.max_value -= tail_closest_neighbor_point.value
                distance += tail_distance_to_closest_neighbor
                tail_point = points.pop(tail_closest_neighbor_index)
                distance += PlaneGeometry().get_distance_between_two_points(tail_point, storehouse)

        # É preciso fazer a ligação com o primeiro ponto para fechar o ciclo da rota:
        route.append(storehouse)

        return Route(vehicle, route, distance)

    def get_all_routes_using_nearest_neighbor(self, storehouse: TargetPoint, points: list, vehicles: list):
        routes = []

        for vehicle in vehicles:
            previous_point = TargetPoint(storehouse.x, storehouse.y, storehouse.value)
            routes.append(self.get_route_using_nearest_neighbor(storehouse, previous_point, points, Vehicle(vehicle.name, vehicle.max_value)))

        return routes

    def get_all_routes_using_both_nearest_neighbor(self, storehouse: TargetPoint, points: list, vehicles: list):
        routes = []

        for vehicle in vehicles:
            previous_point = TargetPoint(storehouse.x, storehouse.y, storehouse.value)
            head_point = TargetPoint(storehouse.x, storehouse.y, storehouse.value)
            tail_point = TargetPoint(storehouse.x, storehouse.y, storehouse.value)
            # Faz uma cópia para aplicar em cada gerador de rota pois internamente do método a lista é alterada 
            # pois é usado passagem por referência, então é preciso manter a lista original intacta até a checagem final:
            points_for_nearest_neighbor = points.copy()
            points_for_nearest_neighbor_ht = points.copy()

            nearest_neighbor_route = self.get_route_using_nearest_neighbor(storehouse, previous_point, points_for_nearest_neighbor, Vehicle(vehicle.name, vehicle.max_value))
            nearest_neighbor_ht_route = self.get_route_using_nearest_neighbor_head_and_tail(storehouse, head_point, tail_point, points_for_nearest_neighbor_ht, Vehicle(vehicle.name, vehicle.max_value))

            if nearest_neighbor_route.distance < nearest_neighbor_ht_route.distance:
                # Adiciona-se a rota com menor distância:
                routes.append(nearest_neighbor_route)
                # Apos ser feita a checagem final é possível alterar a lista original para deletar os pontos que já possuem uma rota:
                points = points_for_nearest_neighbor.copy()
            else:
                # Adiciona-se a rota com menor distância:
                routes.append(nearest_neighbor_ht_route)
                # Apos ser feita a checagem final é possível alterar a lista original para deletar os pontos que já possuem uma rota:
                points = points_for_nearest_neighbor_ht.copy()

        return routes
    '''


            

            
            
