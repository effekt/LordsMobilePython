import time
import numpy as np
from pynput.mouse import Button, Controller as MouseController
import pyautogui


class Controller:
    def __init__(self, window, vision):
        self.window = window
        self.mouse = MouseController()
        self.vision = vision

    def move_to(self, loc, clean_state=False):
        if clean_state:
            self.clean_state()
        for movement in self.movements[loc['screen']]:
            if movement == 'left':
                self.move_left()

    def click_point(self, loc):
        self.move_mouse(loc[0], loc[1])
        self.left_mouse_click()
        time.sleep(1.25)
        self.vision.refresh_frame()

    def move_mouse(self, x, y):
        def set_mouse_position(x, y):
            self.mouse.position = (int(x), int(y))

        def smooth_move_mouse(from_x, from_y, to_x, to_y, speed=3):
            steps = 5
            sleep_per_step = speed // steps
            x_delta = (to_x - from_x) / steps
            y_delta = (to_y - from_y) / steps
            for step in range(steps):
                new_x = x_delta * (step + 1) + from_x
                new_y = y_delta * (step + 1) + from_y
                set_mouse_position(new_x, new_y)
                time.sleep(sleep_per_step)

        return smooth_move_mouse(
            self.mouse.position[0],
            self.mouse.position[1],
            x,
            y
        )

    def left_mouse_click(self):
        self.mouse.click(Button.left, 1)

    def left_mouse_drag(self, start, end):
        x1, y1 = start
        x2, y2 = end
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, 1.5)
        time.sleep(2.25)

    def click_object(self, matches, offset=(0, 0)):
        if len(matches[1]) > 0:
            x = matches[1][0] + offset[0]
            y = matches[0][0] + offset[1]
            matches = np.array([np.delete(matches[0], 0), np.delete(matches[1], 0)])
            self.move_mouse(x, y)
            self.left_mouse_click()
            time.sleep(0.5)
        return matches

    def move_left(self, base=False):
        x = 400
        if base:
            x = 250
        self.left_mouse_drag((self.window.game['midx'], self.window.game['midy']),
                             (self.window.game['midx'] + x, self.window.game['midy']))

    def move_right(self, base=False):
        x = 400
        if base:
            x = 250
        self.left_mouse_drag((self.window.game['midx'], self.window.game['midy']),
                             (self.window.game['midx'] - x, self.window.game['midy']))

    def move_up(self, base=False):
        y = 250
        if base:
            y = 175
        self.left_mouse_drag((self.window.game['midx'], self.window.game['midy']),
                             (self.window.game['midx'], self.window.game['midy'] + y))

    def move_down(self, base=False):
        y = 250
        if base:
            y = 175
        self.left_mouse_drag((self.window.game['midx'], self.window.game['midy']),
                             (self.window.game['midx'], self.window.game['midy'] - y))
