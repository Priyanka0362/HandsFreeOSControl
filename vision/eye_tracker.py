import cv2
from utils.math_utils import MathUtils


class EyeTracker:

    def __init__(self):

        # Default blink threshold
        self.blink_threshold = 0.36

        # Blink calibration
        self.calibration_ears = []
        self.calibrated = False

    # Important eye landmark indices
    LEFT_EYE = [
        33, 133, 160, 159, 158,
        157, 173, 246, 161, 163,
        144, 145, 153, 154, 155
    ]

    RIGHT_EYE = [
        362, 263, 387, 386, 385,
        384, 398, 466, 388, 390,
        373, 374, 380, 381, 382
    ]

    def get_eye_points(self, landmarks):

        left_eye = []
        right_eye = []

        # Left Eye
        for idx in self.LEFT_EYE:
            left_eye.append(landmarks[idx])

        # Right Eye
        for idx in self.RIGHT_EYE:
            right_eye.append(landmarks[idx])

        return left_eye, right_eye

    def draw_eye_points(self, frame, left_eye, right_eye):

        height, width, _ = frame.shape

        # Draw left eye points
        for point in left_eye:
            x = int(point.x * width)
            y = int(point.y * height)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # Draw right eye points
        for point in right_eye:
            x = int(point.x * width)
            y = int(point.y * height)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        return frame

    def eye_aspect_ratio(self, eye):

        # Vertical distances
        A = MathUtils.distance(eye[2], eye[10])
        B = MathUtils.distance(eye[3], eye[9])

        # Horizontal distance
        C = MathUtils.distance(eye[0], eye[1])

        # Avoid division by zero
        if C == 0:
            return 0

        ear = (A + B) / (2.0 * C)

        return ear

    def calibrate_blink(self, ear):

        self.calibration_ears.append(ear)

        # Collect approximately 60 frames
        if len(self.calibration_ears) >= 60:

            average = sum(self.calibration_ears) / len(self.calibration_ears)

            # Dynamic threshold
            self.blink_threshold = average * 0.65

            self.calibrated = True

            print("=" * 40)
            print(" Blink Calibration Complete")
            print(f" Average EAR : {average:.3f}")
            print(f" Threshold   : {self.blink_threshold:.3f}")
            print("=" * 40)

            self.calibration_ears.clear()

    def is_blinking(self, ear):

        return ear < self.blink_threshold