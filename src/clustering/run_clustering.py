from pathlib import Path

from src.clustering.data import load_clustering_data, prepare_clustering_data
from src.clustering.model import scale_features, fit_kmeans
from src.clustering.evaluation import evaluate_k_values
from src.clustering.plots import create_output_folders, save_all_metric_charts, save_cluster_size_charts, save_pca_charts


OUTPUT_DIR = Path("outputs/clustering")

MIN_K = 2
MAX_K = 6


def main():
    folders = create_output_folders(OUTPUT_DIR)

    df = load_clustering_data()

    print("Raw clustering data:")
    print(df.head())

    clustering_df = prepare_clustering_data(df)

    print("\nPrepared clustering data:")
    print(clustering_df.head())

    feature_columns = [column for column in clustering_df.columns if column != "country"]

    X_scaled, _ = scale_features(clustering_df, feature_columns)

    evaluation = evaluate_k_values(X_scaled, min_k=MIN_K, max_k=MAX_K)

    print("\nClustering evaluation:")

    for _, row in evaluation.iterrows():
        print(
            f"k={row['k']} | "
            f"Silhouette={row['silhouette']:.4f} | "
            f"Calinski-Harabasz={row['calinski_harabasz']:.2f} | "
            f"Davies-Bouldin={row['davies_bouldin']:.4f} | "
            f"Sizes={row['cluster_sizes']}"
        )

    metrics_output = evaluation.drop(columns=["cluster_sizes"])

    metrics_output.to_csv(folders["data"] / "clustering_metrics.csv", index=False)

    save_all_metric_charts(evaluation, folders["metrics"])

    save_cluster_size_charts(
        X_scaled,
        folders["cluster_sizes"],
        min_k=MIN_K,
        max_k=MAX_K
    )

    save_pca_charts(
        X_scaled,
        folders["pca"],
        min_k=MIN_K,
        max_k=MAX_K
    )

    # final clusterin on k that I think is the best

    best_k = 2

    _, labels = fit_kmeans(X_scaled, best_k)

    clustering_df["cluster"] = labels
    clustering_df.to_csv(folders["data"] / "country_clusters.csv", index=False)

    print("\nCluster sizes:")
    print(clustering_df["cluster"].value_counts().sort_index())

    print("\nCountries by cluster:")

    for cluster in sorted(clustering_df["cluster"].unique()):
        countries = clustering_df[clustering_df["cluster"] == cluster]["country"].tolist()

        print(f"\nCluster {cluster}:")
        print(", ".join(countries))

    cluster_summary = clustering_df.groupby("cluster")[feature_columns].mean()
    cluster_summary.to_csv(folders["data"] / "cluster_summary.csv")

    print("\nCluster averages:")
    print(cluster_summary)
    print(f"\nOutputs saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()