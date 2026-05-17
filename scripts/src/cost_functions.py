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

def get_sublinear_degree_cost(G):
    """
    Sublinear Degree Cost:
    c(u) = 1 + ceil(log2(1 + d(u)))

    Praticamente mi penalizza i nodi ad alto grado, ma in modo più leggero rispetto
    alla Degree Cost classica della prof
    """
    return {
        node: 1 + math.ceil(math.log2(1 + G.degree(node)))
        for node in G.nodes()
    }