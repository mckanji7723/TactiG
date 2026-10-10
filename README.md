# TactiG

**Football Formation Recognition and Tactical Phase Analysis using Pattern Recognition**

TactiG is a computer-vision and Pattern Recognition project for analysing football match footage. The system detects and tracks players from video, separates them into teams using visual appearance, converts their positions into spatial representations, estimates team formations, identifies broad tactical phases, and generates annotated output videos and CSV analysis.

The project was developed as a Pattern Recognition course project and is intended for academic and demonstration purposes.

---

## Project Objective

The main objective of TactiG is to recognise tactical structure from football video.

The processing pipeline is:
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

Instead of analysing only individual players, TactiG focuses on the spatial pattern formed by the team as a whole.
Main Features
- Player and ball detection using YOLO
- Multi-object tracking using ByteTrack
- Team separation using jersey-colour features and clustering
- Player-position extraction from video frames
- Normalised player-coordinate representation
- Football formation recognition
- Tactical phase recognition
- Annotated match-video generation
- Tactical top-down/pitch-view generation
- Frame-level analysis stored in CSV
- SoccerNet Tracking dataset support
Example formations include:
- 4-3-3
- 4-4-2
- 4-2-3-1
- 3-5-2
Broad tactical phases include:
- Attacking
- Defending
- Transition
Pattern Recognition Concepts Used
1. Feature Extraction
The raw video is not directly used for formation classification.
First, useful features are extracted from detected players.
Examples include:
Player x-position
Player y-position
Team label
Relative player spacing
Horizontal spread
Vertical spread
Distances between players
Player-group structure

This converts raw image/video data into a numerical spatial representation.
2. Clustering
Clustering is used to separate detected players into teams based on jersey appearance.
Conceptually:
Detected player crops
        ↓
Colour features
        ↓
Clustering
        ↓
Team A / Team B

This is an example of unsupervised Pattern Recognition.
3. Spatial Pattern Recognition
A football formation is fundamentally a spatial pattern.
For example:
4 defenders
3 midfielders
3 attackers

creates a different spatial arrangement from:
4 defenders
4 midfielders
2 attackers

TactiG analyses the arrangement of multiple players rather than only individual detections.
4. Coordinate Normalisation
Player locations depend on camera position, zoom and image resolution.
To compare formations more consistently, detected positions are converted into relative/normalised coordinates.
Pixel coordinates
      ↓
Normalisation
      ↓
Relative tactical coordinates

This reduces the effect of raw image scale.
5. Graph-style Player Relationships
Players can be represented as nodes in a spatial graph.
Player = Node
Spatial relation / distance = Edge

For example:
P1 ---- P2 ---- P3
|       |        |
P4 ---- P5 ---- P6

The structure of these player relationships provides information about the team's tactical shape.
This graph-based interpretation is the reason for the name:
TactiG = Tactical + Graph

6. Formation Classification
After the player-position features are extracted, the spatial arrangement is compared with expected football formation structures.
Possible output classes include:
4-3-3
4-4-2
4-2-3-1
3-5-2

The system estimates which formation most closely matches the current player configuration.
7. Sequential Pattern Recognition
Football tactics change over time.
Therefore, formation and phase analysis is performed over consecutive frames:
Frame t
  ↓
Frame t+1
  ↓
Frame t+2
  ↓
...

The temporal ordering of frames is important.
This connects TactiG with Sequential Pattern Recognition.
8. Tactical Phase Recognition
After player positions and team structure are obtained, the system assigns a broad tactical phase such as:
Attacking
Defending
Transition

This is a higher-level classification task built on top of detection, tracking and spatial Pattern Recognition.
Technologies Used
Component	Technology
Programming Language	Python
Object Detection	YOLO / Ultralytics
Tracking	ByteTrack
Computer Vision	OpenCV
Numerical Processing	NumPy
Data Processing	Pandas
Team Separation	Jersey-colour features + clustering
Pattern Recognition	Spatial features and formation matching
Dataset	SoccerNet Tracking
Outputs	MP4 + CSV


Dataset
The project was tested with the SoccerNet Tracking dataset.
One sequence used during development was:
SNMOT-060

Sequence information:
Frame rate: 25 FPS
Resolution: 1920 × 1080
Number of frames: 750

