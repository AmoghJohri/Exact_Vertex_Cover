import os 
import statistics
import networkx as nx 
import progressbar

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
    p_arr = []
    bar = progressbar.ProgressBar(maxval=201, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in range(1, 200, 2):
        G = get_graph(code=i)
        v = len(list(G.nodes))
        e = len(list(G.edges))
        p_arr.append(e/(v*v/2))
        bar.update(i+2)
    bar.finish()
    print("Min: ", min(p_arr))
    print("Max: ", max(p_arr))
    print("Mean: ", statistics.mean(p_arr))
    print("Median: ", statistics.median(p_arr))

"""
Min   :  2.381614667858874e-05
Max   :  0.17610864197530865
Mean  :  0.01887090304564615
Median:  0.00023000940504558766
"""