# Real-Time Traffic Analytics

A modular computer vision project for analyzing road traffic from video using YOLO, ByteTrack, OpenCV, and Supervision.

The system currently supports vehicle detection, multi-object tracking, line-crossing counts, live traffic statistics, simple congestion estimation, traffic-flow estimation, and relative vehicle speed estimation.

## Features

- **Vehicle Detection** — Detects selected vehicle classes using a YOLO model.
- **Multi-Object Tracking** — Uses ByteTrack to assign persistent IDs to vehicles.
- **Readable Vehicle Labels** — Displays tracker ID and vehicle class name.
- **Line Crossing Count** — Counts vehicles crossing a configurable line in `IN` and `OUT` directions.
- **Separate Live Dashboard** — Keeps analytics separate from the video display.
- **Vehicle Class Statistics** — Shows currently visible vehicles by class.
- **Congestion Estimation** — Classifies traffic as `Low`, `Medium`, or `High`.
- **Traffic Flow** — Calculates vehicles/minute and an estimated vehicles/hour rate.
- **Relative Speed** — Estimates tracked vehicle motion in pixels/second (`px/s`).

## Current Pipeline

```text
Input Video
    |
    v
YOLO Vehicle Detection
    |
    v
ByteTrack Tracking
    |
    +--------------------+
    |                    |
    v                    v
Line Crossing       Relative Speed
    |                  (px/s)
    v
IN / OUT Counts
    |
    v
Traffic Flow
    |
    v
Live Dashboard
```

## Project Structure

```text
real-time-traffic-analytics/
├── assets/
│   └── traffic-analysis-demo.png
|
|-- app/
|   |-- analytics/
|   |   |-- congestion.py
|   |   |-- dashboard.py
|   |   |-- flow.py
|   |   |-- line_counter.py
|   |   `-- speed_estimator.py
|   |
|   |-- detection/
|   |   `-- yolo_detector.py
|   |
|   |-- tracking/
|   |   `-- byte_tracker.py
|   |
|   |-- utils/
|   |   `-- config_loader.py
|   |
|   `-- video_processor.py
|
|-- main.py
|-- requirements.txt
`-- README.md
```

> The exact local structure may vary slightly depending on configuration and data folders.

## How It Works

### 1. Vehicle Detection

`YOLOVehicleDetector` loads a YOLO model and detects the configured vehicle classes.

For a standard COCO-trained YOLO model, commonly used traffic classes include:

```text
2 = car
3 = motorcycle
5 = bus
7 = truck
```

The detector exposes readable class names for labels such as `car`, `bus`, and `motorcycle`.

### 2. Multi-Object Tracking

ByteTrack assigns a persistent `tracker_id` to each detected vehicle.

Example:

```text
ID 12 | car
ID 18 | motorcycle
ID 25 | bus
```

Tracking allows the same vehicle to be followed across multiple frames.

### 3. Line Crossing

A configurable counting line is created using Supervision's `LineZone`.

When a tracked vehicle crosses the line, the system updates cumulative:

```text
IN
OUT
```

These counts are different from the number of vehicles currently visible in a frame.

### 4. Live Vehicle Statistics

The dashboard counts the vehicle classes currently visible.

Example:

```text
Vehicles in scene: 14

Car: 8
Motorcycle: 4
Bus: 2
```

### 5. Congestion Estimation

The current implementation uses a simple threshold-based heuristic:

```text
0-10 vehicles   -> Low
11-20 vehicles  -> Medium
21+ vehicles    -> High
```

This is an initial approach. A future version can use road occupancy, lane information, speed, or a region of interest.

### 6. Traffic Flow

Traffic flow is calculated from line-crossing events and video timestamps.

The system uses video time rather than computer processing time:

```python
video_time_seconds = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
```

During the first 60 seconds, crossings are normalized to a per-minute rate. After 60 seconds, the system uses a rolling 60-second window.

Example:

```text
Flow: 12 veh/min
Hourly rate: 720 veh/hr
```

The hourly value is an extrapolated rate based on the current flow rate.

### 7. Relative Speed Estimation

Relative speed is estimated from the movement of each tracked vehicle's bounding-box center between frames:

```text
relative speed = pixel distance travelled / elapsed video time
```

The result is displayed in pixels per second:

```text
ID 12 | car | 184.3 px/s
```

This is **not real-world speed in km/h**. Camera perspective affects pixel-based motion, so the value should be treated as relative image speed.

## Dashboard

The application uses two OpenCV windows.
## Demo

<p align="center">
  <img src="assets/traffic-analytics-demo.png"
       alt="Real-Time Traffic Analytics Demo"
       width="800">
</p>

### Traffic Analytics Window

Displays:

- video
- detection boxes
- tracker IDs
- vehicle class names
- counting line
- relative speed

### Dashboard Window

Displays:

- vehicles currently in the scene
- vehicle counts by class
- traffic congestion level
- cumulative `IN` and `OUT` counts
- vehicles per minute
- estimated vehicles per hour

Keeping the dashboard separate prevents analytics text from covering the video.

## Installation

Create and activate a Python environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

Main libraries:

```text
ultralytics
opencv-python
supervision
numpy
```

## Running the Project

Configure the model path, input/output video paths, confidence threshold, selected vehicle classes, and counting line in your project configuration.

Then run:

```bash
python main.py
```

Press `q` to stop processing.

## Current Limitations

- A standard COCO model does not contain Bangladesh-specific classes such as rickshaw or CNG/auto-rickshaw.
- Congestion estimation currently uses simple vehicle-count thresholds.
- Relative speed is measured in `px/s`, not `km/h`.
- Perspective distortion affects pixel-based speed comparisons.
- Detection and tracking quality depend on the model and video conditions.

## Planned Improvements

- Fine-tune a Bangladesh-specific traffic detector.
- Add classes such as rickshaw, CNG/auto-rickshaw, minibus, and other local vehicle types.
- Smooth relative speed estimates across multiple frames.
- Add calibrated real-world speed estimation.
- Add lane-wise analytics.
- Improve congestion estimation using occupancy and speed.
- Add traffic heatmaps.
- Build a professional desktop or web monitoring interface.
- Store analytics for historical analysis and visualization.

## Technologies

- Python
- OpenCV
- Ultralytics YOLO
- ByteTrack
- Supervision
- NumPy

## Status

This project is under active development and currently provides a modular foundation for an intelligent traffic monitoring system.
