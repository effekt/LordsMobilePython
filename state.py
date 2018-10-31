import time
import util
import random


class State:
    def __init__(self, vision, controller, window):
        self.vision = vision
        self.controller = controller
        self.window = window
        self.state = "unset"

    def clean_state(self, turf=0):
        self.vision.refresh_frame()
        while self.vision.is_visible('screen_close', threshold=0.6) or \
                self.vision.is_visible('screen_close_level_up', threshold=0.6) or \
                self.vision.is_visible('screen_close_main', threshold=0.6):
            if self.vision.is_visible('screen_close', threshold=0.6):
                close_scr_matches = self.vision.find_template('screen_close', threshold=0.6)
                self.controller.click_object(close_scr_matches)
            elif self.vision.is_visible('screen_close_level_up', threshold=0.6):
                close_scr_matches = self.vision.find_template('screen_close_level_up', threshold=0.6)
                self.controller.click_object(close_scr_matches)
            elif self.vision.is_visible('screen_close_main', threshold=0.6):
                close_scr_matches = self.vision.find_template('screen_close_main', threshold=0.6)
                self.controller.click_object(close_scr_matches)
            time.sleep(1.5)
            self.vision.refresh_frame()
        if self.vision.is_visible('kingdom', threshold=0.6):
            self.state = 'turf'
        elif self.vision.is_visible('turf', threshold=0.6):
            self.state = 'kingdom'
        else:
            self.state = 'unknown'

        if self.vision.is_visible('expand_ongoing', threshold=0.6):
            self.controller.click_object(self.vision.find_template('expand_ongoing'))

        if self.state == 'kingdom' and turf == 1:
            turf_matches = self.vision.find_template('turf', threshold=0.6)
            self.controller.click_object(turf_matches)
            util.log('Returned to Turf')
            time.sleep(5)
        return

    def to_kingdom(self):
        if self.state == 'turf':
            kingdom_matches = self.vision.find_template('kingdom', threshold=0.6)
            self.controller.click_object(kingdom_matches)
            util.log('Moved to Kingdom.')
            self.state = 'kingdom'
            time.sleep(5)
            self.vision.refresh_frame()

    def rebase(self):
        self.vision.refresh_frame()
        util.log("Attempting to reset Turf position.")
        while not self.vision.is_visible('static_turf_statue', threshold=0.22):
            randx = random.randint(-1, 1) * 300
            randy = random.randint(-1, 1) * 300
            if not randx and not randy:
                randx = random.randint(-1, 1) * 300
                randy = random.randint(-1, 1) * 300
            midx = self.window.game['x1'] + self.window.game['w'] / 2
            midy = self.window.game['y1'] + self.window.game['h'] / 2
            self.controller.left_mouse_drag(
                (midx, midy),
                (midx + randx, midy + randy)
            )
            time.sleep(1.5)
            self.vision.refresh_frame()

        matches = self.vision.find_template('static_turf_statue', threshold=0.22)
        self.controller.click_object(matches)
        time.sleep(3.5)
        self.clean_state(turf=1)
        time.sleep(3.5)
        self.vision.refresh_frame()
