import random

def remove_x_edges(G, x):
    """Rimuove x archi casuali dal grafo (G')."""
    G_prime = G.copy()
    edges = list(G_prime.edges())
    if x > len(edges): x = len(edges)
    
    edges_to_remove = random.sample(edges, x)
    G_prime.remove_edges_from(edges_to_remove)
    return G_prime

def remove_y_nodes(G, y):
    """Rimuove y nodi casuali e i relativi archi (G')."""
    G_prime = G.copy()
    nodes = list(G_prime.nodes())
    if y > len(nodes): y = len(nodes)
    
    nodes_to_remove = random.sample(nodes, y)
    G_prime.remove_nodes_from(nodes_to_remove)
    return G_prime