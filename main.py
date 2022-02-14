import itertools
import math
from dataclasses import dataclass

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
# from .utils import Get_Distance_Or_Flow
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_array
from itertools import groupby
from collections import Counter
from networkx.algorithms import approximation
import sys
import xlrd
from tkinter import *
from tkinter.filedialog import askopenfile
from openpyxl import load_workbook

from UI import open_file
from batch_topology import create_batch_topology
from variant_topology import config, topology, workstation

random.seed(1314141)

graph = [[1, 5, 9, 10, 2, 11, 13, 15, 7, 20],
         [1, 2, 7, 3, 5, 6, 8, 9, 13, 15, 19, 20],
         [1, 5, 8, 6, 3, 2, 4, 10, 15, 17, 20]]

graph2 = [[1, 8, 9, 10, 2, 11, 13, 15, 7, 20],
          [1, 4, 17, 3, 8, 9, 13, 15, 19, 20],
          [1, 6, 8, 6, 3, 12, 4, 10, 15, 17, 20],
          [1, 14, 8, 6, 13, 2, 4, 10, 15, 17, 20]]

batch_seq = [[1, 5, 9, 10, 2, 11, 13, 15, 7, 20],
             [1, 2, 7, 3, 5, 6, 8, 9, 13, 15, 19, 20],
             [1, 5, 8, 6, 3, 2, 4, 10, 15, 17, 20],
             [1, 8, 9, 10, 2, 11, 13, 15, 7, 20],
             [1, 4, 17, 3, 8, 9, 13, 15, 19, 20],
             [1, 6, 8, 6, 3, 12, 4, 10, 15, 17, 20],
             [1, 14, 8, 6, 13, 2, 4, 10, 15, 17, 20]]

batch_list = [batch_seq]
full_ws = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


# for gr in batch_list:
#     num = 0
#     top = create_graph(batch_seq, num + 1, 2.2)
#     print(top)


@dataclass
class chromosome:
    k_val: float
    iter_nr: int
    sequence: list


chrm = chromosome
init_population = []
start_k = 1.2
stop_k = 2.0
step_k = 0.2

## Calculate 2 sets of population with different iteration value 25 and 35#####

for i in range(int(start_k * 10), int(stop_k * 10), int(step_k * 10)):
    chrm = chromosome(i / 10, 10, batch_seq)
    init_population.append(chrm)
    # print(i / 10)

for i in range(int(start_k * 10), int(stop_k * 10), int(step_k * 10)):
    chrm = chromosome(i / 10, 15, batch_seq)
    init_population.append(chrm)

# for p in population:
#     print(p)


fitness_list = []
topology_htable = dict()
for i in range(len(init_population)):
    btop = create_batch_topology(init_population[i].sequence, i + 1, init_population[i].k_val,
                                 init_population[i].iter_nr)
    fitness_list.append(btop[0])
    topology_htable.update({btop[0]: btop[1]})
    # print(btop)

print("Fitness list:", fitness_list)

# for key, value in topology_htable.items():
#     print(key, value)


########choosing the parents ####################
middle_index = round(len(init_population) / 2)

sorted_fitness1 = fitness_list[:middle_index]
sorted_fitness2 = fitness_list[middle_index:]

print(sorted_fitness1.index(sorted(sorted_fitness1)[0]))
print(sorted_fitness2.index(sorted(sorted_fitness2)[0]))

parent_1 = init_population[sorted_fitness1.index(sorted(sorted_fitness1)[0])]
parent_2 = init_population[sorted_fitness2.index(sorted(sorted_fitness2)[0]) + middle_index]

print("Parent 1:", parent_1)
print("Parent 2:,", parent_2)

####3 Crossover part of Genetic algorithm##################
off_population = []
offspring_fitness = []

offspring_1 = chromosome(parent_1.k_val, parent_2.iter_nr, parent_1.sequence)
off_population.append(offspring_1)

offspring_2 = chromosome(parent_2.k_val, parent_1.iter_nr, parent_2.sequence)
off_population.append(offspring_2)

for i in range(len(off_population)):
    off_top = create_batch_topology(off_population[i].sequence, i + 1, off_population[i].k_val,
                                    off_population[i].iter_nr)
    offspring_fitness.append(off_top[0])
    topology_htable.update({off_top[0]: off_top[1]})
    print("OFF spring topologies:", i + 1, off_top)

print(min(offspring_fitness))

for key, value in topology_htable.items():
    print(key, value)

### Mutation function to be decided later#####3#
mut_population = []
mut_fitness = []

###Recursive operation until desired fitness achieved#############
min_fitness = []


