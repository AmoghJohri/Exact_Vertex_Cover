from copy import deepcopy
from .node import Node 

class Graph:
    def __init__(self, nodes = [], edges = {}):
        self.nodes = nodes 
        self.edges = edges 
        for each in self.nodes:
            edges[each] = each.edgeList

    def get_edge_list(self):
        out = []
        for each in self.edges.keys():
            for _ in self.edges[each]:
                out.append((each, _))
        return out 

    def get_node_by_value(self, value):
        for each in self.nodes:
            if each.value == value:
                return each 
    
    def N(self):
        return len(self.nodes)
    
    def M(self):
        out = 0
        for each in self.edges.keys():
            out += len(self.edges[each])
        return out/2

    def add_node(self, node):
        if node.value not in [each.value for each in self.nodes]:
            self.nodes.append(node)
            self.edges[node] = []
        
    def remove_node(self, node):
        for each in self.nodes:
            if each.value == node.value:
                self.nodes.remove(each)
                _nodes = self.edges[each]
                while len(_nodes) > 0:
                    _nodes[0].remove_edge(each)
                del self.edges[each]

    def add_edge(self, edge):
        for each in self.nodes:
            if each.value == edge[0].value:
                r = each.add_edge(edge[1])
                if r == 0:
                    self.edges[each].append(edge[1])
            elif each.value == edge[1].value:
                r = each.add_edge(edge[0])
                if r == 0:
                    self.edges[each].append(edge[0])

    def remove_edge(self, edge):
        for each in self.nodes:
            if each.value == edge[0].value:
                r = each.remove_edge(edge[1])
                if r == 0:
                    self.edges[each].remove(edge[1])
            elif each.value == edge[1].value:
                r = each.remove_edge(edge[0])
                if r == 0:
                    self.edges[each].remove(edge[0])

    def V(self):
        return [each.value for each in self.nodes]
    
    def E(self):
        edges = []
        for each in self.nodes:
            for key in each.edgeList:
                edges.append((each.value, key.value))
        return edges 
