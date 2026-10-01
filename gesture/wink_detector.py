import time


class WinkDetector:

    def __init__(self):

        # EAR difference required to classify a wink
        self.left_difference = 0.10
        self.right_difference = 0.05

        # Previous eye states
        self.left_previous = False
        self.right_previous = False

        # When eye first closed
        self.left_closed_start = None
        self.right_closed_start = None

        # Last detected wink time
        self.last_left_wink = 0
        self.last_right_wink = 0

        # Timing
        self.minimum_duration = 0.15
        self.maximum_duration = 0.60
        self.debounce_time = 0.40

    def detect(
        self,
        left_ear,
        right_ear,
        blink_threshold
    ):

        current_time = time.time()

        gesture = None

        # ------------------------------------
        # EAR Difference
        # ------------------------------------

        left_difference = right_ear - left_ear
        right_difference = left_ear - right_ear

        # ------------------------------------
        # Eye States
        # ------------------------------------

        left_closed = (
            left_ear < blink_threshold
            and left_difference > self.left_difference
        )

        right_closed = (
            right_ear < blink_threshold
            and right_difference > self.right_difference
        )

        # ====================================
        # LEFT WINK
        # ====================================

        if (
            left_closed
            and not self.left_previous
            and not right_closed
        ):

            self.left_closed_start = current_time

        elif (
            self.left_previous
            and not left_closed
            and self.left_closed_start is not None
        ):

            duration = current_time - self.left_closed_start

            if (
                self.minimum_duration <= duration <= self.maximum_duration
                and current_time - self.last_left_wink >= self.debounce_time
            ):

                gesture = "LEFT_WINK"
                self.last_left_wink = current_time

            self.left_closed_start = None

        # ====================================
        # RIGHT WINK
        # ====================================

        if (
            right_closed
            and not self.right_previous
            and not left_closed
        ):

            self.right_closed_start = current_time

        elif (
            self.right_previous
            and not right_closed
            and self.right_closed_start is not None
        ):

            duration = current_time - self.right_closed_start

            if (
                self.minimum_duration <= duration <= self.maximum_duration
                and current_time - self.last_right_wink >= self.debounce_time
            ):

                gesture = "RIGHT_WINK"
                self.last_right_wink = current_time

            self.right_closed_start = None

        # ====================================
        # BOTH CLOSED
        # ====================================

        if left_closed and right_closed:
            gesture = None

        # Save current state

        self.left_previous = left_closed
        self.right_previous = right_closed

        return gesture