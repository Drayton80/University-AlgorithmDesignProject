import pandas as pd
import copy

class CreateTable:

    def __init__(self, lista_instancias):
        self.table = {}
        self.index = lista_instancias
        self.columns = ["otimo", "HC", "Média solução", "Melhor Solução", "Média Tempo", "gap", "VND","Média solução", "Melhor Solução", "Média Tempo", "gap"]

    def __format_table(self):

        row_list = []
        for name_instance in self.table:
            complete_row = [self.table[name_instance]['otimo'], "|", self.table[name_instance]['media_solu_hc'], self.table[name_instance]['melhor_hc'], self.table[name_instance]['media_tempo_hc'], self.table[name_instance]['gap_hc'], "|", self.table[name_instance]['media_solu_vnd'], self.table[name_instance]['melhor_vnd'], self.table[name_instance]['media_tempo_vnd'], self.table[name_instance]['gap_vnd']]

            row_list.append(copy.deepcopy(complete_row))

        tabela = pd.DataFrame(row_list, index = self.index, columns = self.columns)

        return tabela
    #------------------------------
    #Funções Auxiliares
    #------------------------------
    def __create_instance(self, instance_name):

        if(instance_name not in self.table):
            print("instance_name:", instance_name)
            self.table[instance_name] = {}

            self.table[instance_name]['otimo'] = 0

            #Cria index da Heuristica Construtiva
            self.table[instance_name]['valores_solu_hc'] = []
            self.table[instance_name]['media_solu_hc'] = 0.0
            self.table[instance_name]['melhor_hc'] = 0.0
            self.table[instance_name]['valores_tempo_hc'] = []
            self.table[instance_name]['media_tempo_hc'] = 0.0
            self.table[instance_name]['gap_hc'] = 0.0

            #Cria index do vnd
            self.table[instance_name]['valores_solu_vnd'] = []
            self.table[instance_name]['media_solu_vnd'] = 0.0
            self.table[instance_name]['melhor_vnd'] = 0.0
            self.table[instance_name]['valores_tempo_vnd'] = []
            self.table[instance_name]['media_tempo_vnd'] = 0.0
            self.table[instance_name]['gap_vnd'] = 0.0

        return

    def __calculate_media(self, list):

        qtd_values = len(list)
        max_value = sum(list)

        media_values = (max_value/qtd_values)

        return media_values

    def __calculate_gap(self, value_otimo, value):

        gap = (((value - value_otimo)/value_otimo) * 100)
        gap = "{:.2f}".format(gap)
        gap = str(gap) + "%"

        return gap

    def __process__data(self, instance_name):

        #Processa HC
        media_hc = self.__calculate_media(self.table[instance_name]['valores_solu_hc'])
        self.table[instance_name]['media_solu_hc'] = media_hc

        media_vnd = self.__calculate_media(self.table[instance_name]['valores_solu_vnd'])
        self.table[instance_name]['media_solu_vnd'] = media_vnd

        self.table[instance_name]['melhor_hc'] = min(self.table[instance_name]['valores_solu_hc'])
        self.table[instance_name]['melhor_vnd'] = min(self.table[instance_name]['valores_solu_vnd'])

        media_tempo_hc = self.__calculate_media(self.table[instance_name]['valores_tempo_hc'])
        self.table[instance_name]['media_tempo_hc'] = media_tempo_hc

        list_time_hc_vnd = []
        for value_hc, value_vnd in zip(self.table[instance_name]['valores_tempo_hc'], self.table[instance_name]['valores_tempo_vnd']):
            list_time_hc_vnd.append(value_hc + value_vnd)

        media_tempo_vnd = self.__calculate_media(list_time_hc_vnd)
        self.table[instance_name]['media_tempo_vnd'] = media_tempo_vnd

        self.table[instance_name]['gap_hc'] = self.__calculate_gap(self.table[instance_name]['otimo'], self.table[instance_name]['melhor_hc'])

        self.table[instance_name]['gap_vnd'] = self.__calculate_gap(self.table[instance_name]['otimo'], self.table[instance_name]['melhor_vnd'])

    def __add_otimo(self, instance_name, value):
        self.table[instance_name]['otimo'] = value
        return
    #------------------------------

    #------------------------------
    #Funções Heuristica Construtiva
    #------------------------------
    def __add_value_hc(self, instance_name, value):

        # print("Add Value HC")
        self.table[instance_name]['valores_solu_hc'].append(value)
        return

    def __add_time_hc(self, instance_name, time):

        # print("Add Time HC")
        self.table[instance_name]['valores_tempo_hc'].append(time)
        return
    #------------------------------

    #------------------------------
    #Funções Variable Neighborhood Descent (VND)
    #------------------------------
    def __add_value_vnd(self, instance_name, value):

        # print("Add Value VND")
        self.table[instance_name]['valores_solu_vnd'].append(value)
        return

    def __add_time_vnd(self, instance_name, time):

        # print("Add Time VND")
        self.table[instance_name]['valores_tempo_vnd'].append(time)
        return
    #------------------------------#

    def instance_validate(self, instance_name, type, value):
        # print("Cria e Valida Instância!")

        instance_name = str(instance_name)

        if(type != "create"):
            if(type == "hc_value"):
                self.__add_value_hc(instance_name, value)
            elif(type == "hc_time"):
                self.__add_time_hc(instance_name, value)
            elif(type == "vnd_value"):
                self.__add_value_vnd(instance_name, value)
            elif(type == "vnd_time"):
                self.__add_time_vnd(instance_name, value)
            elif(type == "otimo"):
                self.__add_otimo(instance_name, value)
            elif(type == "process_data"):
                self.__process__data(instance_name)
        else:
            self.__create_instance(instance_name)

        return

    def get_table_json(self):
        return self.table

    def get_table_dataframe(self):
        tabela_excel = self.__format_table()
        return tabela_excel
