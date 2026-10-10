import cv2
import numpy as np


class PitchVisualizer:
    def __init__(self):
        self.w = 900
        self.h = 600

    def _map(self, point):
        x, y = point
        px = int(50 + (x / 100.0) * (self.w - 100))
        py = int(50 + (y / 100.0) * (self.h - 100))
        return px, py

    def _base_pitch(self):
        img = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        img[:] = (45, 120, 45)

        cv2.rectangle(img, (50, 50), (self.w - 50, self.h - 50), (255, 255, 255), 2)
        cv2.line(img, (self.w // 2, 50), (self.w // 2, self.h - 50), (255, 255, 255), 2)
        cv2.circle(img, (self.w // 2, self.h // 2), 70, (255, 255, 255), 2)
        return img

    def draw(self, team_a, team_b, ball_point, summary):
        img = self._base_pitch()

        for p in team_a:
            cv2.circle(img, self._map(p["point"]), 10, (60, 220, 60), -1)
        for p in team_b:
            cv2.circle(img, self._map(p["point"]), 10, (70, 100, 240), -1)
        if ball_point is not None:
            cv2.circle(img, self._map(ball_point), 6, (0, 230, 230), -1)

        cv2.rectangle(img, (10, 8), (self.w - 10, 42), (0, 0, 0), -1)
        text = (
            f"A: {summary.get('formation_a','Unknown')} / {summary.get('phase_a','Unknown')}    "
            f"B: {summary.get('formation_b','Unknown')} / {summary.get('phase_b','Unknown')}"
        )
        cv2.putText(img, text, (24, 32), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2, cv2.LINE_AA)
        return img
