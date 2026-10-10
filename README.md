# TactiG

**Football Formation Recognition and Tactical Phase Analysis using Pattern Recognition**

TactiG is a computer-vision and Pattern Recognition project for analysing football match footage. The system detects and tracks players from video, separates players into teams using visual appearance, converts player locations into spatial representations, estimates team formations, identifies broad tactical phases, and generates annotated output videos and a CSV analysis file.

The project was developed as a **Pattern Recognition course project** and is intended for academic and demonstration purposes.

---

## Project Objective

The main objective of TactiG is to recognise tactical structure from football video.

The processing pipeline is:

```text
Football Video
      ↓
Player / Ball Detection
      ↓
Multi-object Tracking
      ↓
Team Classification
      ↓
Player Coordinate Extraction
      ↓
Spatial / Graph-style Representation
      ↓
Formation Recognition
      ↓
Tactical Phase Recognition
      ↓
Annotated Video + Tactical View + CSV
```

Instead of analysing only individual players, TactiG focuses on the **spatial pattern formed by the team as a whole**.

---

## Main Features

- Football player and ball detection using YOLO
- Multi-object tracking using ByteTrack
- Team separation using jersey-colour features and clustering
- Player-position extraction from video frames
- Normalised player-coordinate representation
- Formation recognition from spatial player arrangements
- Broad tactical phase recognition
- Annotated match-video generation
- Tactical top-down/pitch-view generation
- Frame-level analysis stored in CSV
- Tested with SoccerNet Tracking clips
- Modular Python project structure

### Example Formations

- 4-3-3
- 4-4-2
- 4-2-3-1
- 3-5-2

### Tactical Phases

- Attacking
- Defending
- Transition

---

# Pattern Recognition Concepts Used

TactiG is more than a YOLO detection project. Detection provides the raw objects, while Pattern Recognition is used to interpret the spatial arrangement of those objects.

## 1. Feature Extraction

For each processed frame, the system extracts useful information from detected players.

Typical features include:

- Player x-position
- Player y-position
- Team label
- Relative spacing
- Horizontal spread
- Vertical spread
- Player-group structure
- Distances between players

The raw football frame is therefore transformed into a numerical spatial representation.

---

## 2. Clustering

Clustering is used during team separation.

```text
Detected Player Crops
        ↓
Colour Features
        ↓
Clustering
        ↓
Team A / Team B
```

This is an example of **unsupervised Pattern Recognition**.

---

## 3. Spatial Pattern Recognition

A football formation is fundamentally a spatial pattern.

For example:

```text
4 defenders
3 midfielders
3 attackers
```

creates a different spatial arrangement from:

```text
4 defenders
4 midfielders
2 attackers
```

TactiG analyses the relative positions of players rather than relying only on individual identities.

---

## 4. Coordinate Normalisation

Player locations depend on camera position, zoom and image resolution.

To compare formations more consistently, detected player positions are converted into relative or normalised coordinates.

```text
Pixel Coordinates
      ↓
Normalisation
      ↓
Relative Tactical Coordinates
```

This reduces the effect of raw image scale.

---

## 5. Graph-style Player Relationships

Players can be represented as nodes in a spatial graph.

```text
Player = Node
Spatial Relationship / Distance = Edge
```

A simplified representation may look like:

```text
P1 ---- P2 ---- P3
|       |        |
P4 ---- P5 ---- P6
```

The shape and relative arrangement of these player relationships contain information about the team's tactical structure.

This graph-based interpretation is the reason for the name:

**TactiG = Tactical + Graph**

---

## 6. Formation Classification

After spatial features are extracted, the player arrangement is compared with expected formation structures.

Possible output classes include:

- 4-3-3
- 4-4-2
- 4-2-3-1
- 3-5-2

The recognition stage estimates which formation most closely matches the visible player configuration.

---

## 7. Sequential Pattern Recognition

Football formations and tactical phases cannot always be understood from a single isolated frame.

