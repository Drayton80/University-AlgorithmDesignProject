from PlaneGeometry import PlaneGeometry
from TargetPoint import TargetPoint
from Vehicle import Vehicle

class Route:
    def __init__(self, vehicle: Vehicle, route: list, distance: float):
        self.vehicle = vehicle
        self.route = route
        self.distance = distance

class VehicleRouting:
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
        


            

            
            
