import cv2
import numpy as np
from sklearn.cluster import KMeans


class TeamClassifier:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = None
        self.centers = None

    def extract_jersey_crop(self, frame, xyxy):
        x1, y1, x2, y2 = map(int, xyxy)
        x1 = max(0, x1); y1 = max(0, y1)
        x2 = min(frame.shape[1], x2); y2 = min(frame.shape[0], y2)

        w = x2 - x1
        h = y2 - y1
        if w < self.cfg["team"]["min_crop_width"] or h < self.cfg["team"]["min_crop_height"]:
            return None

        # Focus on upper torso to reduce shorts, grass and skin.
        cx1 = x1 + int(0.2 * w)
        cx2 = x2 - int(0.2 * w)
        cy1 = y1 + int(0.15 * h)
        cy2 = y1 + int(0.55 * h)
        crop = frame[cy1:cy2, cx1:cx2]
        if crop.size == 0:
            return None
        return crop

    def _feature(self, crop):
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        pixels = hsv.reshape(-1, 3)
        # Ignore very dark and weakly saturated pixels.
        mask = (pixels[:, 2] > 45) & (pixels[:, 1] > 35)
        pixels = pixels[mask]
        if len(pixels) == 0:
            return np.array([0.0, 0.0, 0.0])
        return np.median(pixels, axis=0).astype(float)

    def fit(self, crops):
        feats = np.array([self._feature(c) for c in crops if c is not None])
        if len(feats) < 2:
            return
        self.model = KMeans(n_clusters=2, random_state=42, n_init=10)
        self.model.fit(feats)
        self.centers = self.model.cluster_centers_

    def predict_from_frame(self, frame, xyxy):
        crop = self.extract_jersey_crop(frame, xyxy)
        if crop is None or self.model is None:
            return -1
        feat = self._feature(crop).reshape(1, -1)
        return int(self.model.predict(feat)[0])
