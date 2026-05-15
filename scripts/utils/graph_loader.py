import networkx as nx
import os

def load_gnutella_graph(file_path):
    """
    Carica il dataset e lo prepara per l'analisi.
    - Converte in grafo NON orientato (come richiesto dal modello Majority).
    - Rimuove self-loops (archi che tornano sullo stesso nodo).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Errore: File non trovato in {file_path}")

    # Caricamento come grafo non orientato (lo converto per via delle formule -- lo spiego nella relazione per bene)
    G = nx.read_edgelist(file_path, create_using=nx.Graph(), nodetype=int)
    
    # Pulizia: rimuove eventuali archi che collegano un nodo a se stesso
    # Non dovrebbero essercene ma ho avuto risultati discordanti all'inizio
    G.remove_edges_from(nx.selfloop_edges(G))
    
    print(f"--- Grafo Caricato ---")
    print(f"Nodi: {G.number_of_nodes()}")
    print(f"Archi: {G.number_of_edges()}")
    return G