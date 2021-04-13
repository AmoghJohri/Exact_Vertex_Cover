import shutil
import numpy             as np
import matplotlib.pyplot as plt 

from .node  import Node
from .graph import Graph

def draw_graph(G, cover = []):
    nodes = G.V()
    pos   = []
    edges = G.E()
    diff  = 360/len(nodes)
    for i in range(len(nodes)):
        x = np.cos(np.radians(i*diff))
        y = np.sin(np.radians(i*diff))
        pos.append((x, y))
        if nodes[i] in cover:
            plt.plot(x, y, 'bo', markersize=8, color='r')
        else:
            plt.plot(x, y, 'bo', markersize=8)
        plt.text(x + 0.03, y, nodes[i], fontsize=12)
    for each in edges:
        x_values = [pos[each[0]][0], pos[each[1]][0]]
        y_values = [pos[each[0]][1], pos[each[1]][1]]
        plt.plot(x_values, y_values, color='g')
    plt.show()

if __name__ == "__main__":
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n0.add_edge(n2)
    n1.add_edge(n4)
    n2.add_edge(n4)
    n3.add_edge(n4)
    G  = Graph([n0, n1, n2, n3, n4])
    draw_graph(G)
    try:
        shutil.rmtree('__pycache__')
    except:
        pass
    