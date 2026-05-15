import math


# ---------------------------------------------------------
# FUNZIONI DI SUPPORTO
# ---------------------------------------------------------

def compute_thresholds(G):
    """
    Calcola la soglia majority di ogni nodo:

    tau(v) = ceil(d(v) / 2).
    """
    return {
        v: math.ceil(G.degree(v) / 2)
        for v in G.nodes()
    }


def total_cost(S, costs):
    """
    Calcola il costo totale di un seed set S.
    """
    return sum(costs[u] for u in S)


def get_marginal_gain(G, S, u, potential_type, thresholds, neighbors):
    """
    Calcola il guadagno marginale Delta_f(S, u) ottenuto aggiungendo
    il nodo u al seed set S.

    Le funzioni considerate sono f1, f2 e f3, come nell'Algorithm 1
    delle slide.
    """
    gain = 0.0

    for v in neighbors[u]:
        d_v = G.degree(v)

        if d_v == 0:
            continue

        active_before = len(neighbors[v] & S)
        i = active_before + 1
        threshold = thresholds[v]

        if potential_type == "f1":
            if active_before < threshold:
                gain += 1.0

        elif potential_type == "f2":
            if i <= threshold:
                gain += threshold - i + 1

        elif potential_type == "f3":
            if i <= threshold:
                numerator = threshold - i + 1
                denominator = d_v - i + 1

                if denominator > 0:
                    gain += numerator / denominator

        else:
            raise ValueError("potential_type deve essere 'f1', 'f2' oppure 'f3'.")

    return gain


def ratio_gain_cost(gain, cost):
    """
    Calcola il rapporto Delta_f / c(u), gestendo il caso di costo nullo.
    """
    if cost == 0:
        return float("inf") if gain > 0 else 0.0

    return gain / cost


# ---------------------------------------------------------
# ALGORITMO 1: COST-SEEDS-GREEDY
# ---------------------------------------------------------

def algorithm_1_greedy(G, k, costs, potential_type="f1"):
    """
    Implementazione dell'Algorithm 1 delle slide: Cost-Seeds-Greedy.

    A ogni iterazione seleziona il nodo u che massimizza:

        Delta_f_i(S, u) / c(u)

    Il procedimento continua finché il costo del seed set supera k.
    Quando il budget viene superato, viene restituito il seed set precedente.
    """

    S_d = set()
    S_p = set()

    thresholds = compute_thresholds(G)

    neighbors = {
        u: set(G.neighbors(u))
        for u in G.nodes()
    }

    while len(S_d) < G.number_of_nodes():
        best_u = None
        best_ratio = float("-inf")
        best_gain = float("-inf")

        for u in G.nodes():
            if u in S_d:
                continue

            gain = get_marginal_gain(
                G=G,
                S=S_d,
                u=u,
                potential_type=potential_type,
                thresholds=thresholds,
                neighbors=neighbors
            )

            ratio = ratio_gain_cost(gain, costs[u])

            if (
                ratio > best_ratio
                or (ratio == best_ratio and gain > best_gain)
            ):
                best_ratio = ratio
                best_gain = gain
                best_u = u

        if best_u is None:
            break

        S_p = S_d.copy()
        S_d.add(best_u)

        if total_cost(S_d, costs) > k:
            return S_p

    return S_d


# ---------------------------------------------------------
# ALGORITMO 2: WTSS
# ---------------------------------------------------------

def algorithm_2_wtss(G, k, costs):
    """
    Implementazione dell'Algorithm 2 delle slide: WTSS.

    Si usa come threshold:

        t(u) = ceil(d(u) / 2)

    L'algoritmo viene fermato quando l'aggiunta di un nuovo nodo al seed set
    farebbe superare il budget k. In quel caso viene restituito il seed set
    precedente, cioè il più grande trovato fino a quel momento con c(S) <= k.
    """

    S = set()
    S_previous = set()

    U = set(G.nodes())

    delta = {
        u: G.degree(u)
        for u in G.nodes()
    }

    kt = {
        u: math.ceil(G.degree(u) / 2)
        for u in G.nodes()
    }

    residual_neighbors = {
        u: set(G.neighbors(u))
        for u in G.nodes()
    }

    while U:
        # Caso 1:
        # esiste v in U tale che k(v) = 0.
        case1_nodes = [
            u for u in U
            if kt[u] <= 0
        ]

        if case1_nodes:
            v = case1_nodes[0]

            # Il nodo v è già attivabile, quindi può contribuire
            # ad attivare i suoi vicini nel grafo residuo.
            for u in residual_neighbors[v] & U:
                kt[u] = max(0, kt[u] - 1)

        else:
            # Caso 2:
            # esiste v in U tale che delta(v) < k(v).
            case2_nodes = [
                u for u in U
                if delta[u] < kt[u]
            ]

            if case2_nodes:
                v = case2_nodes[0]

                S_previous = S.copy()
                S.add(v)

                if total_cost(S, costs) > k:
                    return S_previous

                # Poiché v viene inserito nel seed set, può influenzare
                # i suoi vicini nel grafo residuo.
                for u in residual_neighbors[v] & U:
                    kt[u] = max(0, kt[u] - 1)

            else:
                # Caso 3:
                # si sceglie il nodo che massimizza:
                #
                # c(u) * k(u) / (delta(u) * (delta(u) + 1))
                def wtss_score(u):
                    denominator = delta[u] * (delta[u] + 1)

                    if denominator == 0:
                        return 0

                    return (costs[u] * kt[u]) / denominator

                v = max(U, key=wtss_score)

        # Rimuove v dal grafo residuo.
        for u in residual_neighbors[v] & U:
            delta[u] = max(0, delta[u] - 1)
            residual_neighbors[u].discard(v)

        U.remove(v)

    return S