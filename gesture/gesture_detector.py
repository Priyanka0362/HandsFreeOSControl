import time


class GestureDetector:

    def __init__(self):

        # Number of blinks collected
        self.blink_count = 0

        # Time of first blink in current sequence
        self.first_blink_time = None

        # Time window to collect multiple blinks
        self.window = 0.55

    def update(self, blink_detected):

        current_time = time.time()

        # -----------------------------
        # New blink event
        # -----------------------------
        if blink_detected:

            if self.blink_count == 0:
                self.first_blink_time = current_time

            self.blink_count += 1

        # Nothing to process
        if self.blink_count == 0:
            return None

        # Still waiting for another blink
        if current_time - self.first_blink_time < self.window:
            return None

        # Decide gesture
        if self.blink_count == 1:
            gesture = None

        elif self.blink_count >= 2:
            gesture = "DOUBLE_BLINK"

       

        # Reset
        self.blink_count = 0
        self.first_blink_time = None

        return gesture