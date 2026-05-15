import matplotlib.pyplot as plt


def plot_influence_vs_budget(results_df, cost_function_name, output_path):
    """
    Grafico diffusion ratio vs budget k per una specifica funzione costo.
    """
    subset = results_df[results_df["cost_function"] == cost_function_name]

    plt.figure(figsize=(8, 5))

    for algorithm_name in subset["algorithm"].unique():
        alg_data = subset[subset["algorithm"] == algorithm_name].sort_values("budget_k")

        plt.plot(
            alg_data["budget_k"],
            alg_data["diffusion_ratio"],
            marker="o",
            label=algorithm_name
        )

    plt.xlabel("Budget k")
    plt.ylabel("Diffusion ratio |Inf[G,S]| / |V|")
    plt.title(f"Diffusion ratio al variare del budget - {cost_function_name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()


def plot_removal_stress_test(results_df, output_path, title):
    """
    Grafico per gli stress test su G'.
    Mostra il diffusion ratio originale e quello dopo la modifica della rete.
    """
    plt.figure(figsize=(8, 5))

    plt.plot(
        results_df["removal_percentage"],
        results_df["modified_ratio"],
        marker="o",
        label="Diffusion ratio su G'"
    )

    plt.axhline(
        y=results_df["original_ratio"].iloc[0],
        linestyle="--",
        label="Diffusion ratio originale su G"
    )

    plt.xlabel("Percentuale rimossa")
    plt.ylabel("Diffusion ratio")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()