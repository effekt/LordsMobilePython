import time
import util


class Quest:
    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.last_quest_check = 0
        
    def collect_quests(self, qtype):
        self.vision.refresh_frame()
        while self.vision.is_visible('quest_collect', threshold=0.4):
            matches = []
            if self.vision.is_visible('quest_collect', 0.4):
                matches = self.vision.find_template('quest_collect', threshold=0.4)
            if len(matches[0]) > 0:
                self.controller.click_object(matches)
                util.log(qtype + ' Quest collected.')
                time.sleep(3)
                self.vision.refresh_frame()

    def quest_start(self, qtype):
        self.vision.refresh_frame()
        if self.vision.is_visible('quest_start', threshold=0.5):
            matches = self.vision.find_template('quest_start', threshold=0.5)
            self.controller.click_object(matches)
            util.log(qtype + ' Quest started.')
            time.sleep(1.25)
            self.vision.refresh_frame()

    def check_quests(self):
        util.log("Checking quests.")
        matches = []
        if self.vision.is_visible('quest_has_quests', threshold=0.6):
            matches = self.vision.find_template('quest_has_quests', threshold=0.6)
        elif self.vision.is_visible('quest_has_completed', threshold=0.6):
            matches = self.vision.find_template('quest_has_completed', threshold=0.6)
            
        if matches is []:
            util.log("No quests for completing.")
            self.last_quest_check = time.time()
            return
        
        self.controller.click_object(matches)
        time.sleep(1.25)
        self.vision.refresh_frame()
        
        matches = []
        if self.vision.is_visible('quest_turf', threshold=0.7):
            matches = self.vision.find_template('quest_turf', threshold=0.7)
            
        if len(matches[0]) > 0:
            self.controller.click_object(matches)
            time.sleep(1)
            self.collect_quests('Turf')

        matches = []
        if self.vision.is_visible('quest_admin', threshold=0.7):
            matches = self.vision.find_template('quest_admin', threshold=0.7)

        if len(matches[0]) > 0:
            self.controller.click_object(matches)
            time.sleep(1)
            self.collect_quests('Admin')
            self.quest_start('Admin')

        matches = []
        if self.vision.is_visible('quest_guild', threshold=0.7):
            matches = self.vision.find_template('quest_guild', threshold=0.7)

        if len(matches[0]) > 0:
            self.controller.click_object(matches)
            time.sleep(1)
            self.collect_quests('Guild')
            self.quest_start('Guild')

        matches = []
        if self.vision.is_visible('quest_vip', threshold=0.7):
            matches = self.vision.find_template('quest_vip', threshold=0.7)

        if len(matches[0]) > 0:
            self.controller.click_object(matches)
            time.sleep(1)
            self.vision.refresh_frame()
            if self.vision.is_visible('quest_vip_lock', threshold=0.4):
                self.controller.click_object(self.vision.find_template('quest_vip_lock', threshold=0.4))
        self.last_quest_check = time.time()

    def time_lapsed(self):
        return time.time() - self.last_quest_check > 300
