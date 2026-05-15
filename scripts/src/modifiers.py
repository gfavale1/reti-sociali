import random


def remove_x_edges(G, x, seed=42):
    """
    Rimuove x archi casuali dal grafo, producendo G'.
    """
    G_prime = G.copy()
    rng = random.Random(seed)

    edges = list(G_prime.edges())

    if x > len(edges):
        x = len(edges)

    edges_to_remove = rng.sample(edges, x)
    G_prime.remove_edges_from(edges_to_remove)

    return G_prime


def remove_y_nodes(G, y, seed=42):
    """
    Rimuove y nodi casuali dal grafo, insieme ai relativi archi, producendo G'.
    """
    G_prime = G.copy()
    rng = random.Random(seed)

    nodes = list(G_prime.nodes())

    if y > len(nodes):
        y = len(nodes)

    nodes_to_remove = rng.sample(nodes, y)
    G_prime.remove_nodes_from(nodes_to_remove)

    return G_prime