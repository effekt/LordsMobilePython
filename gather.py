import time
import util


class Gather:
    def __init__(self, vision, state, controller):
        self.vision = vision
        self.state = state
        self.controller = controller
        self.res = {
            0: {'asset': 'res_field', 'name': 'Field', 'thresh': 0.45},
            1: {'asset': 'res_rocks', 'name': 'Rock', 'thresh': 0.45},
            2: {'asset': 'res_ore', 'name': 'Ore', 'thresh': 0.45},
            3: {'asset': 'res_wood', 'name': 'Wood', 'thresh': 0.6},
            4: {'asset': 'res_gold', 'name': 'Gold', 'thresh': 0.5}
        }
        self.current_resource = 0

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
        self.state.to_kingdom()
        self.current_resource %= 5
        util.log('Searching for: ' + self.res[self.current_resource]['name'])
        if self.vision.is_visible(self.res[self.current_resource]['asset'], self.res[self.current_resource]['thresh']):

            res_matches = self.vision.find_template(self.res[self.current_resource]['asset'],
                                                    threshold=self.res[self.current_resource]['thresh'])

            while len(res_matches[0]) > 0 and not self.vision.is_visible('army_status'):
                res_matches = self.controller.click_object(res_matches, (15, 45))
                util.log(self.res[self.current_resource]['name'] + ' gathering attempted.')
                if self.start_gather():
                    break

        if self.current_resource < 5:
            self.current_resource += 1
