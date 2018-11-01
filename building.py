import util
import time
import statics


class Building:
    def __init__(self, vision, state, controller, window):
        self.building = 1
        self.vision = vision
        self.state = state
        self.controller = controller
        self.window = window

    def upgrade(self):
        self.state.ret_base()
        self.controller.click_point(statics.buildings['castle']['points'])
        self.vision.refresh_frame()
        self.state.turf_loc = None
        while True:
            if self.vision.is_visible('dev_upgrade', threshold=0.7):
                self.controller.click_point(statics.dev['upgrade'])
            time.sleep(1)
            self.vision.refresh_frame()
            for i in range(3):
                go_matches = self.vision.find_template('dev_go', threshold=0.7)
                if len(go_matches[0]) > 0:
                    break
                else:
                    self.vision.refresh_frame()
                    time.sleep(0.25)
            if len(go_matches[0]) > 0:
                self.controller.click_object(go_matches)
                time.sleep(1.25)
                midx = self.window.game['x1'] + self.window.game['w'] / 2
                midy = self.window.game['y1'] + 55 + self.window.game['h'] / 2
                self.controller.click_point((midx, midy))
                time.sleep(0.50)
                self.vision.refresh_frame()
            matches = self.vision.find_template('dev_new', threshold=0.7)
            if len(matches[0]) > 0:
                self.controller.click_object(matches, offset=(200, 10))
                time.sleep(0.5)
            if not self.vision.is_visible('dev_upgrade', 0.7):
                break
        self.vision.refresh_frame()
        self.controller.click_point(statics.dev['upgrade'])
        util.log("Started upgrading a building.")

    def to_building(self, building):
        self.state.to_screen(statics.buildings[building]['screen'])
        time.sleep(1)
        self.vision.refresh_frame()
