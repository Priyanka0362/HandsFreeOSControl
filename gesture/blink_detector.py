import time


class BlinkDetector:

    def __init__(self):

        # Previous eye state
        self.previous_state = False

        # Time when eye first closed
        self.eye_closed_start = None

        # Last valid blink
        self.last_blink_time = 0

        # ----------------------------
        # Blink Timing
        # ----------------------------

        # Blink must last at least 100 ms
        self.minimum_blink_duration = 0.10

        # Ignore if eye closed too long
        self.maximum_blink_duration = 0.40

        # Ignore repeated blinks for 300 ms
        self.debounce_time = 0.20

        # Extra cooldown after a valid blink
        self.cooldown_time = 0.10

    def update(self, eye_closed):

        current_time = time.time()

        blink_detected = False

        # ----------------------------
        # Eye just closed
        # ----------------------------
        if eye_closed and not self.previous_state:

            self.eye_closed_start = current_time

        # ----------------------------
        # Eye just opened
        # ----------------------------
        elif (
            self.previous_state
            and not eye_closed
            and self.eye_closed_start is not None
        ):

            blink_duration = current_time - self.eye_closed_start

            enough_time = (
                current_time - self.last_blink_time
                >= self.debounce_time + self.cooldown_time
            )

            valid_duration = (
                self.minimum_blink_duration
                <= blink_duration
                <= self.maximum_blink_duration
            )

            if valid_duration and enough_time:

                blink_detected = True
                self.last_blink_time = current_time

            # Reset timer
            self.eye_closed_start = None

        # Save eye state
        self.previous_state = eye_closed

        return blink_detected