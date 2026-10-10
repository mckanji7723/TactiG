class CoordinateMapper:
    @staticmethod
    def bbox_to_normalized_bottom_center(xyxy, frame_w, frame_h):
        x1, y1, x2, y2 = xyxy
        x = (x1 + x2) / 2.0
        y = y2
        return (100.0 * x / frame_w, 100.0 * y / frame_h)

    @staticmethod
    def bbox_to_normalized_center(xyxy, frame_w, frame_h):
        x1, y1, x2, y2 = xyxy
        x = (x1 + x2) / 2.0
        y = (y1 + y2) / 2.0
        return (100.0 * x / frame_w, 100.0 * y / frame_h)
