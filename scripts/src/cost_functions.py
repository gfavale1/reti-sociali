import random
import math


def get_random_cost(G, min_c=1, max_c=10, seed=42):
    """
    Funzione costo random.

    Nelle slide la prof l'ha descritta come: c(u) = valore random scelto in un range fissato.
    """
    rng = random.Random(seed)

    return {
        u: rng.randint(min_c, max_c)
        for u in G.nodes()
    }


def get_degree_cost(G):
    """
    Funzione costo basata sul grado.

    Nelle slide la prof l'ha descritta come: c(u) = ceil(d(u) / 2).
    """
    return {
        u: math.ceil(G.degree(u) / 2)
        for u in G.nodes()
    }