from PlaneGeometry import PlaneGeometry
from TargetPoint import TargetPoint
from Vehicle import Vehicle


class VehicleRouting:    
    def closest_neighbor_heuristic(self, storehouse: TargetPoint, points: list, vehicles: list):       
        aux_points = list(points)
        routes = []
        
        for vehicle in vehicles:
            vehicle_route = [storehouse]
            route_distance = 0
            previous_point = storehouse
            
            while aux_points and vehicle.max_value > 0:
                closest_neighbor_point = None
                closest_neighbor_index = None
                distance_to_closest_neighbor = 0

                i = 0
                for point in aux_points:
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

                if not closest_neighbor_index:
                    break
                
                vehicle.max_value -= closest_neighbor_point.value
                route_distance += distance_to_closest_neighbor
                vehicle_route.append(closest_neighbor_point)
                previous_point = aux_points.pop(closest_neighbor_index)
            
            route_distance += PlaneGeometry().get_distance_between_two_points(previous_point, storehouse)
            vehicle_route.append(storehouse)
            routes.append({"vehicle": vehicle, "route": vehicle_route, "distance": route_distance})

        return routes


            

            
            