def GA_recursion(itr1, itr2, rec_nr):
    new_population = []
    fit_list = []
    off_populn = []
    offspr_fitness = []
    start_k = 1.3
    stop_k = 2.0
    step_k = (stop_k - start_k) / 0.25
    print(f'The recursion number is {rec_nr} with iteration pari {itr1} and {itr2}')
    # print("Cleared length of population:", len(new_population))
    for i in range(int(start_k * 10), int(stop_k * 10), int(step_k)):
        chrm1 = chromosome(i / 10, itr1, batch_seq)
        new_population.append(chrm1)
        # print(i / 10)

    for i in range(int(start_k * 10), int(stop_k * 10), int(step_k)):
        chrm2 = chromosome(i / 10, itr2, batch_seq)
        new_population.append(chrm2)

    for i in range(len(new_population)):
        top = create_batch_topology(new_population[i].sequence, i + 1, new_population[i].k_val,
                                    new_population[i].iter_nr)
        fit_list.append(top[0])
        topology_htable.update({top[0]: top[1]})

    print("The current population fitness list:", fit_list)

    m_index = round(len(new_population) / 2)

    sorted_fit1 = fit_list[:m_index]
    sorted_fit2 = fit_list[m_index:]

    p_1 = new_population[sorted_fit1.index(sorted(sorted_fit1)[0])]
    print("The index of 1st parent in fit list:", sorted_fit1.index(sorted(sorted_fit1)[0]))

    p_2 = new_population[sorted_fit2.index(sorted(sorted_fit2)[0]) + m_index]
    print("The index of 2nd parent in fit list:", sorted_fit2.index(sorted(sorted_fit2)[0]) + m_index)

    offspr_1 = chromosome(p_1.k_val, p_2.iter_nr, p_1.sequence)
    off_populn.append(offspr_1)
    offspr_2 = chromosome(p_2.k_val, p_1.iter_nr, p_2.sequence)
    off_populn.append(offspr_2)

    print("offspring 1 chromosome:", offspr_1)
    print("offspring 2 chromosome:", offspr_2)

    for i in range(len(off_populn)):
        otop = create_batch_topology(off_population[i].sequence, i + 1, off_population[i].k_val,
                                     off_population[i].iter_nr)
        offspr_fitness.append(otop[0])
        topology_htable.update({otop[0]: otop[1]})
        # print("OFF spring topologies:", i + 1, otop)

    print("fitness list of offspring in this iteration:", offspr_fitness)
    print("minimum fitnesss value in this iteration:", min(offspr_fitness))

    if min(fit_list) < min(offspr_fitness):
        gen_min_fitness = min(fit_list)
    else:
        gen_min_fitness = min(offspr_fitness)
    print("minimumfitness value in this generation:", gen_min_fitness)

    # rint(int(step_k))
    # print(result)

    if min(offspr_fitness) > 500 and itr1 != 40 and itr2 != 45:
        min_fitness.append(gen_min_fitness)
        # new_population.clear()
        # fit_list.clear()
        # off_populn.clear()
        # offspr_fitness.clear()
        # del p_1
        # del p_2
        # del offspr_1
        # del offspr_2

        GA_recursion(itr1 + 5, itr2 + 5, rec_nr + 1)
        result = min(min_fitness)

    elif min(offspr_fitness) <= 500:
        result = min(offspr_fitness)

    else:
        result = 0

    return result


##### END of GA ######
if min(offspring_fitness) > 500:
    print("\n\nRecursion Started")
    final_fitness = (GA_recursion(20, 25, 1))
    print("the min fitness list:", min_fitness)
    print("The least possible fitness value:", final_fitness)
    print("The topology of the fittest value:", topology_htable[final_fitness])

elif min(offspring_fitness) <= 500:
    print("Fitness value found below 500:", min(offspring_fitness))

### END OF GENETIC ALGORITHM########


### Visualising grid######3
root = Tk()
root.geometry('200x100')
btn = Button(root, text ='Open', command = open_file)
btn.pack(side='top')



mainloop()

sys.exit()


def unique_values_in_list_of_lists(lst):
    result = set(x for l in lst for x in l)
    return list(result)


P_variant = [[0, 1, 5, 9, 10, 2, 11, 13, 15, 7, 20],
             [0, 1, 2, 3, 5, 6, 8, 9, 13, 15, 19, 20],
             [0, 1, 5, 8, 6, 3, 2, 4, 10, 15, 17, 20]]

# print(unique_values_in_list_of_lists(P_variant))

n = len(unique_values_in_list_of_lists(P_variant))  # max length of the topology

G = nx.DiGraph()

# def cost_flow(graph):
#    for l in lst:
#       for x in l:

#   return 0


node_list = unique_values_in_list_of_lists(graph)
edge_list = []
conn_list = []

print("list of nodes:", node_list)
print("number of workstation nodes:", len(node_list))

### Create list of edges in the topology
for i in range(len(graph)):
    for j in range(len(graph[i]) - 1):
        # print(graph[i][j], graph[i][j+1])
        edge = [graph[i][j], graph[i][j + 1]]
        edge_list.append(edge)

print("edge list:", edge_list)
# for i in range(len(edge_list)):
#     for j in range(len(edge_list[i])):
#         print("THe edge list starts here:", edge_list[i][j])

## convert to adjacency list
adj = {k: [v[1] for v in g] for k, g in groupby(sorted(edge_list), lambda e: e[0])}
# adj: {1: [2, 3], 2: [3]}

# an_iterator = itertools.groupby(sorted(edge_list), lambda x : x[0])
# for key, group in an_iterator:
#     key_and_group = {key : list(group)}
#     print(key_and_group)

