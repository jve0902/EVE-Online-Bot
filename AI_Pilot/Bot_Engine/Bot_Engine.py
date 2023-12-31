import threading, time, pyautogui
from AI_Pilot.Control_Functions.Monitors import get_monitor_spec, get_screen
from ml_botting_core import universal_predictor
from AI_Pilot.Game_Functions.Navigation.Waypoint_Navigation import navigate_waypoints_to_end
from AI_Pilot.Control_Functions.Mouse_Keyboard import perform_move_click, perform_range_select, recover_mouse
from AI_Pilot.Objectives.Aggregate_Resources.Aggregate_Resources import Aggregate_Resources
from AI_Pilot.Config_Management.Config_Management import load_config
from AI_Pilot.Objectives.Mining import Miner
import numpy as np


class active_globals():
    def __new__(cls, **args):  # make singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(active_globals, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self):
        if self.__initialized: return  # make singleton
        self.__initialized = True


class Bot_Engine:
    def __new__(cls, **args):  # make singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(Bot_Engine, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self, config_dir):
        if self.__initialized: return  # make singleton
        self.__initialized = True

        self.ag = active_globals()

        #config_dir = r'..\..\AI_Pilot\ai_pilot_config_v2.json'

        self.ag.config_dir = config_dir

        load_config(self.ag)

        self.ag.general_config = self.ag.this_config['general']
        self.ag.ml_botting_core_config = self.ag.this_config['ml_botting_core']
        self.ag.static_screen_pos = self.ag.this_config['static_screen_pos']

        monitor_spec = get_monitor_spec(self.ag)

        self.ag.monitor_spec = {
            "monitor_dims": (monitor_spec['width'], monitor_spec['height']),
            "monitor_offset": np.array([monitor_spec['left'], monitor_spec['top']])  # x, y
        }

        self.ag.up = universal_predictor(config=self.ag.ml_botting_core_config)

        self.dock_at_destination_parms = {}
        self.search_for_destination_parms = {}

    # region ----- dock_at_destination
    def dock_at_destination_e_stop(self):
        self.dock_at_destination_parms['e_stop'] = True

    def dock_at_destination_threaded(self, logging_callback, ui_callback, params):
        self.dock_at_destination_parms['thread'] = threading.Thread(target=self.dock_at_destination,
                                                                    args=(logging_callback, ui_callback,params,))
        self.dock_at_destination_parms['thread'].start()

    def dock_at_destination(self, logging_callback, ui_callback, params):
        self.dock_at_destination_parms['e_stop'] = False
        ui_callback('dock_at_destination_button', 'state', 'disabled')
        ui_callback('dock_at_destination_e_stop_button', 'state', 'active')
        logging_callback(f"Starting in 1 Second...")
        time.sleep(1)
        self.ag.navigation = params
        navigate_waypoints_to_end(self.ag)

        ui_callback('dock_at_destination_button', 'state', 'active')
        ui_callback('dock_at_destination_e_stop_button', 'state', 'disabled')
        logging_callback(f"Arrived")

    # endregion

    # region ----- search_for_destination
    def move_ore_threaded(self, ui_class):
        self.search_for_destination_parms['thread'] = threading.Thread(target=self.move_ore,
                                                                       args=(ui_class,))
        self.search_for_destination_parms['thread'].start()

    def move_ore(self, ui_class):
        source_staton = ui_class.ui_element_get_text('migrate_ore_tb1')
        destination_staton = ui_class.ui_element_get_text('migrate_ore_tb2')
        next_target = source_staton
        next_action = 'load'
        while True:
            perform_move_click(self.ag, pos=(156, 130), button='left', perform_offset=True)
            pyautogui.write(next_target)
            time.sleep(3)
            pyautogui.press('enter')

            click_target = (1300, 650)
            if next_action == 'unload':
                click_target = (1300, 680)

            perform_move_click(self.ag, pos=click_target, button='right', perform_offset=True)
            box_top_left = (click_target[0] + 12, click_target[1] - 33)
            box_bottom_right = (click_target[0] + 256 + 12, click_target[1] + 396 - 33)
            img = get_screen(self.ag)
            img = img.crop([box_top_left[0], box_top_left[1], box_bottom_right[0], box_bottom_right[1]])
            set_dest_result = self.ag.up.predict(img, 'set_dest')

            if set_dest_result['class'] == 'second_pos':
                click_target = (click_target[0] + 50, click_target[1] + 60)
            elif set_dest_result['class'] == 'seventh_pos':
                click_target = (click_target[0] + 50, click_target[1] + 234)
            elif set_dest_result['class'] == 'third_pos':
                click_target = (click_target[0] + 50, click_target[1] + 109)

            perform_move_click(self.ag, pos=click_target, button='left', perform_offset=True)
            time.sleep(2)
            # nav
            self.dock_at_destination(ui_class.dock_at_destination_append_log, ui_class.ui_element_change)
            time.sleep(2)
            # pick up ore
            if next_action == 'load':
                perform_move_click(self.ag, pos=tuple(self.ag.static_screen_pos['hanger_target']), button='left',
                                   perform_offset=True)
                time.sleep(1)
                #perform_range_select(self.ag, tuple(self.ag.static_screen_pos['click_and_drag_inv_box'][2:4]),
                #                          tuple(self.ag.static_screen_pos['click_and_drag_inv_box'][0:2]))
                time.sleep(1)
                perform_range_select(self.ag,
                    tuple(self.ag.static_screen_pos['Load_to_mininghold_click_and_drag_inv_line'][0:2]),
                    tuple(self.ag.static_screen_pos['ship_root_target']))
                time.sleep(1)
                img = get_screen(self.ag)
                menu_result = self.ag.up.predict(img, 'hanger_menus')
                if menu_result['class'] == 'set_quant':
                    perform_move_click(self.ag, pos=tuple(self.ag.static_screen_pos['set_quant_target']), button='left',
                                       perform_offset=True)
                time.sleep(1)
            else:
                perform_move_click(self.ag, pos=tuple(self.ag.static_screen_pos['ship_root_target']), button='left',
                                   perform_offset=True)
                time.sleep(1)
                perform_range_select(self.ag, tuple(self.ag.static_screen_pos['click_and_drag_inv_box'][2:4]),
                                          tuple(self.ag.static_screen_pos['click_and_drag_inv_box'][0:2]))
                time.sleep(1)
                perform_range_select(self.ag,
                    tuple(self.ag.static_screen_pos['Load_to_mininghold_click_and_drag_inv_line'][0:2]),
                    tuple(self.ag.static_screen_pos['hanger_target']))
                time.sleep(1)

            perform_move_click(self.ag, pos=tuple(self.ag.static_screen_pos['exit_hanger_target']), button='left',
                               perform_offset=True)
            time.sleep(30)

            if next_target == source_staton:
                next_target = destination_staton
                next_action = 'unload'
            else:
                next_target = source_staton
                next_action = 'load'

        # set dest
        # nav
        # drop off

        return

    def search_for_destination_threaded(self, ui_class):
        self.search_for_destination_parms['thread'] = threading.Thread(target=self.search_for_destination,
                                                                       args=(ui_class))
        self.search_for_destination_parms['thread'].start()

    def search_for_destination(self, ui_class):

        time.sleep(1)
        search_string = "Amsen VI - Moon - Moon 1 Science and Trade Institute School"
        perform_move_click(self.ag, pos=(156, 130), button='left', perform_offset=True)
        pyautogui.write(search_string)
        time.sleep(3)
        pyautogui.press('enter')
        perform_move_click(self.ag, pos=(1300, 650), button='right', perform_offset=True)
        perform_move_click(self.ag, pos=(1300 + 50, 650 + 65), button='right', perform_offset=True)
        pass
    # endregion

    # region ----- Mining Bot

    # endregion

    # region ----- aggrogate_resources
    def aggregate_resources_start(self, params):
        self.ag.navigation = params
        Aggregate_Resources(self.ag)
        return
    # endregion

    # region ----- minning
    def start_mining(self):
        Miner.mining_cycle(self.ag)
        return

    def restart_fault_vars(self):
        Miner.restart_fault_vars(self.ag)

    def reset_stale_mining_sites(self):
        Miner.reset_stale_mining_sites(self.ag)

    def recover_mouse(self):
        recover_mouse(self.ag)
    # endregion
