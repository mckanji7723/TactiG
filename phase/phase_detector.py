import numpy as np


class PhaseDetector:
    """
    Lightweight phase recognizer:
    - estimate possession by which team's player cloud is closer to the ball
    - mark TRANSITION when possession changes
    - otherwise possession team ATTACKING, other team DEFENDING

    This is a practical MVP approximation of sequential phase recognition.
    """

    def __init__(self, cfg):
        self.transition_seconds = float(cfg["phase"]["transition_seconds"])
        self.last_possession = None
        self.last_change_time = -1e9

    @staticmethod
    def _mean_min_distance(team_points, ball_points):
        if not team_points or not ball_points:
            return np.inf
        players = np.asarray(team_points, dtype=float)
        balls = np.asarray(ball_points, dtype=float)
        vals = []
        for b in balls[-10:]:
            d = np.sqrt(((players - b) ** 2).sum(axis=1))
            vals.append(np.min(d))
        return float(np.mean(vals))

    def estimate(self, team_a_points, team_b_points, ball_points, timestamp):
        da = self._mean_min_distance(team_a_points, ball_points)
        db = self._mean_min_distance(team_b_points, ball_points)

        if not np.isfinite(da) and not np.isfinite(db):
            return "Unknown", "Unknown"

        possession = 0 if da <= db else 1

        if self.last_possession is None:
            self.last_possession = possession
            self.last_change_time = timestamp

        if possession != self.last_possession:
            self.last_possession = possession
            self.last_change_time = timestamp

        if timestamp - self.last_change_time <= self.transition_seconds:
            return "Transition", "Transition"

        if possession == 0:
            return "Attacking", "Defending"
        return "Defending", "Attacking"
