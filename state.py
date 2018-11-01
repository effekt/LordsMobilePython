import time
import util
import statics


class State:
    def __init__(self, vision, controller, window):
        self.vision = vision
        self.controller = controller
        self.window = window
        self.state = "unset"
        self.turf_loc = None
        self.movements = {
            1: {'go': [], 'return': []},
            2: {
                'go':
                    [self.controller.move_left],
                'return':
                    [self.controller.move_right]},
            3: {
                'go':
                    [
                        self.controller.move_right,
                        self.controller.move_up
                    ],
                'return':
                    [
                        self.controller.move_left,
                        self.controller.move_down
                    ]
            }
        }

    def clean_state(self, turf=0):
        self.vision.refresh_frame()
        while self.vision.is_visible('etc_close', threshold=0.7):
            self.controller.click_object(self.vision.find_template('etc_close', threshold=0.7))
            time.sleep(1)
            self.vision.refresh_frame()

        if self.vision.is_visible('etc_kingdom', threshold=0.7):
            self.state = 'turf'
        elif self.vision.is_visible('etc_turf', threshold=0.7):
            self.state = 'kingdom'
        else:
            self.state = 'unknown'

        if self.state == 'kingdom' and turf == 1:
            turf_matches = self.vision.find_template('etc_turf', threshold=0.7)
            self.controller.click_object(turf_matches)
            util.log('Returned to Turf')
            time.sleep(5)

    def to_kingdom(self):
        if self.state == 'turf':
            kingdom_matches = self.vision.find_template('etc_kingdom', threshold=0.6)
            self.controller.click_object(kingdom_matches)
            util.log('Moved to Kingdom.')
            self.state = 'kingdom'
            time.sleep(5)
            self.vision.refresh_frame()

    def rebase(self):
        self.vision.refresh_frame()
        util.log("Attempting to reset Turf position.")
        moves = [
            self.controller.move_down,
            self.controller.move_down,
            self.controller.move_down,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_right,
            self.controller.move_right
        ]
        matches = self.vision.find_template('turf_statue', threshold=0.45)
        for move in moves:
            if len(matches[0]) > 0:
                break
            move()
            matches = self.vision.find_template('turf_statue', threshold=0.45)

        if len(matches[0]) > 0:
            self.controller.click_object(matches, offset=(30, 75))
        else:
            self.controller.click_point(statics.clean_state['statue'])
        time.sleep(2.5)
        self.vision.refresh_frame()
        self.clean_state(turf=1)
        time.sleep(3.5)
        self.vision.refresh_frame()
        self.turf_loc = 1

    def to_screen(self, scr):
        if scr != self.turf_loc:
            self.ret_base()
            for mvmt in self.movements[scr]['go']:
                mvmt(True)
        self.turf_loc = scr
        self.vision.refresh_frame()

    def ret_base(self):
        if self.turf_loc != 1:
            if self.turf_loc is not None:
                for mvmt in self.movements[self.turf_loc]['return']:
                    mvmt(True)
                self.turf_loc = 1
            else:
                self.rebase()
        self.vision.refresh_frame()
