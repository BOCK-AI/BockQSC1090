import numpy as np

# Example QML feature outputs (probabilities)
# Each row = [P(00), P(01), P(10), P(11)]
features = np.array([
    [0.24, 0.26, 0.28, 0.22],   # input [0.1, 0.2]
    [0.26, 0.23, 0.24, 0.27],   # input [1.0, 1.2]
    [0.24, 0.25, 0.27, 0.24]    # input [0.15, 0.25]
])

# choose two reference points as clusters
cluster_a = features[0]
cluster_b = features[1]

labels = []

for f in features:
    dist_a = np.linalg.norm(f - cluster_a)
    dist_b = np.linalg.norm(f - cluster_b)
    labels.append(0 if dist_a < dist_b else 1)

print("\nQML feature vectors:")
for f in features:
    print(f)

print("\nAssigned cluster labels:", labels)
