import numpy as np

def cluster(features):
    # choose two reference points
    c0 = features[0]
    c1 = features[1]

    labels = []
    for f in features:
        d0 = np.linalg.norm(f - c0)
        d1 = np.linalg.norm(f - c1)
        labels.append(0 if d0 < d1 else 1)
    return labels


# --- Base QML feature outputs (from your runs) ---
base_features = np.array([
    [0.24, 0.26, 0.28, 0.22],   # input [0.1, 0.2]
    [0.26, 0.23, 0.24, 0.27],   # input [1.0, 1.2]
    [0.24, 0.25, 0.27, 0.24]    # input [0.15, 0.25]
])

print("\nBase features:")
print(base_features)
print("Cluster labels:", cluster(base_features))


# --- Small variation 1: slightly noisy features ---
variation_1 = base_features + np.random.normal(0, 0.01, base_features.shape)

print("\nVariation 1 (small noise):")
print(variation_1)
print("Cluster labels:", cluster(variation_1))


# --- Small variation 2: averaged features (smoother) ---
variation_2 = (base_features + variation_1) / 2

print("\nVariation 2 (averaged):")
print(variation_2)
print("Cluster labels:", cluster(variation_2))

