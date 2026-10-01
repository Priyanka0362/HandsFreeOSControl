import cv2
import time

from camera.camera import Camera
from vision.face_mesh import FaceMeshDetector
from vision.eye_tracker import EyeTracker

from tracking.head_tracker import HeadTracker

from gesture.blink_detector import BlinkDetector
from gesture.gesture_detector import GestureDetector

from controller.mouse_controller import MouseController
from gesture.wink_detector import WinkDetector

# ==========================================================
# Initialize Modules
# ==========================================================

camera = Camera()

face_detector = FaceMeshDetector()

eye_tracker = EyeTracker()

head_tracker = HeadTracker()

blink_detector = BlinkDetector()

gesture_detector = GestureDetector()

wink_detector = WinkDetector()

# Safe Mode
# False = only print gestures
# True = actually control mouse
mouse_controller = MouseController(enabled=True)
# ---------------------------------
# Gesture Notificationc
# ---------------------------------

notification = ""
notification_time = 0
notification_duration = 1.0

# ---------------------------------
# Calibration Status
# ---------------------------------

calibration_message = "PRESS C TO CALIBRATE"
calibration_time = 0
calibration_duration = 2.0

# ---------------------------------
# FPS Counter
# ---------------------------------

previous_time = time.time()
fps = 0

# ---------------------------------
# Startup Help
# ---------------------------------

start_time = time.time()
help_duration = 5

# ---------------------------------
# Face Tracking Status
# ---------------------------------

face_visible = False

print("Press 'Q' to Exit")


# ==========================================================
# Main Loop
# ==========================================================

