import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
from decimal import Decimal


def read_from_file(filename):
    G = nx.DiGraph()
    with open(filename, mode='r') as graph_file:
        reader = csv.reader(graph_file, delimiter=',')
        for row in reader:
            if any(row):
                u, v = int(row[0]), int(row[1])
                if u < v:
                    G.add_edge(u, v, r=float(row[2]))
                else:
                    G.add_edge(v, u, r=float(row[2]))

    graph_file.close()
    return G


def write_to_file(filename, G):
    with open(filename, mode='w+') as graph_file:
        writer = csv.writer(graph_file)
        for e in list(G.edges(data=True)):
            writer.writerow([e[0], e[1], e[2]['r']])
    graph_file.close()


def to_digraph(G):
    DG = nx.DiGraph()
    for e in list(G.edges(data=True)):
        if e[0] < e[1]:
            DG.add_edge(*e[:2], r=e[2]['r'], em=e[2]['em'])
        else:
            DG.add_edge(e[1], e[0], r=e[2]['r'], em=e[2]['em'])
    return DG


def draw_nodes(G, pos):
    nx.draw_networkx_nodes(G, pos, node_size=160, node_color='orange')
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')


def draw_edges(G, pos):
    all_rs = []
    for (node1, node2, data) in G.edges(data=True):
        all_rs.append(data['r'])

    unique_rs = list(set(all_rs))

    for i in unique_rs:
        red_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if
                     edge_attr['r'] == i and edge_attr['em'] != 0]
        rest = [(node1, node2) for (node1, node2, edge_attr) in G.edges(data=True) if
                edge_attr['r'] == i and edge_attr['em'] == 0]
        width = i * len(G.nodes) / sum(all_rs)
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, width=1, edge_color='red')
        nx.draw_networkx_edges(G, pos, edgelist=rest, width=width)

    Is = nx.get_edge_attributes(G, 'I')
    Is = {k: round(Decimal(v), 2) for k, v in Is.items()}
    nx.draw_networkx_edge_labels(G.edges(), pos, font_size=7, edge_labels=Is)


def draw_graph(G, pos):
    plt.figure(1, figsize=(8, 6))
    draw_nodes(G, pos)
    draw_edges(G, pos)
    plt.axis('off')
    plt.show()


def add_Is(G, I):
    I_vals = []
    nx.set_edge_attributes(G, I_vals, 'I')
    i = 0
    for e in list(G.edges()):
        G[e[0]][e[1]]['I'] = I[i]
        i += 1
    repair_flow(G)


def kirchoff_i(G):
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


def kirchoff_ii(G, A, B):
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


def repair_flow(G):
    E = []
    for e in G.edges(data=True):
        i = G[e[0]][e[1]]['I']
        if i < 0:
            E.append(e)

    for e in E:
        G.remove_edge(*e[:2])
        G.add_edge(e[1], e[0], r=e[2]['r'], em=e[2]['em'], I=-e[2]['I'])


def checkkirchoff_i(G):
    eps = 1e-9
    for u in list(G.nodes()):
        sum = 0
        for v in list(G.neighbors(u)):
            sum += G[u][v]['I']
        for v in list(G.predecessors(u)):
            sum -= G[v][u]['I']
        if abs(sum) >= eps: return False
    return True


def checkkirchoff_ii(G):
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
        if abs(v_sum) >= eps: return False
    return True


def is_connected(G):
    if nx.number_connected_components(G) == 1: return True
    return False


def solve_Is(G):
    A, B = kirchoff_i(G)
    A, B = kirchoff_ii(G, A, B)
    I = np.linalg.lstsq(A, B, rcond=None)[0]
    add_Is(G, I)
    if not checkkirchoff_i(G):
        print("Graph does not satisfy I Kirchoff's law")
        return
    if not checkkirchoff_ii(G):
        print("Graph does not satisfy II Kirchoff's law")
        return


def driver(G):
    if not is_connected(G):
        print("Graph is not connected")
        return
    if type(G) != nx.DiGraph:
        G = to_digraph(G)
    solve_Is(G)
    pos = nx.kamada_kawai_layout(G)
    draw_graph(G, pos)


