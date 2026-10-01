# Hands-Free OS Control Engine

A computer vision-based hands-free operating system controller that enables users to control the mouse using head movements and eye gestures without requiring a physical mouse.

---

## Features

### Cursor Control
- Head-controlled mouse cursor
- Adaptive cursor sensitivity
- Adaptive cursor smoothing
- Dead-zone filtering for stable cursor movement

### Eye Gesture Control
- Left Wink → Left Click
- Right Wink → Right Click
- Double Blink → Toggle Scroll Mode
- Long Blink → Lock/Unlock Cursor

### Smart Scrolling
- Adaptive scrolling speed
- Scroll using vertical head movement
- Pause scrolling when both eyes are closed
- Adjustable scroll sensitivity

### Face Tracking
- Real-time face landmark detection using MediaPipe
- Automatic blink calibration
- Face loss detection
- Manual calibration using keyboard

### User Interface
- Live FPS counter
- EAR (Eye Aspect Ratio) display
- Blink threshold display
- Cursor coordinates
- Nose coordinates
- Current interaction mode
- Gesture notifications
- Face tracking status
- Calibration assistant

### Safety Features
- Safe Mode (prints actions without controlling the mouse)
- Real Mode (actual mouse control)
- Cursor boundary protection
- Cursor lock mode

---

## Technologies Used

- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

---

## Project Structure

```
HandsFreeOSControl/
│
├── camera/
│   └── camera.py
│
├── controller/
│   └── mouse_controller.py
│
├── gesture/
│   ├── blink_detector.py
│   ├── gesture_detector.py
│   └── wink_detector.py
│
├── tracking/
│   └── head_tracker.py
│
├── vision/
│   ├── eye_tracker.py
│   └── face_mesh.py
│
├── main.py
├── requirements.txt
├── README.md
└── PROJECT_JOURNAL.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

## Controls

| Gesture | Action |
|----------|--------|
| Move Head | Move Cursor |
| Left Wink | Left Click |
| Right Wink | Right Click |
| Double Blink | Toggle Scroll Mode |
| Long Blink | Lock/Unlock Cursor |
| Close Both Eyes | Pause Scrolling |
| C | Calibrate |
| Q | Quit |

---

## Current Status

### Completed

- Face Detection
- Eye Tracking
- Head Tracking
- Cursor Control
- Left Click
- Right Click
- Adaptive Cursor Smoothing
- Adaptive Sensitivity
- Scroll Mode
- Cursor Lock
- Automatic Blink Calibration
- Face Lost Detection
- FPS Counter
- Gesture Notification
- Safe Mode
- Real Mode

---

## Future Enhancements

- Drag & Drop
- Volume Control
- Brightness Control
- Voice Commands
- Virtual Keyboard
- Multi-Monitor Support
- Custom Gesture Training
- AI-Based Gesture Personalization

---

## Authors

Priyanka Basappa Goranal

M.Tech Computer Science & Engineering

University Visvesvaraya College of Engineering (UVCE)

---

## License

This project is developed for academic and research purposes.