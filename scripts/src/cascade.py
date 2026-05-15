import math


def run_majority_cascade(G, seed_set):
    """
    Simula il Majority Cascade Model.

    Dato un seed set S, la cascata evolve secondo la regola:

    un nodo v si attiva se almeno ceil(d(v) / 2) dei suoi vicini
    sono già attivi. i nodi attivati in uno step influenzano
    gli altri solo dallo step successivo.
    """

    active_nodes = set(seed_set) & set(G.nodes())

    thresholds = {
        v: math.ceil(G.degree(v) / 2)
        for v in G.nodes()
    }

    while True:
        next_active = set()

        for v in G.nodes():
            if v in active_nodes:
                continue

            active_neighbors = sum(
                1 for u in G.neighbors(v)
                if u in active_nodes
            )

            if active_neighbors >= thresholds[v]:
                next_active.add(v)

        if not next_active:
            break

        active_nodes.update(next_active)

    return active_nodes