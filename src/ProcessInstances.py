import numpy as np

class ProcessInstances:

    def _init_(self):
        self.data = []
        self.NAME = ""
        self.DIMENSION = 0
        self.CAPACITY = 0
        self.DEMAND_SECTION = []
        self.EDGE_WEIGHT_SECTION = []
        self.best_solution = 0

    def load_data(self, path_archive):

        data = open(path_archive, "r")
        self.data = data
        self.__separate_data(data)

    def read_best_solution(self, path_archive, archive_name):
        data = open(path_archive, "r")
        data = data.read()
        data = data.split("\n")

        for count in range(len(data)):

            result = data[count].split("=")

            if(str(result[0]).strip() == archive_name):
                self.best_solution = result[1]

    def __separate_data(self, data):

        data = data.read()
        data = data.split(":")
        data = " ".join(data)

        self.NAME = self.__processAtributes(data, "NAME")
        #print("NAME:", self.NAME, "\n")

        self.DIMENSION = self.__processAtributes(data, "DIMENSION")
        #print("DIMENSION:", self.DIMENSION, "\n")

        self.CAPACITY = self.__processAtributes(data, "CAPACITY")
        #print("CAPACITY:", self.CAPACITY, "\n")

        self.DEMAND_SECTION = self.__processPoints(self.__processAtributes(data, "DEMAND_SECTION"))
        #print("DEMAND_SECTION:", self.DEMAND_SECTION, "\n")

        self.EDGE_WEIGHT_SECTION = self.__processPoints(self.__processAtributes(data, "EDGE_WEIGHT_SECTION"))
        #print("EDGE_WEIGHT_SECTION:", self.EDGE_WEIGHT_SECTION, "\n")

    def __processAtributes(self, data, name):

        data = data.split(name)
        data = data[1:]
        data = " ".join(data)
        data = data.split("\n")
        #print("self.data:\n", data, "\n\n")

        result = []
        for line in data:

            if (line.strip(" ") == ""):
                continue
            elif (not line.isupper()):
                result.append(line.strip(" "))
            else:
                return result

        return result

    def __processPoints(self, points):

        qtd_points = len(points)
        #print("qtd_points:", qtd_points)
        distancia = []
        for point in points:
            point = point.split("   ")
            distancia.append(point)

        return distancia

    def get_name(self):
        return self.NAME

    def get_dimension(self):
        return self.DIMENSION

    def get_capacity(self):
        return self.CAPACITY

    def get_demandSection(self):
        return self.DEMAND_SECTION

    def get_edgeWeightSection(self):
        return self.EDGE_WEIGHT_SECTION

    def get_best_solution(self):
        return self.best_solution
