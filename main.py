import argparse
from pathlib import Path
import cv2
import yaml
import pandas as pd

from detection.detector import FootballDetector
from teams.team_classifier import TeamClassifier
from positions.coordinate_mapper import CoordinateMapper
from features.spatial_features import compute_team_spatial_features
from features.graph_features import compute_graph_features
from formation.formation_detector import FormationDetector
from phase.phase_detector import PhaseDetector
from visualization.video_visualizer import VideoVisualizer
from visualization.pitch_visualizer import PitchVisualizer


def load_config(path="config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_args():
    parser = argparse.ArgumentParser(description="TactiG football tactical analysis")
    parser.add_argument("--video", required=True, help="Path to football video")
    parser.add_argument("--config", default="config/config.yaml")
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)

    video_path = Path(args.video)
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    detector = FootballDetector(cfg)
    team_classifier = TeamClassifier(cfg)
    mapper = CoordinateMapper()
    formation_detector = FormationDetector(cfg)
    phase_detector = PhaseDetector(cfg)
    video_viz = VideoVisualizer()
    pitch_viz = PitchVisualizer()

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    src_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    analysis_fps = min(float(cfg["video"]["analysis_fps"]), src_fps)
    frame_stride = max(1, int(round(src_fps / analysis_fps)))
    effective_fps = src_fps / frame_stride

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    annotated_writer = cv2.VideoWriter(
        str(out_dir / "analysed_match.mp4"),
        fourcc,
        effective_fps,
        (width, height)
    )
    pitch_writer = cv2.VideoWriter(
        str(out_dir / "tactical_view.mp4"),
        fourcc,
        effective_fps,
        (900, 600)
    )

    window_seconds = float(cfg["video"]["tactical_window_seconds"])
    window_frames = max(1, int(round(window_seconds * effective_fps)))

    frame_idx = 0
    processed_idx = 0
    rows = []

    team_classifier_bootstrapped = False
    recent_player_crops = []

    current_summary = {
        "formation_a": "Unknown",
        "formation_b": "Unknown",
        "phase_a": "Unknown",
        "phase_b": "Unknown",
        "width_a": 0.0,
        "width_b": 0.0,
        "compactness_a": 0.0,
        "compactness_b": 0.0,
    }

    window_positions_a = []
    window_positions_b = []
    window_ball = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_idx % frame_stride != 0:
            frame_idx += 1
            continue

        timestamp = frame_idx / src_fps
        detections = detector.track(frame)

        player_dets = [d for d in detections if d["kind"] == "person"]
        ball_dets = [d for d in detections if d["kind"] == "ball"]

        # Bootstrap team classifier from player crops collected early in the clip.
        if not team_classifier_bootstrapped:
            for det in player_dets:
                crop = team_classifier.extract_jersey_crop(frame, det["xyxy"])
                if crop is not None:
                    recent_player_crops.append(crop)
            if len(recent_player_crops) >= 20 or processed_idx >= max(10, int(effective_fps * 2)):
                team_classifier.fit(recent_player_crops)
                team_classifier_bootstrapped = True

        team_a_players, team_b_players, unknown_players = [], [], []

        for det in player_dets:
            team = team_classifier.predict_from_frame(frame, det["xyxy"]) if team_classifier_bootstrapped else -1
            point = mapper.bbox_to_normalized_bottom_center(det["xyxy"], width, height)
            player = {**det, "team": team, "point": point}
            if team == 0:
                team_a_players.append(player)
            elif team == 1:
                team_b_players.append(player)
            else:
                unknown_players.append(player)

        ball_point = None
        if ball_dets:
            best_ball = max(ball_dets, key=lambda d: d["conf"])
            ball_point = mapper.bbox_to_normalized_center(best_ball["xyxy"], width, height)

        window_positions_a.extend([p["point"] for p in team_a_players])
        window_positions_b.extend([p["point"] for p in team_b_players])
        if ball_point is not None:
            window_ball.append(ball_point)

        if processed_idx % window_frames == 0 and processed_idx > 0:
            features_a = compute_team_spatial_features(window_positions_a)
            features_b = compute_team_spatial_features(window_positions_b)
            graph_a = compute_graph_features(window_positions_a, cfg)
            graph_b = compute_graph_features(window_positions_b, cfg)

            formation_a, conf_a = formation_detector.predict(window_positions_a)
            formation_b, conf_b = formation_detector.predict(window_positions_b)

            phase_a, phase_b = phase_detector.estimate(
                window_positions_a, window_positions_b, window_ball, timestamp
            )

            current_summary = {
                "formation_a": formation_a,
                "formation_b": formation_b,
                "formation_conf_a": conf_a,
                "formation_conf_b": conf_b,
                "phase_a": phase_a,
                "phase_b": phase_b,
                "width_a": features_a["width"],
                "width_b": features_b["width"],
                "compactness_a": features_a["compactness"],
                "compactness_b": features_b["compactness"],
            }

            rows.append({
                "time_sec": round(timestamp, 2),
                "formation_team_a": formation_a,
                "formation_conf_team_a": round(conf_a, 3),
                "phase_team_a": phase_a,
                "width_team_a": round(features_a["width"], 2),
                "depth_team_a": round(features_a["depth"], 2),
                "compactness_team_a": round(features_a["compactness"], 3),
                "avg_spacing_team_a": round(features_a["avg_spacing"], 2),
                "graph_density_team_a": round(graph_a["density"], 3),
                "formation_team_b": formation_b,
                "formation_conf_team_b": round(conf_b, 3),
                "phase_team_b": phase_b,
                "width_team_b": round(features_b["width"], 2),
                "depth_team_b": round(features_b["depth"], 2),
                "compactness_team_b": round(features_b["compactness"], 3),
                "avg_spacing_team_b": round(features_b["avg_spacing"], 2),
                "graph_density_team_b": round(graph_b["density"], 3),
            })

            window_positions_a = []
            window_positions_b = []
            window_ball = []

        annotated = video_viz.draw(
            frame,
            team_a_players,
            team_b_players,
            unknown_players,
            ball_dets,
            current_summary
        )
        annotated_writer.write(annotated)

        pitch_frame = pitch_viz.draw(
            team_a_players,
            team_b_players,
            ball_point,
            current_summary
        )
        pitch_writer.write(pitch_frame)

        processed_idx += 1
        frame_idx += 1

    cap.release()
    annotated_writer.release()
    pitch_writer.release()

    pd.DataFrame(rows).to_csv(out_dir / "analysis.csv", index=False)

    print("TactiG analysis completed.")
    print(f"Annotated video: {out_dir / 'analysed_match.mp4'}")
    print(f"Tactical video:  {out_dir / 'tactical_view.mp4'}")
    print(f"CSV analysis:    {out_dir / 'analysis.csv'}")


if __name__ == "__main__":
    main()
