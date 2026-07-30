from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def scale_features(df, feature_columns):
    scaler = StandardScaler()

    X = df[feature_columns]
    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler


def create_kmeans(k):
    return KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )


def fit_kmeans(X_scaled, k):
    model = create_kmeans(k)
    labels = model.fit_predict(X_scaled)

    return model, labels