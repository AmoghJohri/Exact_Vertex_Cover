import random
import numpy             as np
import networkx          as nx
import matplotlib.pyplot as plt 

def getCustomGraph():
    G = nx.Graph()
    G.add_nodes_from(range(0, 15))
    G.add_edges_from([(0, 1), (0, 9), (0, 12), (0, 13)])
    G.add_edges_from([(1, 10), (1, 14)])
    G.add_edges_from([(2, 6), (2, 10)])
    G.add_edges_from([(4, 5), (4, 7), (4, 14)])
    G.add_edges_from([(5, 11)])
    G.add_edges_from([(6, 8)])
    G.add_edges_from([(7, 9), (7, 11), (7, 13), (7, 14)])
    G.add_edges_from([(8, 10)])
    G.add_edges_from([(9, 12)])
    G.add_edges_from([(11, 13)])
    G.add_edges_from([(12, 13)])
    return G 

def generateRandomGraph(n, p):
    G = nx.Graph()
    G.add_nodes_from(range(0, n))
    for i in G.nodes:
        for j in G.nodes:
            if i != j:
                if random.random() < p:
                    G.add_edge(i, j)
    return G

def drawGraph(G):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def drawCustomGraph(G, cover = []):
    nodes = list(G.nodes)
    pos   = []
    edges = list(G.edges)
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

def test(G, cover):
    G_copy = G.copy()
    for each in cover:
        try:
            G.remove_node(each)
        except:
            print("Cover: ", cover)
            drawGraph(G_copy)
    if len(list(G.edges)) != 0:
        drawCustomGraph(G_copy, cover)
        print("Test-case failed!")