import pyautogui


class HeadTracker:

    def __init__(self):

        self.filtered_dy = 0.0

        # -----------------------------
        # Screen Size
        # -----------------------------
        self.screen_width, self.screen_height = pyautogui.size()

        # MediaPipe Nose Landmark
        self.NOSE_TIP = 1

        # -----------------------------
        # Calibration
        # -----------------------------
        self.center_x = None
        self.center_y = None

        # -----------------------------
        # Cursor State
        # -----------------------------
        self.previous_x = self.screen_width // 2
        self.previous_y = self.screen_height // 2

        # -----------------------------
        # Adaptive Cursor Smoothing
        # -----------------------------
        self.min_smoothing = 0.10
        self.max_smoothing = 0.35

        # -----------------------------
        # Adaptive Cursor Sensitivity
        # -----------------------------
        self.low_sensitivity = 2200
        self.medium_sensitivity = 3000
        self.high_sensitivity = 4200

        # -----------------------------
        # Dead Zone
        # -----------------------------
        self.dead_zone = 0.005

    def get_nose_position(self, landmarks):

        nose = landmarks[self.NOSE_TIP]

        return nose.x, nose.y

    def calibrate(self, nose_x, nose_y):

        self.center_x = nose_x
        self.center_y = nose_y

        print("=" * 40)
        print(" Calibration Complete")
        print(f" Center = ({nose_x:.3f}, {nose_y:.3f})")
        print("=" * 40)

    def get_screen_position(self, nose_x, nose_y):
    

        # Wait until calibration
        if self.center_x is None:
            return self.previous_x, self.previous_y

        # ---------------------------------
        # Relative Head Movement
        # ---------------------------------
        dx = nose_x - self.center_x
        dy = nose_y - self.center_y

        # ---------------------------------
        # Vertical Motion Filtering
        # ---------------------------------
        alpha = 0.20

        self.filtered_dy = (
            alpha * dy
            + (1 - alpha) * self.filtered_dy
        )

        dy = self.filtered_dy

        # ---------------------------------
        # Dead Zone
        # ---------------------------------
        if abs(dx) < self.dead_zone:
            dx = 0

        if abs(dy) < self.dead_zone:
            dy = 0

        # ---------------------------------
        # Adaptive Sensitivity
        # ---------------------------------
        movement = max(abs(dx), abs(dy))

        if movement < 0.02:

            sensitivity = self.low_sensitivity
            smoothing = self.min_smoothing

        elif movement < 0.05:

            sensitivity = self.medium_sensitivity
            smoothing = 0.20

        else:

            sensitivity = self.high_sensitivity
            smoothing = self.max_smoothing

        # ---------------------------------
        # Convert to Screen Position
        # ---------------------------------
        target_x = (
            self.screen_width // 2
            + int(dx * sensitivity)
        )

        # Head Up -> Cursor Up
        target_y = (
            self.screen_height // 2
            - int(dy * sensitivity)
        )

        # ---------------------------------
        # Keep Cursor on Screen
        # ---------------------------------
        target_x = max(0, min(target_x, self.screen_width - 1))
        target_y = max(0, min(target_y, self.screen_height - 1))

        # ---------------------------------
        # Adaptive Cursor Smoothing
        # ---------------------------------
        smooth_x = int(
            self.previous_x
            + (target_x - self.previous_x) * smoothing
        )

        smooth_y = int(
            self.previous_y
            + (target_y - self.previous_y) * smoothing
        )

        self.previous_x = smooth_x
        self.previous_y = smooth_y

        return smooth_x, smooth_y