def fill_random(G1):
    for e in G1.edges:
        G1[e[0]][e[1]]['r'] = np.random.randint(1, 10)
        G1[e[0]][e[1]]['em'] = 0


def fill_1(G1):
    for e in G1.edges:
        G1[e[0]][e[1]]['r'] = 1
        G1[e[0]][e[1]]['em'] = 0


def randomConnected():
    G1 = nx.generators.random_graphs.gnp_random_graph(30, 0.1)
    while not is_connected(G1):
        G1 = nx.generators.random_graphs.gnp_random_graph(30, 0.1)
    fill_random(G1)
    e1 = list(G1.edges)[0]
    G1[e1[0]][e1[1]]['r'] = 0
    G1[e1[0]][e1[1]]['em'] = np.random.randint(10, 100)
    driver(G1)


def cubic(rand):
    G1 = nx.generators.small.cubical_graph()
    if rand: fill_random(G1)
    else: fill_1(G1)
    e1 = list(G1.edges)[1]
    G1[e1[0]][e1[1]]['r'] = 0
    G1[e1[0]][e1[1]]['em'] = np.random.randint(10, 100)
    driver(G1)


def cubic2(u, v, rand):  # with electromotive force between u and v
    G1 = nx.generators.small.cubical_graph()
    if rand:
        fill_random(G1)
    else:
        fill_1(G1)
    G1.add_edge(u, v, r=0, em=np.random.randint(1, 20))
    driver(G1)


def bridge():
    n = 15
    p = 0.1
    G1 = nx.generators.random_graphs.gnp_random_graph(n, p)
    while not is_connected(G1):
        G1 = nx.generators.random_graphs.gnp_random_graph(n, p)

    G2 = nx.generators.random_graphs.gnp_random_graph(n, p)
    while not is_connected(G2):
        G2 = nx.generators.random_graphs.gnp_random_graph(n, p)

    G2 = nx.relabel_nodes(G2, lambda v: v + n)

    G1.add_edges_from(G2.edges())
    u, v = np.random.randint(0, n - 1), np.random.randint(n, 2 * n - 1)
    print(u, v)
    G1.add_edge(u, v)
    u, v = np.random.randint(0, n - 1), np.random.randint(n, 2 * n - 1)
    print(u, v)
    G1.add_edge(u, v)
    fill_random(G1)
    u, v = np.random.randint(0, n - 1), np.random.randint(0, n - 1)
    print(u, v)
    G1.add_edge(u, v, r=0, em=np.random.randint(10, 100))
    driver(G1)


def grid_2d(n, m):
    G1 = nx.generators.lattice.grid_2d_graph(n, m)
    fill_random(G1)
    e1 = list(G1.edges)[0]
    G1[e1[0]][e1[1]]['r'] = 0
    G1[e1[0]][e1[1]]['em'] = np.random.randint(10, 100)
    driver(G1)


def grid_2d(n, m, u, v, rand):
    G1 = nx.generators.lattice.grid_2d_graph(n, m)
    if rand:
        fill_random(G1)
    else:
        fill_1(G1)
    e1 = list(G1.edges)[0]
    G1.add_edge(u, v, r=0, em=np.random.randint(50, 100))
    driver(G1)


def given_graph(filename, em_edge):
    G = read_from_file(filename)
    G.add_edge(em_edge[0], em_edge[1], em=em_edge[3], r=0)
    driver(G)


def random_connected2(n, u, v):
    G1 = nx.generators.random_graphs.gnp_random_graph(n, 0.1)
    while not is_connected(G1):
        G1 = nx.generators.random_graphs.gnp_random_graph(n, 0.1)
    fill_random(G1)
    # e1 = list(G1.edges)[0]
    G1.add_edge(u, v)
    G1[u][v]['r'] = 0
    G1[u][v]['em'] = np.random.randint(10, 100)
    driver(G1)


random_connected2(30, 5, 4)