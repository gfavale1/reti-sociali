# Majority Cascade Dynamics in Online Networks

Questo progetto studia la diffusione dell'influenza in reti complesse attraverso il modello di **Majority Cascade** con vincoli di costo. L'obiettivo è selezionare un seed set $S$ che massimizzi il numero finale di nodi attivati, rispettando un budget massimo disponibile.

Il progetto è stato sviluppato nell'ambito del corso di **Reti Sociali** e si basa su una rete peer-to-peer della collezione SNAP, utilizzata per simulare dinamiche di influenza in una rete online.

## Obiettivo del progetto

Dato un grafo $G=(V,E)$, una funzione costo $c:V \rightarrow \mathbb{N}$ e un budget $k$, il problema consiste nel trovare un seed set $S \subseteq V$ tale che:

$$
c(S) \leq k
$$

e che massimizzi il numero finale di nodi attivati:

$$
|Inf[G,S]|
$$

Il modello di diffusione utilizzato è il **Majority Cascade**, in cui un nodo si attiva quando almeno metà dei suoi vicini è già attiva.

## Modello di diffusione

La cascata parte dal seed set iniziale:

$$
Inf[S,0] = S
$$

A ogni round, un nodo non ancora attivo viene attivato se il numero dei suoi vicini attivi è almeno pari alla soglia majority:

$$
\tau(v)=\left\lceil \frac{d(v)}{2} \right\rceil
$$

Il processo termina quando non vengono attivati nuovi nodi. Una volta attivato, un nodo rimane attivo fino alla fine della cascata.

## Dataset

Il dataset utilizzato è **p2p-Gnutella04**, appartenente alla collezione SNAP.

Si tratta di una rete peer-to-peer Gnutella. Il grafo è originariamente diretto, ma nel progetto viene trattato come non orientato, poiché il modello Majority Cascade utilizzato è definito tramite vicinato, grado e soglia majority, senza distinguere tra archi entranti e archi uscenti.

## Algoritmi implementati

Sono stati confrontati cinque algoritmi per la selezione del seed set:

- **Greedy f1**
- **Greedy f2**
- **Greedy f3**
- **WTSS**
- **Threshold-Deficit Greedy**

I primi tre algoritmi sono varianti greedy basate su funzioni di potenziale. WTSS è stato adattato al vincolo di budget. Threshold-Deficit Greedy è l'euristica proposta nel progetto, progettata per sfruttare direttamente la logica del Majority Cascade.

## Funzioni costo

Sono state considerate tre funzioni costo.

### Random Cost

Ogni nodo riceve un costo casuale intero in un intervallo fissato:

$$
c(u) \in [1,10]
$$

Questa funzione non dipende dalla struttura della rete.

### Degree Cost

Il costo di un nodo dipende dal suo grado:

$$
c(u)=\left\lceil \frac{d(u)}{2} \right\rceil
$$

Questa funzione penalizza maggiormente i nodi ad alto grado.

### Sublinear Degree Cost

La funzione costo proposta nel progetto è:

$$
c(u)=1+\left\lceil \log_2(1+d(u)) \right\rceil
$$

Questa funzione mantiene un legame con la struttura della rete, ma penalizza gli hub in modo meno severo rispetto alla Degree Cost.

## Esperimenti

L'analisi sperimentale include:

- il confronto degli algoritmi al variare dei valori di budget;
- la valutazione del numero finale di nodi attivati;
- l'analisi dei tempi di esecuzione;
- stress test basati sulla rimozione casuale di archi e nodi.

I risultati numerici vengono salvati in:

```text
results/data/
```

I grafici generati vengono salvati in:

```text
results/plots/
```