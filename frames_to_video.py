import cv2
from pathlib import Path

frames_dir = Path(
    r"data\SoccerNet\tracking\train\SNMOT-060\img1"
)

output_path = Path(
    r"input\match_clip.mp4"
)

fps = 25
width = 1920
height = 1080

images = sorted(frames_dir.glob("*.jpg"))

if not images:
    raise FileNotFoundError("No JPG frames found.")

output_path.parent.mkdir(parents=True, exist_ok=True)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    str(output_path),
    fourcc,
    fps,
    (width, height)
)

for img_path in images:
    frame = cv2.imread(str(img_path))

    if frame is None:
        print(f"Skipping unreadable frame: {img_path}")
        continue

    writer.write(frame)

writer.release()

print(f"Created video: {output_path}")
print(f"Frames written: {len(images)}")