print("adjacency list dictionary:", adj)
BDS_graph = [[] for i in range(max(node_list))]
BDS_list = []


#### Function to convert nestedlist into Flat list########
def flattenNestedList(nestedList):
    ''' Converts a nested list to a flat list '''
    flatList = []
    # Iterate over all the elements in given list
    for elem in nestedList:
        # Check if type of element is list
        if isinstance(elem, list):
            # Extend the flat list by adding contents of this element (list)
            flatList.extend(flattenNestedList(elem))
        else:
            # Append the element to the list
            flatList.append(elem)
    return flatList


#### remove repeating values in the list for node keys##############
for key, value in adj.items():
    edg_lst = []
    flatList = []
    newlist = list(dict.fromkeys(value))
    conn_list.append(newlist)
    for i in range(len(newlist)):
        edg_lst.append(newlist[i])
    L = [key, edg_lst]
    flatList = flattenNestedList(L)
    # print(flatList)
    BDS_list.append(flatList)

print("BDS list:", BDS_list)

for i in range(1, len(BDS_graph)):
    for key, value in adj.items():
        if i == key:
            BDS_graph[i] = list(dict.fromkeys(value))

print("BDS graph for level:", BDS_graph)
print("Values from adjacency dict:", conn_list)
#### convert edge list to adjacency matrix#######3
# G = nx.Graph(edge_list)
# A = nx.to_scipy_sparse_matrix(G)
# print(A.todense())
adjacency_list = []
G = nx.MultiGraph()  # Multigraph - Undirected with self loops####
G.add_nodes_from(node_list)
G.add_edges_from(edge_list)
width_dict = Counter(G.edges())
edge_width = [[u, v, {'frequency': value}]
              for ((u, v), value) in width_dict.items()]

print("edge congestion:", edge_width)
# print("cluster triangles", nx.triangles(G))
print("average clustering:", approximation.average_clustering(G))

H = nx.Graph()
H.add_nodes_from(node_list)
H.add_edges_from(edge_list)

print(approximation.treewidth_min_degree(H))
print(approximation.treewidth_min_fill_in(H))

# print("The graph is a tree:'",nx.is_forest(G))


# printLevels(BDS_graph, 20, 0)


### PLOT the graph###3
M = nx.Graph()
M.add_edges_from(edge_width)
initialpos = {1: [0, 0], 20: [2, 2]}
pos = nx.spring_layout(G, weight='myweight', pos=initialpos, k=0.5, dim=2, scale=1, seed=10, iterations=20)
nx.draw_networkx(G, pos)

for key, value in pos.items():
    print(value)

min_x, min_y = 0, 0
for key, value in pos.items():
    if value[0] < min_x:
        min_x = value[0]
    if value[1] < min_y:
        min_y = value[1]

print(f"min x {min_x} min y {min_y}")

scale = 50
new_pos = []
for key, value in pos.items():
    new_pos.append((key, (scale * (value[0] + abs(min_x)), scale * (value[1] + abs(min_y)))))

# pos = dict(new_pos)
# print(dict(new_pos))

pos = dict(new_pos)

pos2 = nx.rescale_layout_dict(pos, 2)
print("old pos:", pos)
print("new pos:", pos2)
val = []
for key, value in pos.items():
    val.append(list(dict.fromkeys(value)))

# print(val)

##Interpolation to grid is required#######3


plt.xlabel('Columns')
plt.ylabel('Rows')
plt.title('Swarm topology')
plt.grid(True)
plt.savefig('plot of topology')
# not_in_list = 1 not in node_list


### Initialize product specific topologies#################

pos_list = [[0, 0] for i in range(max(node_list) + 1)]
config_list = []

product_topologies = []
all_workstations = []
batch_topologies = []
new_list = []

for i in range(len(pos_list)):
    for key, value in pos.items():
        if i == key:
            pos_list[i] = list(dict.fromkeys(value))

print("position list", pos_list)
print(len(pos_list))

for i in range(len(graph)):
    ws = []
    for j in range(len(graph[i])):
        ws.append(workstation(num=graph[i][j], active=True))
    all_workstations.append(ws)

# Configuration data for topologies is created here
# for i in range(len(graph)):
#     cs = []
#     ds = []
#     for j in range(len(graph[i])):
#         cs.append(config(random.randint(0, 9), random.randint(0, 9)))
#
#         ds.append(config(0, 0))
#     config_list.append(cs)
#     new_list.append(ds)
#
# print("config list:", config_list)

sorted_configs = []
for graph_taken in graph:
    # [1 5 4 2 3]
    this_graph_config = []
    for node in graph_taken:
        print(f"Node {node}")
        print(f"Value= {pos_list[node]}")
        this_graph_config.append(config(pos_list[node][0], pos_list[node][0]))
    sorted_configs.append(this_graph_config)

print(all_workstations)
print(len(all_workstations))

print("Sorted list:", sorted_configs)

for num in range(len(all_workstations)):
    product_topologies.append(topology(all_workstations[num], sorted_configs[num], num + 1))

for top in product_topologies:
    top.display()
    print("distance travelled:", top.calculate_distance())
    print("Fitness value:", top.fitness_calc())

sys.exit()
