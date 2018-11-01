import time
import util
import statics


class Gather:
    def __init__(self, vision, state, controller):
        self.vision = vision
        self.state = state
        self.controller = controller
        self.res = {
            0: {'asset': ['res_field'], 'title': 'res_txt_f', 'name': 'Field', 'thresh': 0.45},
            1: {'asset': ['res_rocks'], 'title': 'res_txt_r', 'name': 'Rock', 'thresh': 0.45},
            2: {'asset': ['res_ore2', 'res_ore'], 'title': 'res_txt_o', 'name': 'Ore', 'thresh': 0.45},
            3: {'asset': ['res_woods', 'res_woods2'], 'title': 'res_txt_w', 'name': 'Wood', 'thresh': 0.6},
            4: {'asset': ['res_gold2', 'res_gold'], 'title': 'res_txt_g', 'name': 'Gold', 'thresh': 0.5}
        }
        self.current_resource = 0
        self.moves = [
            self.controller.move_left,
            self.controller.move_up,
            self.controller.move_right,
            self.controller.move_right,
            self.controller.move_down,
            self.controller.move_down,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_left,
            self.controller.move_up,
            self.controller.move_up,
            self.controller.move_up,
            self.controller.move_right,
            self.controller.move_right,
            self.controller.move_right,
            self.controller.move_right
        ]

    def start_gather(self):
        time.sleep(1.25)
        self.vision.refresh_frame()
        if self.vision.is_visible('gather_gather') and not self.vision.is_visible('army_status'):
            gather_matches = self.vision.find_template('gather_gather')
            self.controller.click_object(gather_matches)
            time.sleep(1.25)
            self.vision.refresh_frame()
            gather_matches = self.vision.find_template('gather_auto_ass')
            self.controller.click_object(gather_matches)
            time.sleep(0.5)
            gather_matches = self.vision.find_template('gather_start')
            self.controller.click_object(gather_matches)
            time.sleep(5)
            return True
        else:
            self.state.clean_state()
            return False

    def gather(self):
        self.state.clean_state()
        self.state.to_kingdom()
        self.current_resource %= 5
        move = 0
        res = self.res[self.current_resource]
        self.vision.refresh_frame()
        gathering = False
        while move < 15 and not gathering:
            util.log('Searching for: ' + res['name'])
            for ass in res['asset']:
                self.vision.refresh_frame()
                match = self.vision.find_template(ass, max_v=True)
                self.controller.click_object(match, offset=(35, 45))
                time.sleep(1.25)
                self.vision.refresh_frame()
                if self.vision.is_visible(res['title'], threshold=0.7) and \
                        self.vision.is_visible('res_gather', threshold=0.8):
                    self.controller.click_point(statics.gather['gather'])
                    self.controller.click_point(statics.gather['assemble'])
                    self.controller.click_point(statics.gather['start'])
                    gathering = True
                    util.log('Starting gathering: ' + res['name'])
                else:
                    self.state.clean_state()
                    time.sleep(1)
            if not gathering:
                self.moves[move]()
                move += 1

        if self.current_resource < 5:
            self.current_resource += 1
        self.vision.refresh_frame()
