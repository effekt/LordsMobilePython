import time
from gather import Gather
from state import State
from quest import Quest
import util
import statics
from building import Building


class Game:
    def __init__(self, vision, controller, window):
        self.vision = vision
        self.controller = controller
        self.window = window
        self.current_resource = 2
        self.train_troops = 0
        self.state = State(vision, controller, window)
        self.gather = Gather(vision, self.state, controller)
        self.building = Building(vision, self.state, controller, window)
        self.quest = Quest(vision, controller)
        self.last_inf_check = 0
        self.last_shelter_check = 0

    def run(self):
        util.log("Starting MaggotBot!")
        while True and self.state != 'unknown':
            self.state.clean_state(turf=1)
            if self.vision.is_visible('dev_free', threshold=0.7):
                self.controller.click_object(self.vision.find_template('dev_free', threshold=0.7))
                util.log('Finished research / building.')
            if self.vision.is_visible('dev_help', threshold=0.7):
                self.controller.click_object(self.vision.find_template('dev_help', threshold=0.7))
                util.log('Requested help for research / building.')
            if time.time() - self.last_shelter_check > 300:
                self.building.to_building('shelter')
                util.log('Checking shelter.')
                if self.vision.is_visible('turf_shelter', threshold=0.675):
                    self.controller.click_point(statics.buildings['shelter']['points'])
                    time.sleep(1)
                    self.controller.click_point(statics.shelter['hours'])
                    time.sleep(0.3)
                    self.controller.click_point(statics.shelter['ok'])
                    time.sleep(0.75)
                    self.controller.click_point(statics.shelter['clear'])
                    time.sleep(0.3)
                    self.controller.click_point(statics.shelter['grunt'])
                    time.sleep(0.3)
                    self.controller.click_point(statics.shelter['go'])
                    time.sleep(1.25)
                    self.vision.refresh_frame()
                    self.last_shelter_check = time.time()
                    util.log('Sheltered leader.')
                else:
                    self.last_shelter_check = time.time()
            elif self.vision.is_visible('chest_collect', threshold=0.9):
                self.controller.click_point(statics.chest['chest'])
                if self.vision.is_visible('chest_5x', 0.8):
                    util.log('Collected 5x free chest.')
                else:
                    util.log('Collected free chest.')
                self.controller.click_point(statics.chest['claim'])
            elif self.vision.is_visible('hud_gift', threshold=0.7):
                self.controller.click_point(statics.hud['guild'])
                time.sleep(1.25)
                self.controller.click_point(statics.guild['tab1'])
                time.sleep(0.5)
                self.controller.click_point(statics.guild['gift'])
                time.sleep(0.5)
                self.vision.refresh_frame()
                while self.vision.is_visible('guild_open', threshold=0.7):
                    self.controller.click_point(statics.guild['open'])
                    time.sleep(0.5)
                    self.controller.click_point(statics.guild['delete'])
                    self.vision.refresh_frame()
                    util.log('Collected guild gift.')
            elif not self.vision.is_visible('hud_army', threshold=0.8):
                util.log('Attempting to gather.')
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
            elif (self.vision.is_visible('quest_has_q', threshold=0.8) or
                    self.vision.is_visible('quest_has_completed', threshold=0.8)) and self.quest.time_lapsed():
                self.quest.check_quests()
            elif self.vision.is_visible('dev_no_cr', threshold=0.8):
                self.building.upgrade()

            elif time.time() - self.last_inf_check > 300:
                self.building.to_building('infirmary')
                if self.vision.is_visible('turf_infirmary', threshold=0.65):
                    self.controller.click_point(statics.buildings['infirmary']['points'])
                    self.controller.click_point(statics.infirmary['heal'])
                    util.log('Healing troops.')
                self.last_inf_check = time.time()


            time.sleep(1)