The dataset stores the sequence as individual JPG frames.
Example:
SNMOT-060/
└── img1/
    ├── 000001.jpg
    ├── 000002.jpg
    ├── 000003.jpg
    └── ...

These frames were converted to an MP4 video before analysis.
Project Structure
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

The exact local folder structure may vary slightly.
Installation
Recommended Python Version
Use:
Python 3.11 or Python 3.12

Check:
python --version

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/TactiG.git

Then:
cd TactiG

2. Create a Virtual Environment
python -m venv .venv

Activate:
.\.venv\Scripts\Activate.ps1

If PowerShell blocks activation:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then:
.\.venv\Scripts\Activate.ps1

3. Install Dependencies
python -m pip install --upgrade pip

Then:
python -m pip install -r requirements.txt

If OpenCV is missing:
python -m pip install opencv-python

Preparing the Input Video
TactiG expects a video such as:
input\match_clip.mp4

If this file already exists, no conversion is needed.
Converting SoccerNet Frames to Video
If you only have SoccerNet image frames, create:
frames_to_video.py

Use:
import cv2import osframes_folder = r"data\SoccerNet\tracking\SNMOT-060\img1"output_video = r"input\match_clip.mp4"fps = 25images = sorted(    [img for img in os.listdir(frames_folder) if img.endswith(".jpg")])first_frame = cv2.imread(    os.path.join(frames_folder, images[0]))height, width, _ = first_frame.shapefourcc = cv2.VideoWriter_fourcc(*"mp4v")video = cv2.VideoWriter(    output_video,    fourcc,    fps,    (width, height))for image in images:    frame = cv2.imread(        os.path.join(frames_folder, image)    )    video.write(frame)video.release()print(f"Video created: {output_video}")


Run:
python frames_to_video.py

The output will be:
input\match_clip.mp4

Running the Project
Activate the virtual environment:
.\.venv\Scripts\Activate.ps1

Run:
python main.py --video input\match_clip.mp4

The YOLO model may download automatically on the first run.
Processing time depends on:
- video resolution
- number of frames
- CPU/GPU availability
- YOLO model size
Output Files
TactiG creates output files inside:
output/

analysed_match.mp4
The original match footage with analysis overlays such as:
- detected players
- tracking information
- team labels
- formation information
- tactical information
tactical_view.mp4
A simplified tactical representation of the detected player positions.
This makes the team shape easier to inspect than the broadcast camera view.
analysis.csv
Contains frame-level or time-based numerical analysis.
It can be used for:
- formation-frequency analysis
- tactical-phase analysis
- visualisation
- statistical analysis
Re-running the Project
If you want to preserve the existing output:
Rename-Item output output_old

Create a new output folder:
New-Item -ItemType Directory output

Then run again:
python main.py --video input\match_clip.mp4

Daily Startup
After setup, you only need:
cd "PATH_TO_TactiG_Project"

.\.venv\Scripts\Activate.ps1

python main.py --video input\match_clip.mp4

Dependencies do not need to be reinstalled each time.
Limitations
TactiG is an academic prototype.
Current limitations may include:
- missed player detections
- tracking-ID changes
- referee/goalkeeper confusion
- similar jersey colours between teams
- camera perspective distortion
- camera movement and zoom
- partial player visibility
- unreliable ball detection
- formation changes during transitions
- incomplete visibility of all 11 players
- broad tactical-phase classification
Formation output should therefore be interpreted as an estimate of the visible tactical structure.
Possible Future Improvements
Possible future improvements include:
- homography-based image-to-pitch transformation
- improved goalkeeper/referee classification
- more robust ball tracking
- temporal smoothing of formation predictions
- deep-learning formation classifier
- Graph Neural Networks
- player-role recognition
- possession recognition
- pressing-intensity estimation
- defensive-line detection
- pass-network analysis
- automated event recognition
Academic Relevance
Pattern Recognition Topic	Use in TactiG
Feature Extraction	Player coordinates, colours, distances and spatial structure
Clustering	Team separation
Normalisation	Relative player positions
Spatial Pattern Recognition	Formation recognition
Graph Representation	Player spatial relationships
Classification	Formation and phase labels
Sequential Recognition	Analysis across consecutive frames
Computer Vision	Provides detections and tracking observations


YOLO itself mainly provides object detection.
The core Pattern Recognition component begins when those detections are converted into appearance-based and spatial features and used to recognise team structure.
