import math
from collections import deque

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

def algorithm_3_threshold_deficit_greedy(G, costs, budget, return_info=False):
    """
    Threshold-Deficit Greedy.

    Euristica greedy per il modello Cost Majority Cascade.

    Idea generale:
    - ogni nodo v ha una soglia majority tau(v) = ceil(d(v) / 2);
    - ogni nodo v ha un deficit def(v), cioè il numero di vicini attivi
      che mancano per raggiungere la soglia;
    - a ogni iterazione scegliamo come seed il nodo che offre il miglior
      beneficio stimato rispetto al costo.

    Il beneficio stimato di un nodo u è:

        score(u) = 1 + somma_{v vicino di u, v non attivo} 1 / def(v)

    Il termine 1 rappresenta il fatto che, scegliendo u come seed,
    u diventa sicuramente attivo.

    Il termine 1 / def(v) dà più peso ai vicini che sono vicini
    all'attivazione. Per esempio:
    - se def(v) = 1, basta un solo vicino attivo per attivare v;
    - se def(v) = 4, v è ancora lontano dall'attivazione.

    Parameters
    ----------
    G : networkx.Graph
        Grafo non orientato.
    costs : dict
        Dizionario dei costi: costs[u] = costo del nodo u.
    budget : int or float
        Budget massimo disponibile.
    return_info : bool
        Se True, restituisce anche informazioni aggiuntive utili
        per debug/analisi.

    Returns
    -------
    set
        Seed set selezionato.
    """

    # Verifichiamo che ogni nodo del grafo abbia un costo associato.
    missing_costs = [u for u in G.nodes() if u not in costs]
    if missing_costs:
        raise ValueError(
            f"Mancano i costi per {len(missing_costs)} nodi. "
            f"Esempio nodo senza costo: {missing_costs[0]}"
        )

    # I costi devono essere positivi, perché l'algoritmo usa score / costo.
    for u in G.nodes():
        if costs[u] <= 0:
            raise ValueError(f"Il nodo {u} ha costo non positivo: {costs[u]}")

    # Seed set finale che verrà restituito.
    seeds = set()

    # Costo totale dei seed scelti fino a questo momento.
    current_cost = 0

    # Soglia majority di ogni nodo:
    # tau(v) = ceil(d(v) / 2)
    threshold = {
        v: math.ceil(G.degree(v) / 2)
        for v in G.nodes()
    }

    # Deficit iniziale:
    # all'inizio nessun nodo è attivo, quindi a(v)=0.
    # Dunque def(v) = tau(v).
    deficit = {
        v: threshold[v]
        for v in G.nodes()
    }

    # Insieme dei nodi attivi.
    # In un grafo senza nodi isolati sarà inizialmente vuoto.
    # Tuttavia, dopo eventuali rimozioni di nodi/archi, possono comparire
    # nodi con grado 0. In quel caso tau(v)=0, quindi sono già attivi
    # secondo la condizione majority.
    active = {
        v for v in G.nodes()
        if deficit[v] <= 0
    }

    # Fissiamo una lista dei nodi per avere iterazioni stabili e riproducibili.
    nodes = list(G.nodes())

    # Ciclo greedy
    while True:
        best_node = None
        best_score = None
        best_ratio = None
        best_key = None

        # Cerchiamo il miglior nodo candidato.
        # Un nodo è candidato se:
        # - non è già attivo;
        # - può essere acquistato senza superare il budget.
        for u in nodes:

            # Se u è già attivo, non ha senso sceglierlo come seed.
            if u in active:
                continue

            cost_u = costs[u]

            # Rispettiamo il vincolo di budget.
            if current_cost + cost_u > budget:
                continue

            # Il termine 1 rappresenta l'attivazione certa di u come seed.
            score = 1.0

            # Ogni vicino non ancora attivo riceve un contributo pari a 1/def(v).
            # Più il deficit è basso, più il contributo è alto.
            for v in G.neighbors(u):
                if v not in active and deficit[v] > 0:
                    score += 1.0 / deficit[v]

            # Beneficio per unità di costo.
            ratio = score / cost_u

            # Tie-break:
            # 1. massimizza ratio;
            # 2. a parità di ratio, massimizza score;
            # 3. a parità di score, preferisce nodi con grado maggiore.
            #
            # Non inseriamo il nodo u nella chiave, così evitiamo problemi
            # se le label dei nodi non sono confrontabili tra loro.
            key = (ratio, score, G.degree(u))

            if best_key is None or key > best_key:
                best_key = key
                best_node = u
                best_score = score
                best_ratio = ratio

        # Se non esiste nessun candidato acquistabile, l'algoritmo termina.
        if best_node is None:
            break

        seeds.add(best_node)
        current_cost += costs[best_node]

        # Il seed scelto diventa immediatamente attivo.
        active.add(best_node)

        # Usiamo una coda per propagare le attivazioni successive.
        # Ogni volta che un nodo diventa attivo, può ridurre il deficit
        # dei suoi vicini.
        queue = deque([best_node])

        # -------------------------------
        # 5. Propagazione della cascata
        # -------------------------------

        while queue:
            x = queue.popleft()

            # Ogni vicino non ancora attivo vede ridursi il proprio deficit,
            # perché x è appena diventato attivo.
            for v in G.neighbors(x):

                if v in active:
                    continue

                # Riduciamo il deficit di v di una unità.
                deficit[v] = max(0, deficit[v] - 1)

                # Se il deficit arriva a 0, v raggiunge la soglia majority
                # e diventa attivo a sua volta.
                if deficit[v] == 0:
                    active.add(v)
                    queue.append(v)

    if return_info:
        return {
            "seeds": seeds,
            "active": active,
            "seed_cost": current_cost,
            "num_seeds": len(seeds),
            "num_active_internal": len(active),
            "remaining_budget": budget - current_cost,
        }

    return seeds