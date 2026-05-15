import random
import math

def get_random_cost(G, min_c=1, max_c=10, seed=42):
    """Costo random in un range fissato (Slide: c(u) valore random)."""
    random.seed(seed)
    return {u: random.randint(min_c, max_c) for u in G.nodes()}

def get_degree_cost(G):
    """Costo basato sul grado (Slide: c(u) = ceil(d(u)/2))."""
    return {u: math.ceil(G.degree(u) / 2) for u in G.nodes()}

def get_unit_cost(G):
    """Per ora scelta mia: gCosto unitario (tutti i nodi costano 1). Utile per baseline."""
    return {u: 1 for u in G.nodes()}