import cv2


class VideoVisualizer:
    TEAM_A = (60, 220, 60)
    TEAM_B = (70, 100, 240)
    UNKNOWN = (180, 180, 180)
    BALL = (0, 230, 230)

    def _draw_player(self, frame, p, color, label_prefix):
        x1, y1, x2, y2 = map(int, p["xyxy"])
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{label_prefix}-{p['track_id']}"
        cv2.putText(frame, label, (x1, max(18, y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    def draw(self, frame, team_a, team_b, unknown, ball_dets, summary):
        out = frame.copy()

        for p in team_a:
            self._draw_player(out, p, self.TEAM_A, "A")
        for p in team_b:
            self._draw_player(out, p, self.TEAM_B, "B")
        for p in unknown:
            self._draw_player(out, p, self.UNKNOWN, "U")

        for b in ball_dets:
            x1, y1, x2, y2 = map(int, b["xyxy"])
            cv2.rectangle(out, (x1, y1), (x2, y2), self.BALL, 2)
            cv2.putText(out, "BALL", (x1, max(18, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.BALL, 1, cv2.LINE_AA)

        panel = out.copy()
        cv2.rectangle(panel, (10, 10), (420, 145), (0, 0, 0), -1)
        cv2.addWeighted(panel, 0.55, out, 0.45, 0, out)

        lines = [
            f"Team A: {summary.get('formation_a', 'Unknown')} | {summary.get('phase_a', 'Unknown')}",
            f"Team B: {summary.get('formation_b', 'Unknown')} | {summary.get('phase_b', 'Unknown')}",
            f"A width: {summary.get('width_a', 0):.1f} | compactness: {summary.get('compactness_a', 0):.2f}",
            f"B width: {summary.get('width_b', 0):.1f} | compactness: {summary.get('compactness_b', 0):.2f}",
        ]

        y = 38
        for line in lines:
            cv2.putText(out, line, (24, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2, cv2.LINE_AA)
            y += 28

        return out