TactiG analyses consecutive frames:

```text
Frame t
  ↓
Frame t+1
  ↓
Frame t+2
  ↓
...
```

Changes in player positions and team organisation help identify broad tactical phases such as attack, defence and transition.

This connects the project with **Sequential Pattern Recognition**.

---

## 8. Tactical Phase Recognition

The project uses spatial and match-state features to assign a broad phase such as:

- Attacking
- Defending
- Transition

This is a higher-level recognition task built on top of detection, tracking and spatial Pattern Recognition.

---

# Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Object Detection | YOLO / Ultralytics |
| Tracking | ByteTrack |
| Computer Vision | OpenCV |
| Numerical Processing | NumPy |
| Data Processing | Pandas |
| Team Separation | Jersey-colour features + clustering |
| Pattern Recognition | Spatial features, clustering, formation matching |
| Dataset | SoccerNet Tracking |
| Output | MP4 videos + CSV |

---

# Dataset

The project was tested using the **SoccerNet Tracking** dataset.

One sequence used during development was:

```text
SNMOT-060
```

Sequence information:

```text
Frame rate: 25 FPS
Resolution: 1920 × 1080
Sequence length: 750 frames
```

SoccerNet Tracking stores this sequence as individual image frames.

Example:

```text
SNMOT-060/
└── img1/
    ├── 000001.jpg
    ├── 000002.jpg
    ├── 000003.jpg
    └── ...
```

These frames were converted into an MP4 video before running TactiG.

---

# Project Structure

```text
TactiG_Project/
│
├── main.py
├── requirements.txt
│
├── detection/
│   └── detector.py
│
├── teams/
│   └── team_classifier.py
│
├── formation/
│   └── formation_detector.py
│
├── phase/
│   └── phase_detector.py
│
├── visualization/
│   └── pitch_visualizer.py
│
├── input/
│   └── match_clip.mp4
│
├── output/
│   ├── analysed_match.mp4
│   ├── tactical_view.mp4
│   └── analysis.csv
│
└── data/
    └── SoccerNet/
```

The exact folder contents may vary slightly depending on the local setup.

---

# Installation and Setup

## Recommended Python Version

Use:

```text
Python 3.11 or Python 3.12
```

Check your installed version:

```powershell
python --version
```

---

## 1. Clone the Repository

```powershell
git clone https://github.com/YOUR_USERNAME/TactiG.git
```

Enter the project directory:

```powershell
cd TactiG
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install requirements:

```powershell
python -m pip install -r requirements.txt
```

If OpenCV is missing:

```powershell
python -m pip install opencv-python
```

---

# Preparing the Input Video

TactiG expects a video file.

The default example path used during development was:

```text
input\match_clip.mp4
```

If this file already exists, no frame-to-video conversion is required.

---

# Converting SoccerNet Frames to Video

If you only have SoccerNet JPG frames, create:

```text
frames_to_video.py
```

Use:

```python
import cv2
import os

frames_folder = r"data\SoccerNet\tracking\SNMOT-060\img1"
output_video = r"input\match_clip.mp4"

fps = 25

images = sorted(
    [img for img in os.listdir(frames_folder) if img.endswith(".jpg")]
)

first_frame = cv2.imread(
    os.path.join(frames_folder, images[0])
)

height, width, _ = first_frame.shape

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

video = cv2.VideoWriter(
    output_video,
    fourcc,
    fps,
    (width, height)
)

for image in images:
    frame = cv2.imread(
        os.path.join(frames_folder, image)
    )
    video.write(frame)

video.release()

print(f"Video created: {output_video}")
```

Run:

```powershell
python frames_to_video.py
```

The output should be:

```text
input\match_clip.mp4
```

---

# Running TactiG

Make sure the virtual environment is active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python main.py --video input\match_clip.mp4
```

The YOLO model may download automatically during the first run.

Processing time depends on:

