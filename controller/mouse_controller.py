import time
import pyautogui


class MouseController:

    def __init__(self, enabled=False):

        self.enabled = enabled

        # -----------------------------
        # Interaction Modes
        # -----------------------------
        self.scroll_mode = False
        self.cursor_locked = False

        # -----------------------------
        # Scroll Control
        # -----------------------------
        self.last_scroll_time = 0.0

        # Scroll every 200 ms
        self.scroll_interval = 0.20

        # Ignore tiny head movement
        self.scroll_dead_zone = 0.07

        pyautogui.FAILSAFE = True

    # =====================================================
    # Cursor Movement
    # =====================================================

    def move_cursor(self, x, y):

        if not self.enabled:
            return

        if self.cursor_locked:
            return

        screen_width, screen_height = pyautogui.size()

        x = max(0, min(x, screen_width - 1))
        y = max(0, min(y, screen_height - 1))

        pyautogui.moveTo(x, y, duration=0)

    # =====================================================
    # Scroll
    # =====================================================

    def scroll(self, dy):

        current_time = time.time()

        # Limit scroll rate
        if current_time - self.last_scroll_time < self.scroll_interval:
            return

        # Ignore tiny movements
        if abs(dy) < self.scroll_dead_zone:
            return

        self.last_scroll_time = current_time

        movement = abs(dy)

        # -----------------------------
        # Adaptive Scroll Speed
        # -----------------------------
        if movement < 0.10:
            amount = 20

        elif movement < 0.18:
            amount = 40

        elif movement < 0.28:
            amount = 60

        else:
            amount = 80

        # -----------------------------
        # SAFE MODE
        # -----------------------------
        if not self.enabled:

            direction = "UP" if dy < 0 else "DOWN"

            print(f"[SAFE MODE] Scroll {direction} ({amount})")

            return

        # -----------------------------
        # Real Scroll
        # -----------------------------
        if dy < 0:
            pyautogui.scroll(amount)
        else:
            pyautogui.scroll(-amount)

    # =====================================================
    # Gesture Handler
    # =====================================================

    def handle_gesture(self, gesture):

        if gesture == "LEFT_WINK":

            self.left_click()

        elif gesture == "RIGHT_WINK":

            self.right_click()

        elif gesture == "DOUBLE_BLINK":

            self.scroll_mode = not self.scroll_mode

            print(
                "Scroll Mode:",
                "ON" if self.scroll_mode else "OFF"
            )

        elif gesture == "LONG_BLINK":

            self.cursor_locked = not self.cursor_locked

            print(
                "Cursor:",
                "LOCKED" if self.cursor_locked else "UNLOCKED"
            )

    # =====================================================
    # Left Click
    # =====================================================

    def left_click(self):

        if not self.enabled:

            print("[SAFE MODE] LEFT CLICK")
            return

        pyautogui.click()

    # =====================================================
    # Right Click
    # =====================================================

    def right_click(self):

        if not self.enabled:

            print("[SAFE MODE] RIGHT CLICK")
            return

        pyautogui.rightClick()