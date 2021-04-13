import time
import random 
import matplotlib.pyplot as plt 
from   copy           import deepcopy 

from   make_test_case import get_test_case 
from   brute_force    import brute_force 
from   kernel_A       import kernelization 
from   Graph.util     import draw_graph
from   Graph.node     import Node 
from   Graph.graph    import Graph 


if __name__ == "__main__":
    test_cases = 10
    redundancy = 10
    passed = 0
    enablePrint = False
    time_brute_force = []
    time_kernel_A = []
    for i in range(test_cases):
        for j in range(redundancy):
            test_graph_size   = i
            vertex_cover_size = random.randint(int(i/2), i)
            G                 = get_test_case(test_graph_size)
            G_brute_force     = deepcopy(G)
            G_kernel          = deepcopy(G) 
            start = time.time()
            vertex_cover_bf   = brute_force(G_brute_force, vertex_cover_size)
            end = time.time() - start
            brute_force_time = end 
            start = time.time()
            vertex_cover_kA   = kernelization(G_kernel, vertex_cover_size)
            end = time.time() - start 
            kernel_A_time = end 
            try:
                time_brute_force[i] += (brute_force_time)
            except:
                time_brute_force.append(brute_force_time)
            try:
                time_kernel_A[i] += (kernel_A_time)
            except:
                time_kernel_A.append(kernel_A_time)
            if vertex_cover_bf and (len(vertex_cover_bf[0]) > vertex_cover_size) and vertex_cover_kA:
                print("Something Went Wrong")
                print("Graph Nodes: ", G.V())
                print("Graph Edges: ", G.E())
                print("vertex_cover_size: ", vertex_cover_size)
                print("vertex_cover_bf: ", vertex_cover_bf)
                print("vertex_cover_kA: ", vertex_cover_kA)
                draw_graph(G)
                continue
            if enablePrint:
                print("Test Graph Size: ", test_graph_size)
                print("Vertex Cover Size: ", vertex_cover_size)
                print("Optimal Vertex Cover Size: ", len(vertex_cover_bf[0]))
                print("Time Taken By Brute Force: ", brute_force_time)
                print("Time Taken By Kernel_A: ", kernel_A_time)
            passed = passed + 1
    print("Accuracy: ", (passed/(test_cases*redundancy))*100, "%")
    plt.plot([i for i in range(test_cases)], time_brute_force)
    plt.plot([i for i in range(test_cases)], time_kernel_A)
    plt.legend(['Brute Force', 'Kernel-A'])
    plt.grid()
    plt.show()

    