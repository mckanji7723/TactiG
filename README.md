# TactiG

**Football Formation and Match-Phase Recognition using Computer Vision, Spatial Graphs and Clustering**

TactiG is a compact Pattern Recognition course project that analyzes a short football match clip and produces:

- YOLO-based player and ball detection
- persistent player tracking
- jersey-colour based team separation
- normalized player coordinates
- spatial/graph features
- formation estimation
- attacking / defending / transition phase estimation
- annotated output video
- 2D tactical output video
- per-window CSV analysis

## Recommended input

Start with a 30-60 second broadcast clip in which:
- most outfield players are visible
- the camera is fairly wide
- team jersey colours are clearly different
- there are few replays/cuts

Place the file at:

`input/match_clip.mp4`

## Install

Python 3.11 or 3.12 is recommended.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```powershell
python main.py --video input\match_clip.mp4
```

The first run may download the pretrained YOLO model automatically.

## Outputs

After a successful run:

```text
output/
├── analysed_match.mp4
├── tactical_view.mp4
└── analysis.csv
```

## Important project assumption

This MVP deliberately uses **normalized screen coordinates** instead of full pitch homography. That makes the project much easier to complete and demonstrate. Formation recognition therefore works best on wide broadcast views with limited camera distortion.

A future version can replace `positions/coordinate_mapper.py` with a pitch-homography module.
