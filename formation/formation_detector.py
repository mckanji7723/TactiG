import numpy as np
from sklearn.cluster import KMeans


class FormationDetector:
    """
    Formation estimator using longitudinal player-line clustering.
    This is deliberately simple and interpretable for a Pattern Recognition MVP.
    """

    TEMPLATES = {
        "4-3-3": [4, 3, 3],
        "4-4-2": [4, 4, 2],
        "4-2-3-1": [4, 2, 3, 1],
        "3-5-2": [3, 5, 2],
    }

    def __init__(self, cfg):
        supported = cfg["formation"]["supported"]
        self.templates = {k: v for k, v in self.TEMPLATES.items() if k in supported}

    @staticmethod
    def _representative_players(points):
        """
        Window data contains repeated observations of tracked players.
        We do not have track IDs here, so reduce to spatial centroids via KMeans.
        Target 10 outfield representatives where possible.
        """
        pts = np.asarray(points, dtype=float)
        if len(pts) <= 10:
            return pts
        n_clusters = min(10, max(3, len(pts) // 5))
        n_clusters = min(n_clusters, 10)
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        km.fit(pts)
        return km.cluster_centers_

    def predict(self, points):
        if len(points) < 6:
            return "Unknown", 0.0

        reps = self._representative_players(points)
        xs = reps[:, 0].reshape(-1, 1)

        best_name = "Unknown"
        best_score = 1e9

        for name, template in self.templates.items():
            k = len(template)
            if len(reps) < k:
                continue

            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(xs)
            centers = km.cluster_centers_.flatten()
            order = np.argsort(centers)

            counts = []
            for cluster_id in order:
                counts.append(int(np.sum(labels == cluster_id)))

            # Scale template if representative player count differs from 10.
            target = np.asarray(template, dtype=float)
            target = target / target.sum() * len(reps)
            score = float(np.abs(np.asarray(counts, dtype=float) - target).sum())

            if score < best_score:
                best_score = score
                best_name = name

        confidence = max(0.0, 1.0 - best_score / max(1.0, len(reps) * 1.5))
        return best_name, float(confidence)
