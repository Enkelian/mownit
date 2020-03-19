import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

# G = nx.DiGraph()
#
# G.add_edge(1, 2, r=0.2, em=0)
# G.add_edge(1, 3, r=0.1, em=0)
# G.add_edge(1, 4, r=0.7, em=0)
# G.add_edge(2, 3, r=0.3, em=0)
# G.add_edge(2, 4, r=0.3, em=0)
# G.add_edge(3, 4, r=0.3, em=0)
# G.add_edge(2, 3, r=0, em=1)


def readFromFile(filename):
    G = nx.Graph()
    with open(filename, mode='r') as graph_file:
        reader = csv.reader(graph_file, delimiter=',')
        for row in reader:
            if any(row):
                u, v = int(row[0]), int(row[1])
                G.add_edge(u, v, r=float(row[2]))
    graph_file.close()
    return G


def writeToFile(filename, G):
    with open(filename, mode='w+') as graph_file:
        writer = csv.writer(graph_file)
        for e in list(G.edges(data=True)):
            # print(e[2]['r'])
            writer.writerow([e[0],e[1],e[2]['r']])
    graph_file.close()


def toDiGraph(G):
    DG = nx.DiGraph()
    for e in list(G.edges(data=True)):
        if e[0] < e[1]:
            DG.add_edge(*e[:2], r=e[2]['r'], em=e[2]['em'])
        else:
            DG.add_edge(e[1], e[0], r=e[2]['r'], em=e[2]['em'])
    return DG


def drawNodes(G, pos):
    nx.draw_networkx_nodes(G, pos, node_size=150)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')


def drawred(G, pos):
    all_Is = []
    for (node1, node2, data) in G.edges(data=True):
        all_Is.append(data['I'])

    unique_Is = list(set(all_Is))

    for i in unique_Is:
        red_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if
                          edge_attr['I'] == i]
        width = i * len(G.nodes) / sum(all_Is)
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, width=width)

    rs = nx.get_edge_attributes(G, 'r')
    red_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if edge_attr['r'] != 0]
    corr_rs = dict(filter(lambda elem: elem[1] != 0, rs.items()))

    nx.draw_networkx_edge_labels(red_edges, pos, edge_labels=corr_rs)


def drawEm(G, pos):
    all_ems = []
    for (node1, node2, data) in G.edges(data=True):
        all_ems.append(G[node1][node2]['em'])

    unique_ems = list(set(all_ems))

    for em in unique_ems:
        em_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if
                    edge_attr['em'] == em and edge_attr['em'] != 0]
        nx.draw_networkx_edges(G, pos, edgelist=em_edges, width=1, edge_color='red')


def drawEdges(G, pos):
    drawred(G, pos)
    drawEm(G, pos)


def drawGraph(G, I):
    I_vals = []
    nx.set_edge_attributes(G, I_vals, 'I')
    i = 0
    for e in list(G.edges()):
        G[e[0]][e[1]]['I'] = I[i]
        i += 1
    repairFlow(G)
    pos = nx.spring_layout(G)
    drawNodes(G, pos)
    drawEdges(G, pos)
    # nx.draw_networkx_edge_labels(G.edges(), pos, edge_labels=nx.get_edge_attributes(G, 'I'))
    plt.axis('off')
    plt.show()


def kirchoffI(G):
    e_count = len(G.edges)
    v_count = len(G.nodes)
    B = []
    A = np.zeros((v_count, e_count))
    row = 0
    for u in list(G.nodes):
        for v in list(nx.all_neighbors(G, u)):
            if u < v:
                e = (u, v)
                val = 1
            else:
                e = (v, u)
                val = -1
            A[row][list(G.edges).index(e)] = val
        row += 1
        B.append(0)

    return A, B


def kirchoffII(G, A, B):
    CG = nx.Graph()
    CG.add_edges_from(G.edges())
    cycles = nx.cycle_basis(CG)
    e_list = list(G.edges)
    for cycle in cycles:
        c_len = len(cycle)
        row = len(A)
        A = np.append(A, [np.zeros(len(G.edges))], axis=0)
        em_sum = 0
        for i in range(c_len):
            u = cycle[i]
            v = cycle[(i + 1) % c_len]
            if G.has_edge(u, v):
                A[row][e_list.index((u, v))] = -G[u][v]['r']
                em_sum += G[u][v]['em']
            else:
                A[row][e_list.index((v, u))] = G[v][u]['r']
                em_sum += G[v][u]['em']
        row += 1
        B.append(em_sum)
    return A, B


def repairFlow(G):
    E = []
    for e in G.edges(data=True):
        i = G[e[0]][e[1]]['I']
        if i < 0:
            E.append(e)

    for e in E:
        G.remove_edge(*e[:2])
        G.add_edge(e[1], e[0], r=e[2]['r'], em=e[2]['em'], I=-e[2]['I'])


def checkKirchoffI(G):
    eps = 1e-9
    for u in list(G.nodes()):
        sum = 0
        for v in list(G.neighbors(u)):
            sum += G[u][v]['I']
        for v in list(G.predecessors(u)):
            sum -= G[v][u]['I']
        if abs(sum) >= eps: return False
    return True


def checkKirchoffII(G):
    eps = 1e-7
    CG = nx.Graph()
    CG.add_edges_from(G.edges())
    cycles = nx.cycle_basis(CG)
    for cycle in cycles:
        c_len = len(cycle)
        v_sum = 0
        for i in range(c_len):
            u = cycle[i]
            v = cycle[(i + 1) % c_len]
            if G.has_edge(u, v):
                v_sum += G[u][v]['r'] * G[u][v]['I'] - G[u][v]['em']
            else:
                v_sum += - G[v][u]['r'] * G[v][u]['I'] + G[v][u]['em']
        # print(cycle)
        # print(v_sum)
        if abs(v_sum) >= eps: return False

    return True


def driver(G):
    A, B = kirchoffI(G)
    A, B = kirchoffII(G, A, B)
    print(A)
    print(B)
    I = np.linalg.lstsq(A, B, rcond=None)[0]
    drawGraph(G, I)
    print(checkKirchoffI(G))
    print(checkKirchoffII(G))


G1 = nx.generators.small.cubical_graph()
for e in G1.edges:
    G1[e[0]][e[1]]['r'] = np.random.randint(1, 10)
print(G1.edges(data=True))

writeToFile("graph2.csv", G1)
G2 = readFromFile("graph2.csv")
print(G2.edges(data=True))


#
# e1 = list(G1.edges)[0]
# G1[e1[0]][e1[1]]['r'] = 0
# G1[e1[0]][e1[1]]['em'] = np.random.randint(10, 100)
# # print(G1.edges(data=True))
#
# DG1 = toDiGraph(G1)
# driver(DG1)



#TODO: check signs