import pandas as pd

from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

from src.clustering.model import fit_kmeans


def evaluate_k_values(X_scaled, min_k=2, max_k=6):
    results = []

    for k in range(min_k, max_k + 1):
        _, labels = fit_kmeans(X_scaled, k)

        cluster_sizes = pd.Series(labels).value_counts().sort_index().to_dict()

        results.append({
            "k": k,
            "silhouette": silhouette_score(
                X_scaled,
                labels
            ),
            "calinski_harabasz": calinski_harabasz_score(
                X_scaled,
                labels
            ),
            "davies_bouldin": davies_bouldin_score(
                X_scaled,
                labels
            ),
            "cluster_sizes": cluster_sizes
        })

    return pd.DataFrame(results)