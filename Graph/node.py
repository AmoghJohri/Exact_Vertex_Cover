class Node:
    def __init__(self, value = 0):
        self.value    = value
        self.edgeList = []
    
    def set_edge_list(self, eList):
        self.edgeList = eList 

    def get_degree(self):
        return len(self.edgeList)

    def add_edge(self, vertex):
        if vertex.value not in [each.value for each in self.edgeList]:
            self.edgeList.append(vertex)
            vertex.edgeList.append(self)
            return 0
        return 1
    
    def remove_edge(self, vertex):
        for each in self.edgeList:
            if each.value == vertex.value:
                self.edgeList.remove(each)
                each.edgeList.remove(self)
                return 0
        return 1