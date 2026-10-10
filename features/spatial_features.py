import numpy as np


def compute_team_spatial_features(points):
    if not points:
        return {
            "width": 0.0,
            "depth": 0.0,
            "centroid_x": 0.0,
            "centroid_y": 0.0,
            "compactness": 0.0,
            "avg_spacing": 0.0,
        }

    pts = np.asarray(points, dtype=float)
    xs = pts[:, 0]
    ys = pts[:, 1]
    width = float(ys.max() - ys.min()) if len(ys) > 1 else 0.0
    depth = float(xs.max() - xs.min()) if len(xs) > 1 else 0.0

    centroid = pts.mean(axis=0)

    if len(pts) >= 2:
        dmat = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(axis=2))
        dmat[dmat == 0] = np.inf
        avg_spacing = float(np.min(dmat, axis=1).mean())
    else:
        avg_spacing = 0.0

    # Higher value => more compact, bounded roughly 0..1.
    occupied = max(width * depth, 1.0)
    compactness = float(1.0 / (1.0 + occupied / 1000.0))

    return {
        "width": width,
        "depth": depth,
        "centroid_x": float(centroid[0]),
        "centroid_y": float(centroid[1]),
        "compactness": compactness,
        "avg_spacing": avg_spacing,
    }
