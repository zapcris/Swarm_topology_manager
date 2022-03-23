import sys

import networkx as nx
from matplotlib import pyplot as plt
from shapely.geometry import MultiLineString, LineString
from itertools import combinations

multiline = MultiLineString([[(614633.1598889811, 6614684.232110311), (614585.0239559432, 6615176.69973293),
                              (614244.3696605981, 6615210.024609649), (614174.0171430812, 6615058.211282375)],
                             [(614849.2836035677, 6614574.273030049), (615163.3363697577, 6614591.624011607),
                              (615477.7302093033, 6614608.993836996), (615475.8039105758, 6614892.159749944),
                              (615474.6318041045, 6615064.459401229), (614967.3343471865, 6615119.389699113)],
                             [(615054.1363645532, 6614185.399992246), (615163.3363697577, 6614591.624011607),
                              (615227.7403992868, 6614831.207001455), (615475.8039105758, 6614892.159749944),
                              (615835.3545208545, 6614980.506471327), (615867.958614701, 6615021.869873968),
                              (615474.6318041045, 6615064.459401229), (615474.2581286087, 6615119.389699113),
                              (615286.7657710963, 6615227.024200648)],
                             [(616057.5676853136, 6615001.338955494), (615867.958614701, 6615021.869873968),
                              (616067.9839273975, 6615275.633330373)]])

for line1, line2 in combinations([line for line in multiline], 2):
    if line1.intersects(line2):
        print(line1.intersection(line2))

line1 = LineString([(0, 0), (5, 5)])

line2 = LineString([(5, 0), (0, 5)])

line3 = LineString([(1, 0), (5, 4)])

line4 = LineString([(4, 0), (0, 4)])

# print(line1.intersection(line4))
if line1.intersects(line3):
    print("done")

"Testing the edges "

total_edges = MultiLineString([[(0, 0), (5, 5)],
                               [(5, 0), (0, 5)],
                               [(1, 0), (5, 4)],
                               [(4, 0), (0, 4)],
                               ])
count = 0
for line1, line2 in combinations([line for line in total_edges], 2):

    if line1.crosses(line2):
        print(line1.intersection(line2))
        count += 1

print(count)
def find_graph_crossing(Batch, pos):
    G_pos = {1: (9, 4), 2: (18, 13), 3: (22, 8), 4: (18, 10), 5: (13, 0), 6: (15, 4), 7: (24, 22), 8: (12, 6), 9: (10, 11),
         10: (14, 16), 11: (26, 15), 12: (30, 4), 13: (17, 17), 14: (0, 2), 15: (19, 24), 16: (22, 12), 17: (26, 20),
         19: (23, 33), 20: (27, 28)}

    Batch = [[1, 5, 9, 10, 2, 11, 13, 15, 7, 20],
         [1, 2, 7, 3, 5, 6, 8, 9, 13, 15, 19, 20],
         [1, 5, 8, 6, 3, 2, 4, 10, 15, 17, 20],
         [1, 8, 9, 10, 2, 11, 13, 15, 7, 20],
         [1, 4, 17, 3, 8, 9, 13, 15, 19, 20],
         [1, 6, 8, 6, 3, 12, 4, 10, 15, 17, 20],
         [1, 14, 8, 6, 13, 2, 4, 10, 15, 17, 20]]

    print(Batch[0])
    Batch_sequence = Batch

    edge_list = []
    edge_pos_list = []
    for i in range(len(Batch_sequence)):
        edges = []
        edges_pos = []
        for j in range(len(Batch_sequence[i]) - 1):
            edge = [Batch_sequence[i][j], Batch_sequence[i][j + 1]]
            edge_pos = [G_pos[Batch_sequence[i][j]], G_pos[Batch_sequence[i][j + 1]]]
            edges.append(edge)
            edges_pos.append(edge_pos)
        edge_list.append(edges)
        edge_pos_list.append(edges_pos)

    print(edge_list)
    print(edge_pos_list)


    multi_strng_list = []

    for pos_seq in edge_pos_list:
        e = MultiLineString(pos_seq)
        multi_strng_list.append(e)

    for i in multi_strng_list:
        print(i)


    c = 0
    for multi_strng in multi_strng_list:
        for line1, line2 in combinations([line for line in multi_strng], 2):
            if line1.crosses(line2):
                print(line1.intersection(line2))
                c += 1

    return c


sys.exit()
"Draw graph of the subject"

G = nx.MultiGraph()
G.add_nodes_from(Batch_sequence)
G.add_edges_from(edge_list)
plt.figure()
plt.title(f"The plot belongs to initial population {i + 1} ")
nx.draw(G, G_pos, with_labels=True)
plt.grid(True)
plt.pause(0.05)
plt.show()