- Video resolution
- Number of frames
- CPU/GPU availability
- YOLO model size

---

# Output Files

Results are written to:

```text
output/
```

## `analysed_match.mp4`

The original football footage with analysis overlays such as:

- Detected players
- Tracking information
- Team labels
- Formation information
- Tactical information

---

## `tactical_view.mp4`

A simplified tactical/pitch representation of detected player positions.

This makes team structure easier to inspect than in the normal broadcast-camera view.

---

## `analysis.csv`

Contains frame-level or time-based numerical results generated by the analysis pipeline.

It can be used for:

- Formation-frequency analysis
- Tactical-phase analysis
- Visualisation
- Statistical analysis

---

# Re-running the Project

If the `output` folder already contains previous results and you want to preserve them:

```powershell
Rename-Item output output_old
```

Create a fresh output folder:

```powershell
New-Item -ItemType Directory output
```

Then run:

```powershell
python main.py --video input\match_clip.mp4
```

---

# Daily Startup

After the project has already been installed, you only need:

```powershell
cd "PATH_TO_TactiG_Project"
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python main.py --video input\match_clip.mp4
```

You do not need to reinstall dependencies every time.

---

# Limitations

TactiG is an academic prototype.

Current limitations may include:

- Missed player detections
- Occasional tracking-ID changes
- Referee/goalkeeper confusion during team classification
- Similar jersey colours between teams
- Camera perspective distortion
- Camera movement and zoom
- Partial player visibility
- Unreliable ball detection in some frames
- Formation changes during transitions
- Formation estimates based only on visible players
- Broad rather than professional-level tactical-phase classification

Formation output should therefore be interpreted as an estimate of the visible tactical structure.

---

# Possible Future Improvements

Possible extensions include:

- Homography-based image-to-pitch transformation
- Improved goalkeeper/referee classification
- Improved ball tracking
- Temporal smoothing of formation predictions
- Deep-learning formation classification
- Graph Neural Networks for tactical recognition
- Player-role recognition
- Possession recognition
- Pressing-intensity estimation
- Defensive-line detection
- Pass-network analysis
- Automatic event recognition

---

# Academic Relevance

| Pattern Recognition Concept | Use in TactiG |
|---|---|
| Feature Extraction | Player coordinates, colour features, distances and spatial structure |
| Clustering | Jersey/team separation |
| Normalisation | Relative player-coordinate representation |
| Spatial Pattern Recognition | Formation recognition |
| Graph Representation | Player spatial relationships |
| Classification | Formation and tactical-phase labels |
| Sequential Analysis | Consecutive football frames |
| Computer Vision | Provides detections and tracking observations |

YOLO mainly provides the object detections.

The Pattern Recognition component begins when those detections are converted into useful appearance-based and spatial features and are used to recognise team structure.

---

# Suggested Viva Explanation

If asked:

> **Where is Pattern Recognition used in TactiG?**

You can answer:

> TactiG first uses YOLO and ByteTrack to detect and track football players. These detections are converted into features such as player coordinates, relative spacing and jersey-colour information. Clustering is used to separate the two teams, while normalised player coordinates and spatial relationships are used to recognise team formations. Because football organisation changes continuously over consecutive frames, sequential analysis is also used to classify broad tactical phases such as attacking, defending and transition.

---

# Short Project Description

**TactiG: Football Formation Recognition using Graph Patterns and Clustering**

TactiG is a football-video analysis system that combines object detection, multi-object tracking, clustering and spatial Pattern Recognition. Players are detected using YOLO and tracked using ByteTrack. Jersey-colour features are used to separate teams, after which player positions are converted into a normalised tactical representation. Spatial player arrangements are analysed to estimate football formations and broad tactical phases.

The system produces:

- An annotated match video
- A tactical-view video
- CSV-based analysis results

---

# Disclaimer

TactiG is an academic Pattern Recognition prototype and is not intended to replace professional football tracking systems or commercial tactical-analysis platforms.
