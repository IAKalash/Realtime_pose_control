# Real-time Pose Tiredness Detection

## Task Description
Implement a real-time pose control system to detect tiredness based on shoulder position.  
Integrates external modules from **CV-2-31** (upper body pose detection using MediaPipe) and **CV-2-11** (person detection via face tracking with Haar cascades).  
The system processes video frames from webcam or file, detects a person (via face), identifies key pose points (face, shoulders), tracks their positions, and classifies the pose as 'Tired' if shoulders are lowered relative to the face. Outputs the status and visualizes keypoints.

> **IMPORTANT NOTE:**  
> In the `detect_tiredness` function, all checks and validations have been intentionally removed to maximize performance for real-time use. It is assumed that input arguments (e.g., frame) are pre-validated outside the function. Always preprocess inputs in your calling code to avoid errors.  
> Additionally, the `threshold` parameter must be tuned based on camera distance: the greater the distance to the subject, the smaller the threshold value should be (due to perspective compression reducing the apparent y-delta between face and shoulders).

## Features 
- **Pose Detection:** Leverages MediaPipe from CV-2-31 for upper body keypoints (face center, shoulders).  
- **Tiredness Classification:** Simple threshold-based check: if average shoulder y-coordinate < face y-coordinate + (threshold * image height), classify as 'Tired'.  
- **Real-time Processing:** Optimized for video streams (webcam or file) with minimal overhead.    
- **Flexible Input:** Supports webcam or video files (e.g., MP4).  
- **No Error Handling in Core Function:** For speed; handle externally.  
- **Parameterization:** Adjustable threshold for tiredness sensitivity.

## Functions

### `detect_tiredness(frame, pose_detector, threshold=0.2)`
Processes a single video frame to detect and classify tiredness based on pose.

**Parameters:**
- `frame` (np.ndarray): Input video frame (BGR format from cv2). 
- `pose_detector` (object): Pre-initialized MediaPipe pose detector (from CV-2-31).
- `threshold` (float, optional): Normalized threshold for detecting lowered shoulders (default: 0.2). Tune based on distance: smaller for farther subjects.  

**Returns:**
- `str`: 'Tired' if shoulders are lowered, 'OK' otherwise, or 'No person' if no pose detected.

**Notes:**  
- Assumes pre-validation of inputs for performance.  
- Integrates CV-2-31 functions like `detect_pose_landmarks`, `calculate_face_center_point`, etc., without modification.

### `main()`
Demonstration script for running the system on webcam or sample videos.

**Features:**
- Interactive input for source selection (webcam or predefined samples).  
- Initializes pose detector.  
- Processes frames in a loop, prints status, and displays visualized output.  

## Running the Demo
```bash
python pose_tiredness_control.py
```

**Example Input/Output:**
```bash
0 - webcam; 1,2 - video samples
0
# (Opens webcam window with visualized pose and status printed to console, e.g.)
OK
OK
Tired
No person
# Press 'q' to exit
```

Result: Real-time window ('Pose Control') showing frame with green pose landmarks. Status printed per frame. For videos, processes until end.

## Adjustable Parameters
The detection accuracy depends on tuning these parameters:

| Parameter | Typical Values | Description |
|------------|----------------|--------------|
| `threshold` | 0.1–0.3 | Tiredness sensitivity: y-delta for shoulders vs. face (normalized to image height). Lower for distant subjects to account for perspective. |
| MediaPipe `model_complexity` (in CV-2-31 init) | 0–2 | Balance speed vs. accuracy: 0 for faster RT, 1 default, 2 for precision (edit in imported module if needed). |

> **Note:** Test on sample videos to calibrate. Threshold impacts false positives/negatives based on camera angle/distance.

## Dependencies
- `opencv-python` (for video capture, processing, and visualization).  
- `mediapipe` (for pose detection, from CV-2-31).
- `numpy` (from CV-2-31)
- `pathlib` (from CV-2-31)
- `scikit-image` (from CV-2-31)

Install dependencies:
```bash
pip install -r requirements.txt
```

**Notes:**  
- Assumes CV_2_31.py (from linked repo) is in the project directory or import path.

## Implementation Details
- Imports CV-2-31 as `pose` and uses its functions (e.g., `detect_pose_landmarks`, `calculate_shoulders_center`) without modification for upper body pose (focus on head, shoulders, elbows, wrists).  
- Tiredness logic: Computes centers from landmarks, compares y-coordinates (y increases downward in images).  
- Optimized for RT: No internal checks in core function; init detector once in main.  
- Supports BGR frames; draws green custom connections (shoulders to elbows/wrists).  
- Tested on webcam and sample MP4 videos (e.g., people sitting/standing).

## Materials 
- [CV-2-31: Pose Detection Repo](https://github.com/Pozovi23/CV-2-31)  

---
*Developed and tested on sample videos with varying poses and distances.*