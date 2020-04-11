from random import randint
from datetime import datetime
from TargetPoint import TargetPoint
from Vehicle import Vehicle
from VehicleRouting import RoutePoint, VehicleRouting
from DisplayRoutes import DisplayRoutes
from ProcessInstances import ProcessInstances
from NeighborhoodMovements import NeighborhoodMovements
from VariableNeighborhoodDescent import VariableNeighborhoodDescent
from CreateTable import CreateTable

import json
import pandas as pd

processaDados = ProcessInstances()
arquivos = ["P-n16-k8", "P-n19-k2", "P-n20-k2", "P-n23-k8", "P-n45-k5", "P-n50-k10", "P-n51-k10", "P-n55-k7"]
qtd_arquivos = len(arquivos)
arquivo_otimo = "otimos"

table = CreateTable(arquivos)

for archive_name in arquivos:

    archive = "instancias_teste/" + archive_name + ".txt"
    best_solution_archive = "info_instancias/" + arquivo_otimo + ".txt"

    processaDados.load_data(archive)
    processaDados.read_best_solution(best_solution_archive, archive_name)

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

    #Criamos a instância do veículo
    table.instance_validate(archive_name, "create", 0)
    table.instance_validate(archive_name, "otimo", int(processaDados.get_best_solution()))

    qtd_execuções = 10
    while(qtd_execuções):
        #Execução do HC

        #Iniciamos o time, assim poderemos pegar o tempo da melhor solução
        start_time = datetime.now()

        routes = VehicleRouting().get_routes_using_nearest_neighbor(points, 0, float(processaDados.get_capacity()[0]), random_max_range = 3)

        #Aqui nós finalizamos o tempo, para saber o tempo da atual solução
        end_time = datetime.now()

        total_hc = 0.0
        for route in routes:
            total_hc += route.total_distance

        table.instance_validate(archive_name, "hc_time", (end_time - start_time).total_seconds())

        #Aqui nós salvamos o total da atual distância
        table.instance_validate(archive_name, "hc_value", total_hc)


        #routes = NeighborhoodMovements().apply_movement_in_routes("2-opt", routes)
        #Execução do VND

        #Inicamos o tempo para a solução
        start_time = datetime.now()

        routes = VariableNeighborhoodDescent().execute_vnd(routes)

        #Agora pegamos o tempo da solução
        end_time = datetime.now()

        total_vnd = 0.0
        for route in routes:
            total_vnd += route.total_distance

        #Setamos então os valores da solução e seu tempo
        table.instance_validate(archive_name, "vnd_value", total_vnd)
        table.instance_validate(archive_name, "vnd_time", (end_time - start_time).total_seconds())

        qtd_execuções -= 1

        # for route in routes:
        #     print(route)

    table.instance_validate(archive_name, "process_data", "")

table_dataframe = table.get_table_dataframe()
table_json = table.get_table_json()

table_dataframe.to_excel("resultado/tabela.xlsx")
