import time
from gather import Gather
from state import State
from quest import Quest
import util


class Game:
    def __init__(self, vision, controller, window):
        self.vision = vision
        self.controller = controller
        self.window = window
        self.current_resource = 2
        self.train_troops = 0
        self.state = State(vision, controller, window)
        self.gather = Gather(vision, self.state, controller)
        self.quest = Quest(vision, controller)

    def run(self):
        util.log("Starting up!")
        while True and self.state != 'unknown':
            self.state.clean_state(turf=1)
            self.vision.refresh_frame()
            if self.vision.is_visible('free_speedup', threshold=0.6):
                self.controller.click_object(self.vision.find_template('free_speedup', threshold=0.6))
                util.log('Finished research / building.')
            if self.vision.is_visible('help', threshold=0.4):
                self.controller.click_object(self.vision.find_template('help', threshold=0.4))
                util.log('Requested help for research / building.')
            elif self.vision.is_visible('free_chest', threshold=0.5):
                self.controller.click_object(self.vision.find_template('free_chest', threshold=0.5))
                time.sleep(1)
                self.vision.refresh_frame()
                if self.vision.is_visible('free_chest_claim', threshold=0.5):
                    self.controller.click_object(self.vision.find_template('free_chest_claim', threshold=0.5))
                util.log('Collected free chest.')
            elif self.vision.is_visible('free_chest_5x', threshold=0.5):
                self.controller.click_object(self.vision.find_template('free_chest_5x', threshold=0.5))
                time.sleep(1)
                self.vision.refresh_frame()
                if self.vision.is_visible('free_chest_claim', threshold=0.5):
                    self.controller.click_object(self.vision.find_template('free_chest_claim', threshold=0.5))
                util.log('Collected 5x free chest.')
            elif not self.vision.is_visible('army_status'):
                self.state.clean_state()
                self.gather.gather()

            # elif self.vision.is_visible('barracks_idle') and self.train_troops == 1:
            #     self.controller.click_object(self.vision.find_template('barracks_idle'))
            #     time.sleep(1.25)
            #     self.vision.refresh_frame()
            #     if self.vision.is_visible('unit_ballista'):
            #         self.controller.click_object(self.vision.find_template('unit_ballista'))
            #         time.sleep(1.25)
            #         self.vision.refresh_frame()
            #         if self.vision.is_visible('barracks_train'):
            #             self.controller.click_object(self.vision.find_template('barracks_train'))

            # self.vision.is_visible('quest_uncompleted') or
            elif (self.vision.is_visible('quest_has_quests') or
                    self.vision.is_visible('quest_has_completed')) and self.quest.time_lapsed():
                self.quest.check_quests()
            elif self.vision.is_visible('cr_none', threshold=0.4):
                self.state.rebase()
                if self.vision.is_visible('amt_wood', threshold=0.6):
                    self.controller.click_object(self.vision.find_template('amt_wood', threshold=0.6), offset=(-171, 0))
                    time.sleep(1.5)
                    self.vision.refresh_frame()
                    while True:
                        self.controller.click_object(self.vision.find_template('cr_upgrade', threshold=0.8))
                        time.sleep(1.5)
                        self.vision.refresh_frame()
                        for i in range(3):
                            go_matches = self.vision.find_template('cr_go', threshold=0.4)
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
                            self.controller.click_object([[midy], [midx]])
                            time.sleep(1.50)
                            self.vision.refresh_frame()
                        if not self.vision.is_visible('cr_upgrade', 0.8):
                            break
                    self.vision.refresh_frame()
                    self.controller.click_object(self.vision.find_template('cr_upgrade', threshold=0.8))


            time.sleep(1)
