import math

def run_majority_cascade(G, seed_set):
    """
    Modello Majority Cascade.
    Un nodo si attiva se almeno ceil(d(v)/2) vicini sono attivi.
    L'ho leggermente modificato perchè la rete è di 10k nodi.
    """
    active_nodes = set(seed_set)
    newly_activated = list(seed_set)
    
    # Pre-calcolo delle soglie di attivazione per ogni nodo
    thresholds = {u: math.ceil(G.degree(u) / 2) for u in G.nodes()}
    
    # Contatore vicini attivi per ogni nodo
    active_neighbors_count = {u: 0 for u in G.nodes()}
    
    # Inizializza i contatori con i seed iniziali
    for s in seed_set:
        for neighbor in G.neighbors(s):
            active_neighbors_count[neighbor] += 1

    # Propagazione a ondate
    while newly_activated:
        next_wave = []
        for u in newly_activated:
            for v in G.neighbors(u):
                if v not in active_nodes:
                    # Se il nodo v raggiunge la soglia, si attiva
                    if active_neighbors_count[v] >= thresholds[v]:
                        active_nodes.add(v)
                        next_wave.append(v)
                        # Notifica i vicini dell'attivazione di v
                        for neighbor_of_v in G.neighbors(v):
                            active_neighbors_count[neighbor_of_v] += 1
        newly_activated = next_wave
        
    return active_nodes