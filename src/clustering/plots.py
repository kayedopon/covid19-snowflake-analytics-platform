from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA

from src.clustering.model import fit_kmeans


def create_output_folders(base_dir):
    base_dir = Path(base_dir)

    folders = {
        "metrics": base_dir / "metrics",
        "cluster_sizes": base_dir / "cluster_sizes",
        "pca": base_dir / "pca",
        "data": base_dir / "data"
    }

    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    return folders


def save_metric_chart(
    evaluation_df,
    metric,
    title,
    ylabel,
    output_path
):
    plt.figure(figsize=(8, 5))

    plt.plot(
        evaluation_df["k"],
        evaluation_df[metric],
        marker="o"
    )

    plt.xlabel("Number of clusters (k)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(evaluation_df["k"])
    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()


def save_all_metric_charts(evaluation_df, output_dir):
    save_metric_chart(
        evaluation_df,
        metric="silhouette",
        title="Silhouette Score by Number of Clusters",
        ylabel="Silhouette Score",
        output_path=output_dir / "silhouette_score.png"
    )

    save_metric_chart(
        evaluation_df,
        metric="calinski_harabasz",
        title="Calinski-Harabasz Score by Number of Clusters",
        ylabel="Calinski-Harabasz Score",
        output_path=output_dir / "calinski_harabasz_score.png"
    )

    save_metric_chart(
        evaluation_df,
        metric="davies_bouldin",
        title="Davies-Bouldin Score by Number of Clusters",
        ylabel="Davies-Bouldin Score",
        output_path=output_dir / "davies_bouldin_score.png"
    )


def save_cluster_size_charts(
    X_scaled,
    output_dir,
    min_k=2,
    max_k=6
):
    for k in range(min_k, max_k + 1):
        _, labels = fit_kmeans(X_scaled, k)

        cluster_sizes = pd.Series(labels).value_counts().sort_index()

        plt.figure(figsize=(8, 5))
        plt.bar(
            [
                f"Cluster {cluster}"
                for cluster in cluster_sizes.index
            ],
            cluster_sizes.values
        )
        plt.xlabel("Cluster")
        plt.ylabel("Number of countries")
        plt.title(f"Cluster Sizes for k={k}")
        plt.tight_layout()

        plt.savefig(output_dir / f"cluster_sizes_k{k}.png")
        plt.close()


def save_pca_charts(
    X_scaled,
    output_dir,
    min_k=2,
    max_k=6
):
    pca = PCA(n_components=2)

    components = pca.fit_transform(X_scaled)

    for k in range(min_k, max_k + 1):
        _, labels = fit_kmeans(X_scaled, k)

        plt.figure(figsize=(10, 7))
        scatter = plt.scatter(
            components[:, 0],
            components[:, 1],
            c=labels
        )
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.title(f"COVID-19 Country Clusters - k={k}")
        plt.legend(*scatter.legend_elements(), title="Cluster")
        plt.tight_layout()

        plt.savefig(output_dir/ f"country_clusters_pca_k{k}.png")
        plt.close()