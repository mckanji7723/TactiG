from ultralytics import YOLO


class FootballDetector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = YOLO(cfg["model"]["weights"])
        self.person_class = int(cfg["model"]["classes"]["person"])
        self.ball_class = int(cfg["model"]["classes"]["ball"])

    def track(self, frame):
        results = self.model.track(
            frame,
            persist=True,
            verbose=False,
            conf=float(self.cfg["model"]["confidence"]),
            iou=float(self.cfg["model"]["iou"]),
            classes=[self.person_class, self.ball_class],
            tracker="bytetrack.yaml"
        )

        detections = []
        if not results:
            return detections

        result = results[0]
        if result.boxes is None:
            return detections

        boxes = result.boxes
        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i].item())
            conf = float(boxes.conf[i].item())
            xyxy = boxes.xyxy[i].cpu().numpy().tolist()
            track_id = -1
            if boxes.id is not None:
                track_id = int(boxes.id[i].item())

            kind = "person" if cls_id == self.person_class else "ball"
            detections.append({
                "kind": kind,
                "class_id": cls_id,
                "conf": conf,
                "track_id": track_id,
                "xyxy": xyxy,
            })
        return detections
