from random import randint

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
    def __init__(self, vehicle: Vehicle, total_distance: float, points_sequence: list):
        self.vehicle = vehicle
        self.total_distance = total_distance
        self.points_sequence = points_sequence

    def __str__(self):
        route_points = ''

        for route_point in self.points_sequence:
            route_points += route_point.__str__()

        return 'Veículo: ' + self.vehicle.__str__() + '\nPontos da Rota:\n' + route_points + 'Distância Percorrida Total da Rota: ' + str(self.total_distance) + '\n'
    
    # Quando a rota é alterada, recalcula a distância total e as novas distâncias até o próximo ponto de cada ponto na rota:
    def recalculate_route_values(self):
        # Recalcula a distância para o próximo ponto de todos com exceção do ultimo (que é o storehouse):
        for point_index in range(len(self.points_sequence) - 1):
            self.points_sequence[point_index].next_point_distance = self.points_sequence[point_index].all_points_distances[self.points_sequence[point_index+1].number_id]

        self.total_distance = 0
        # Agora que as distâncias para o próximo foram recalculadas é possível corrigir a distância total da rota:
        for point in self.points_sequence:
            self.total_distance += point.next_point_distance

    # Insere um ponto em outro índice da rota:
    def insert_point_in_other_index(self, previous_index: int, next_index: int, recalculate_route=True):
        self.points_sequence.insert(next_index, self.points_sequence.pop(previous_index))
        
        if recalculate_route:
            self.recalculate_route_values()
    
    # Troca dois pontos entre si na rota:
    def swap_points(self, index1: int, index2: int, recalculate_route=True):
        self.points_sequence[index1], self.points_sequence[index2] = self.points_sequence[index2], self.points_sequence[index1]
        
        if recalculate_route:
            self.recalculate_route_values()

class VehicleRouting:    
    # Dado um conjunto de veiculos e uma matriz de distâncias entre cada ponto, retorna as
    # possíveis rotas que cada veiculo poderia fazer baseado na Heurística do Vizinho mais Próximo
    # 
    # Parâmetros:
    #   storehouse_index: um inteiro que indica na lista de pontos qual é o centro de distribuição (aqui denomidado de storehouse)
    #   points: uma lista de RoutePoint, o qual contém todas as informações disponível para cada ponto
    #   vehicle_max_value: o número de veículos é ilimitado, então aqui é passado apenas o máximo que eles conseguem carregar
    def get_routes_using_nearest_neighbor(self, points: list, storehouse_index: int, vehicle_max_value: float, random_max_range = 5):
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

                nearest_neighboors = [{'distance': None, 'index': None} for _ in range(random_max_range)]
                
                # Itera para obter todos os vizinhos mais próximos possíveis:
                for index_nearest_list in range(len(nearest_neighboors)):
                    nearest_indexes = [nearest_neighboor['index'] for nearest_neighboor in nearest_neighboors]
                    # Checa todos os pontos ainda não adicionados em alguma rota para
                    # encotnrar um dos vizinhos mais próximos:
                    for index in not_visited_points_indexes:
                        # Se o índice dos não visitados já estiver na lista de vizinhos mais próximos
                        # ele pode ser ignorado e as iterações continuam:
                        if index in nearest_indexes:
                            continue
                        # Caso não haja um vizinho mais próximo na posição atual da lista de vizinhos mais próximos, pega o primeiro vizinho
                        # como mais próximo, nas iterações subsequentes, ele colocará como mais próximo aqueles que tiverem uma distância
                        # menor que o atual e que o valor não exceda a capacidade atual do veículo:
                        if (not nearest_neighboors[index_nearest_list]['distance'] or all_points_distances[index] < nearest_neighboors[index_nearest_list]['distance']) and points[index].value <= current_vehicle.max_value:
                            nearest_neighboors[index_nearest_list]['distance'] = all_points_distances[index]
                            nearest_neighboors[index_nearest_list]['index'] = index

                # Remove os elementos que estão vazios, ou seja, qualquer um que não for realmente um vizinho mais próximo:
                nearest_neighboors = [nearest_neighboor for nearest_neighboor in nearest_neighboors if nearest_neighboor['distance'] != None]

                # Se não houver um vizinho que seja possível o veiculo visitar 
                # ou se todos os pontos já foram visitados não haverá outro ponto na sequência:
                if not nearest_neighboors or not not_visited_points_indexes:
                    # Então restará ao veiculo apenas retornar para o centro de distribuição:
                    selected_nearest_neighboor = {'distance': route[-1].all_points_distances[storehouse_index], 'index': storehouse_index}
                    vehicle_returned_to_storehouse = True
                else:
                    # Escolhe randomicamente um dos vizinhos da lista de vizinhos mais próximos:
                    random_index = randint(0, len(nearest_neighboors)-1)
                    selected_nearest_neighboor = {'distance': nearest_neighboors[random_index]['distance'], 'index': nearest_neighboors[random_index]['index']}
                    # Caso ainda haja pontos, remove da lista o ponto que foi visitado:
                    not_visited_points_indexes.remove(nearest_neighboors[random_index]['index'])

                route[-1].next_point_distance = selected_nearest_neighboor['distance']

                route.append(points[selected_nearest_neighboor['index']].copy())
                total_distance += selected_nearest_neighboor['distance']
                current_vehicle.max_value -= points[selected_nearest_neighboor['index']].value

            route[-1].next_point_distance = 0
            routes.append(Route(current_vehicle, total_distance, route))

            vehicle_number += 1

        return routes
