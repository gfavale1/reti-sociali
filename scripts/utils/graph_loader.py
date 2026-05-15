import networkx as nx
import os


def load_graph(file_path):
    """
    Carica il dataset SNAP e lo prepara per il Majority Cascade Model.

    Il dataset p2p-Gnutella04 è originariamente diretto, ma viene trattato
    come non orientato perché il modello Majority Cascade usato nelle slide
    è definito tramite vicinato N(v) e grado d(v).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Errore: file non trovato in {file_path}")

    G = nx.read_edgelist(
        file_path,
        create_using=nx.Graph(),
        nodetype=int,
        comments="#"
    )

    G.remove_edges_from(nx.selfloop_edges(G))

    print("--- Grafo caricato ---")
    print(f"Nodi: {G.number_of_nodes()}")
    print(f"Archi: {G.number_of_edges()}")

    return G