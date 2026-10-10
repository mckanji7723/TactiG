import numpy as np
import networkx as nx


def compute_graph_features(points, cfg):
    if len(points) < 2:
        return {"density": 0.0, "avg_degree": 0.0, "avg_edge_length": 0.0}

    pts = np.asarray(points, dtype=float)
    n = len(pts)
    k = max(1, min(int(cfg["graph"]["k_neighbors"]), n - 1))

    g = nx.Graph()
    for i in range(n):
        g.add_node(i)

    edge_lengths = []
    for i in range(n):
        dists = np.sqrt(((pts - pts[i]) ** 2).sum(axis=1))
        order = np.argsort(dists)
        neighbors = [j for j in order if j != i][:k]
        for j in neighbors:
            dist = float(dists[j])
            if not g.has_edge(i, j):
                g.add_edge(i, j, weight=dist)
                edge_lengths.append(dist)

    density = nx.density(g)
    avg_degree = float(sum(dict(g.degree()).values()) / n)
    avg_edge_length = float(np.mean(edge_lengths)) if edge_lengths else 0.0

    return {
        "density": float(density),
        "avg_degree": avg_degree,
        "avg_edge_length": avg_edge_length,
    }
