import os 
import networkx as nx 

from util import drawGraph

def get_graph(code=5):
    if code < 10:
        code = "00" + str(code)
    elif code < 100:
        code = "0" + str(code)
    else:
        code = str(code)
    file_name = os.getcwd() + "/public/" + "vc-exact_" + code + ".gr"
    f = open(file_name, 'r')
    i = 0
    G = nx.Graph()
    for line in f:
        if i == 0:
            var = line.split()
            vertices = int(var[-2])
            edges = int(var[-1])
        else:
            var = line.split()
            n1 = int(var[0])
            n2 = int(var[1])
            G.add_edge(n1,n2)
        i = i + 1
    return G

if __name__ == "__main__":
    G = get_graph()
    print("|V|: ", len(G.nodes))
    print("|E|: ", len(G.edges))