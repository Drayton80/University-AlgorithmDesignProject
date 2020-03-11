class NeighborhoodMovements:
    def _get_routes_total_distance(self, routes: list):
        routes_tota_distance = 0

        for route in routes:
            routes_tota_distance += route.total_distance

        return routes_tota_distance
    
    def insertion(self, routes: list):
        best_movement = {'greater distance reduction': 0, 'route index': None, 'point index': None, 'insertion index': None}
        
        for index_route in range(len(routes)):
            for index_point in range(len(routes[index_route].points_sequence)):
                # O storehouse é o unico que não pode ser alterado de lugar pois ele deve permanecer
                # sempre como o primeiro e último ponto da rota, então ele pode ser ignorado:
                if not routes[index_route].points_sequence[index_point].number_id == 0:
                    # Para cada indice de inserção possível, ou seja, do primeiro até o penultimo (pois o storehouse deve ser ignorado)
                    for point_insertion_index in range(1, len(routes[index_route].points_sequence)-1):
                        # O novo local de inserção não pode ser igual ao proprio ponto nem no local do proximo ponto 
                        # logo em seguida na sequência pois isso colocaria o ponto na exata posição em que ele já está:
                        if not point_insertion_index == index_point and not point_insertion_index == index_point + 1:
                            new_route_distance = routes[index_route].total_distance
                            route_sequence_points = routes[index_route].points_sequence

                            # OBS.: como o primeiro e o ultimo ponto da lista sempre são desconsiderados (já que o storehouse não entra
                            #       nessa checagem do movimento), não é necessário fazer qualquer tratamento com relação 
                            #       ao caso do -1 ou +1 dos indices ultrapassarem os limites da lista:

                            # Subtração da aresta anterior ao ponto que será inserido
                            new_route_distance -= route_sequence_points[index_point-1].next_point_distance
                            # Subtração da aresta posterior ao ponto que será inserido
                            new_route_distance -= route_sequence_points[index_point].next_point_distance
                            # Subtração da aresta em que o ponto será inserido
                            new_route_distance -= route_sequence_points[point_insertion_index-1].next_point_distance

                            # Soma da conexão entre o ponto anterior ao que foi movido com o posterior ao que foi movido 
                            new_route_distance += route_sequence_points[index_point-1].all_points_distances[route_sequence_points[index_point+1].number_id]
                            # Soma da conexão entre o primeiro ponto da aresta onde o ponto será inserido com o ponto que será inserido
                            new_route_distance += route_sequence_points[point_insertion_index-1].all_points_distances[route_sequence_points[index_point].number_id]
                            # Soma da conexão entre o ponto que será inserido com o segundo ponto da aresta em que ele será inserido:
                            new_route_distance += route_sequence_points[index_point].all_points_distances[route_sequence_points[point_insertion_index].number_id]

                            route_distance_reduction = routes[index_route].total_distance - new_route_distance
                            
                            # Primeiramente checa se a redução de distância que o movimento gera é maior que zero, ou seja, se o movimento
                            # aplicado teve uma mudança positiva reduzindo a distância total da rota, já nas próximas checagens
                            # checará se a redução atual é maior do que a melhor redução já feita dentre os movimentos:
                            if route_distance_reduction > best_movement['greater distance reduction']:
                                best_movement['greater distance reduction'] = route_distance_reduction
                                best_movement['route index'] = index_route
                                best_movement['point index'] = index_point
                                best_movement['insertion index'] = point_insertion_index
        
        if best_movement['insertion index'] != None:
            routes_changed = routes.copy()
            # Retira o ponto da sua posição anterior:
            point_inserted = routes_changed[best_movement['route index']].points_sequence.pop(best_movement['point index'])
            # Insere o ponto em sua nova posição:
            routes_changed[best_movement['route index']].points_sequence.insert(best_movement['insertion index'], point_inserted)
            # Recalcula os valores da rota agora que as posições foram alteradas:
            routes_changed[best_movement['route index']].recalculate_route_values()

            return routes_changed
        else:
            return routes


    def swap(self, routes: list):
        for index_route in range(len(routes)):
            # O índice 0 e len-1 não precisam
            # ser iterados sobre pois ambos representam o storehouse:
            for index_first in range(1, len(routes[index_route].points_sequence)-1):
                # Não é preciso checar com pontos anteriores ao primeiro 
                # ponto pois essa combinação já foi checada em iterações anteriores
                # e o for começa em index_first+1 pois o ponto não irá trocar de lugar com ele mesmo:
                for index_second in range(index_first+1, len(routes[index_route].points_sequence)-1):
                    pass

    def two_opt(self, routes: list):
        for index_route in range(len(routes)):
            # Colocar o final da iteração em len-4 garante que na ultima iteração
            # o primeiro ponto esteja no máximo 4 posições antes do final da lista
            # fazendo com que o p2 da aresta 2 esteja exatamente na ultima posição
            # da lista, garantindo que uma posição fora dela não seja acessada:
            for first_edge_p1 in range(0, len(routes[index_route].points_sequence)-4):
                first_edge_p2 = first_edge_p1 + 1
                # O p1 da segunda aresta sempre fica duas posições além do p2 da primeira aresta
                # e ir até -1 no final garante que o p2 da aresta 2 no máximo chegue até a ultima posição:
                for second_edge_p1 in range(first_edge_p2+2, len(routes[index_route].points_sequence)-1):
                    second_edge_p2 = second_edge_p1 + 1