while True:

    frame = camera.get_frame()

    # ---------------------------------
    # FPS Calculation
    # ---------------------------------

    current_time = time.time()

    fps = 1 / (current_time - previous_time)

    previous_time = current_time

    if frame is None:
        break

    # ------------------------------------------------------
    # Face Detection
    # ------------------------------------------------------

    results = face_detector.detect(frame)

    face_visible = bool(results.face_landmarks)

    if face_visible:

        landmarks = results.face_landmarks[0]

        # --------------------------------------------------
        # Face Information
        # --------------------------------------------------

        total_landmarks = len(landmarks)
        # --------------------------------------------------
        # Head Tracking
        # --------------------------------------------------

        nose_x, nose_y = head_tracker.get_nose_position(landmarks)

        screen_x, screen_y = head_tracker.get_screen_position(
            nose_x,
            nose_y
        )

        # --------------------------------------------------
        # Eye Tracking
        # --------------------------------------------------

        left_eye, right_eye = eye_tracker.get_eye_points(landmarks)

        frame = eye_tracker.draw_eye_points(
            frame,
            left_eye,
            right_eye
        )

       # --------------------------------------------------
       # EAR Calculation
       # --------------------------------------------------

        left_ear = eye_tracker.eye_aspect_ratio(left_eye)

        right_ear = eye_tracker.eye_aspect_ratio(right_eye)

        # Average EAR
        ear = (left_ear + right_ear) / 2

        # ------------------------------------------
        # Automatic Blink Calibration
        # ------------------------------------------

        if not eye_tracker.calibrated:
            eye_tracker.calibrate_blink(ear)
            eye_closed = False
        else:
            eye_closed = eye_tracker.is_blinking(ear)
        # --------------------------------------------------
        # Wink Detection
        # --------------------------------------------------

        wink = (
            wink_detector.detect(
                left_ear,
                right_ear,
                eye_tracker.blink_threshold
            )
            if eye_tracker.calibrated
            else None
        )

        if wink == "LEFT_WINK":

            print(wink)

            notification = "LEFT CLICK"
            notification_time = time.time()

            mouse_controller.handle_gesture(wink)

        elif wink == "RIGHT_WINK":

            print(wink)

            notification = "RIGHT CLICK"
            notification_time = time.time()

            mouse_controller.handle_gesture(wink)
        # --------------------------------------------------
        # Blink Detection
        # --------------------------------------------------

        blink_detected = blink_detector.update(eye_closed)

        # --------------------------------------------------
        # Gesture Detection
        # --------------------------------------------------

        gesture = gesture_detector.update(blink_detected)

       # --------------------------------------------------
       # Mouse Control
       # --------------------------------------------------


        # --------------------------------------------------
        # Mouse Control
        # --------------------------------------------------

        if mouse_controller.scroll_mode:

            # Pause scrolling while both eyes are closed
            if not eye_closed:

                dy = nose_y - head_tracker.center_y

                mouse_controller.scroll(dy)

        else:

            mouse_controller.move_cursor(
                screen_x,
                screen_y
            )
        # --------------------------------------------------
        # Perform Gesture Actions
        # --------------------------------------------------

        if gesture == "DOUBLE_BLINK":

            print(gesture)

            mouse_controller.handle_gesture(gesture)

            notification = (
                "SCROLL MODE"
                if mouse_controller.scroll_mode
                else "CURSOR MODE"
            )

            notification_time = time.time()
        elif gesture == "LONG_BLINK":

            print(gesture)

            mouse_controller.handle_gesture(gesture)

            notification = (
                "CURSOR LOCKED"
                if mouse_controller.cursor_locked
                else "CURSOR UNLOCKED"
            )

            notification_time = time.time()
        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        eye_status = "CLOSED" if eye_closed else "OPEN"

        gesture_status = gesture if gesture else "WAITING"

        # ---------------------------------
        # Tracking Status
        # ---------------------------------

        tracking_status = "GOOD" if face_visible else "LOST"

        tracking_color = (
        (0, 255, 0)
        if face_visible
        else (0, 0, 255)
        )

        cv2.putText(
            frame,
            f"Tracking: {tracking_status}",
            (20, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            tracking_color,
            2
        )

        # --------------------------------------------------
        # Display Information
        # --------------------------------------------------

        cv2.putText(
            frame,
            f"Landmarks: {total_landmarks}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"EAR: {ear:.3f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Threshold: {eye_tracker.blink_threshold:.3f}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Eye: {eye_status}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Gesture: {gesture_status}",
            (20, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Nose: ({nose_x:.2f}, {nose_y:.2f})",
            (20, 255),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Cursor: ({screen_x}, {screen_y})",
            (20, 290),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )
        cv2.putText(
            frame,
            f"Dead Zone: {head_tracker.dead_zone:.3f}",
            (20, 360),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 200, 255),
            2
        )


        mode_color = (
            (0,165,255)
            if mouse_controller.scroll_mode
            else (0,255,0)
        )

        mode_text = (
        "SCROLL"
        if mouse_controller.scroll_mode
        else "CURSOR"
        )

        cv2.putText(
        frame,
        f"Mode: {mode_text}",
        (20, 325),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        mode_color,
        2
        )   

        cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (900, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
        )

    # ------------------------------------------------------
    # Show Frame
    # ------------------------------------------------------
    
    # ---------------------------------
    # Face Lost
    # ---------------------------------

    if not face_visible:

        cv2.putText(
            frame,
            "FACE LOST - LOOK AT CAMERA",
            (20, 400),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # ---------------------------------
    # Gesture Notification
    # ---------------------------------

    if time.time() - notification_time < notification_duration:

      cv2.rectangle(
        frame,
        (340, 20),
        (760, 75),
        (40, 40, 40),
        -1
    )

      cv2.putText(
        frame,
        notification,
        (360, 58),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )
   
    # ---------------------------------
    # Startup Instructions
    # ---------------------------------
    if time.time() - start_time < help_duration:
        cv2.rectangle(
            frame,
            (120, 80),
            (760, 360),
            (30, 30, 30),
            -1
        )

        instructions = [
            "Press C : Calibrate",
            "",
            "Left Wink    : Left Click",
            "Right Wink   : Right Click",
            "Double Blink : Scroll Mode",
            "Long Blink   : Cursor Lock",
            "",
            "Press Q : Exit"
        ]

        y = 120
        for text in instructions:
            cv2.putText(
                frame,
                text,
                (160, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )
            y += 35
    # ---------------------------------
    # Calibration Message
    # ---------------------------------

    if head_tracker.center_x is None:

        cv2.putText(
            frame,
            "PRESS C TO CALIBRATE",
            (20, 395),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    elif time.time() - calibration_time < calibration_duration:

        cv2.putText(
        frame,
        "CALIBRATION COMPLETE",
        (20, 395),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )
    # ==========================================================
    # Frame Rendering & Input Handling (Moved OUTSIDE the if-block)
    # ==========================================================
    cv2.imshow("Hands-Free OS Control Engine", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("c") and face_visible:

        head_tracker.calibrate(
            nose_x,
            nose_y
        )

        calibration_message = "CALIBRATION COMPLETE"
        calibration_time = time.time()

    if key == ord("q"):
        break

# Clean up window and camera resources after loop breaks
camera.release()
cv2.destroyAllWindows()