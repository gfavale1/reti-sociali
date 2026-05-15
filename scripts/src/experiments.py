import time

from scripts.src.cascade import run_majority_cascade
from scripts.src.algorithms import algorithm_1_greedy, algorithm_2_wtss, total_cost
from scripts.src.modifiers import remove_x_edges, remove_y_nodes


def get_algorithms():
    """
    Restituisce gli algoritmi usati negli esperimenti.
    Per ora sono inclusi solo quelli esplicitamente richiesti dalle slide.
    """
    return {
        "Greedy f1": lambda G, k, costs: algorithm_1_greedy(G, k, costs, potential_type="f1"),
        "Greedy f2": lambda G, k, costs: algorithm_1_greedy(G, k, costs, potential_type="f2"),
        "Greedy f3": lambda G, k, costs: algorithm_1_greedy(G, k, costs, potential_type="f3"),
        "WTSS": lambda G, k, costs: algorithm_2_wtss(G, k, costs),
    }


def run_single_experiment(G, algorithm_name, algorithm_fn, costs, cost_function_name, budget_percentage, k):
    """
    Esegue un singolo esperimento:
    1. selezione del seed set S;
    2. simulazione Majority Cascade;
    3. calcolo delle metriche.
    """
    start_time = time.perf_counter()

    seed_set = algorithm_fn(G, k, costs)
    seed_set_cost = total_cost(seed_set, costs)

    activated_nodes = run_majority_cascade(G, seed_set)

    end_time = time.perf_counter()

    return {
        "cost_function": cost_function_name,
        "algorithm": algorithm_name,
        "budget_percentage": budget_percentage,
        "budget_k": k,
        "seed_set_size": len(seed_set),
        "seed_set_cost": seed_set_cost,
        "activated_nodes": len(activated_nodes),
        "diffusion_ratio": len(activated_nodes) / G.number_of_nodes(),
        "runtime_seconds": end_time - start_time,
    }


def run_main_experiments(G, cost_functions, budgets_by_cost):
    """
    Esegue tutti gli esperimenti principali su G.

    Per ogni funzione costo:
    - Random Cost
    - Degree Cost

    Per ogni algoritmo:
    - Greedy f1
    - Greedy f2
    - Greedy f3
    - WTSS

    Per ogni budget k.
    """
    algorithms = get_algorithms()
    results = []

    for cost_name, costs in cost_functions.items():
        print(f"\nCost function: {cost_name}")

        for budget_percentage, k in budgets_by_cost[cost_name].items():
            print(f"  Budget {budget_percentage * 100:.1f}% -> k={k}")

            for algorithm_name, algorithm_fn in algorithms.items():
                print(f"    Running {algorithm_name}...")

                result = run_single_experiment(
                    G=G,
                    algorithm_name=algorithm_name,
                    algorithm_fn=algorithm_fn,
                    costs=costs,
                    cost_function_name=cost_name,
                    budget_percentage=budget_percentage,
                    k=k,
                )

                results.append(result)

    return results


def run_edge_removal_experiment(G, seed_set, original_influence, removal_percentages, seed=42):
    """
    Stress test con rimozione casuale di archi.

    Il seed set S viene calcolato sul grafo originale G.
    Poi si rimuovono x archi ottenendo G' e si valuta Inf[G', S].
    """
    results = []
    num_edges = G.number_of_edges()

    for p in removal_percentages:
        removed_edges = int(num_edges * p)

        G_prime = remove_x_edges(G, removed_edges, seed=seed)

        # Per gli archi, i nodi restano gli stessi.
        seed_set_prime = set(seed_set) & set(G_prime.nodes())

        activated_prime = run_majority_cascade(G_prime, seed_set_prime)
        modified_influence = len(activated_prime)

        results.append({
            "removal_type": "edges",
            "removal_percentage": p,
            "removed_edges": removed_edges,
            "original_influence": original_influence,
            "modified_influence": modified_influence,
            "original_ratio": original_influence / G.number_of_nodes(),
            "modified_ratio": modified_influence / G_prime.number_of_nodes(),
            "absolute_loss": original_influence - modified_influence,
            "percentage_loss": (
                ((original_influence - modified_influence) / original_influence) * 100
                if original_influence > 0 else 0
            ),
        })

    return results


def run_node_removal_experiment(G, seed_set, original_influence, removal_percentages, seed=42):
    """
    Stress test con rimozione casuale di nodi.

    Il seed set S viene calcolato sul grafo originale G.
    Dopo la rimozione dei nodi, si usa S' = S ∩ V(G').
    """
    results = []
    num_nodes = G.number_of_nodes()

    for p in removal_percentages:
        removed_nodes = int(num_nodes * p)

        G_prime = remove_y_nodes(G, removed_nodes, seed=seed)

        seed_set_prime = set(seed_set) & set(G_prime.nodes())
        removed_seed_nodes = len(set(seed_set) - seed_set_prime)

        activated_prime = run_majority_cascade(G_prime, seed_set_prime)
        modified_influence = len(activated_prime)

        results.append({
            "removal_type": "nodes",
            "removal_percentage": p,
            "removed_nodes": removed_nodes,
            "removed_seed_nodes": removed_seed_nodes,
            "original_influence": original_influence,
            "modified_influence": modified_influence,
            "original_ratio": original_influence / G.number_of_nodes(),
            "modified_ratio": modified_influence / G_prime.number_of_nodes(),
            "absolute_loss": original_influence - modified_influence,
            "percentage_loss": (
                ((original_influence - modified_influence) / original_influence) * 100
                if original_influence > 0 else 0
            ),
        })

    return results