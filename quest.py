import time
import util
import statics


class Quest:
    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.last_quest_check = 0
        
    def collect_quests(self, qtype):
        self.vision.refresh_frame()
        while self.vision.is_visible('quest_collect', threshold=0.6):
            if qtype == 'Turf':
                self.controller.click_point(statics.quest['turf_collect'])
            else:
                self.controller.click_point(statics.quest['ag_collect'])
            util.log(qtype + ' Quest collected.')
            time.sleep(3)
            self.vision.refresh_frame()

    def quest_start(self, qtype):
        self.vision.refresh_frame()
        if self.vision.is_visible('quest_start', threshold=0.7):
            self.controller.click_point(statics.quest['ag_collect'])
            util.log(qtype + ' Quest started.')
            time.sleep(1.25)
            self.vision.refresh_frame()

    def check_quests(self):
        util.log("Checking quests.")
        self.controller.click_point(statics.hud['quest'])

        if self.vision.is_visible('quest_turf_comp', threshold=0.5):
            self.controller.click_point(statics.quest['turf'])
            self.collect_quests('Turf')

        if self.vision.is_visible('quest_admin_comp', threshold=0.5):
            self.controller.click_point(statics.quest['admin'])
            self.collect_quests('Admin')
            self.quest_start('Admin')

        if self.vision.is_visible('quest_guild_comp', threshold=0.5):
            self.controller.click_point(statics.quest['guild'])
            self.collect_quests('Guild')
            self.quest_start('Guild')

        if self.vision.is_visible('quest_vip_comp', threshold=0.5):
            self.controller.click_point(statics.quest['vip'])
            self.vision.refresh_frame()
            if self.vision.is_visible('quest_vip_chest', threshold=0.7) and \
                    self.vision.is_visible('quest_vip_claim', threshold=0.7):
                self.controller.click_object(
                    self.vision.find_template('quest_vip_chest', threshold=0.7),
                    offset=(31, 40)
                )
        self.last_quest_check = time.time()

    def time_lapsed(self):
        return time.time() - self.last_quest_check > 300
