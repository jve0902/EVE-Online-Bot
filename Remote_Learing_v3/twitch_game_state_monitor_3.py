import threading, time, json, socket, pyautogui, uuid, random
from AI_Pilot.Monitor_Interface.Monitors import get_monitor_spec, get_screen
from AI_Pilot.General.General import get_game_state
from ml_botting_core import universal_predictor
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

ag = active_globals()

config_dir = r'remote_learning_config.json'

host = socket.gethostname()
config = json.load(open(config_dir))
if host in config:
    config = config[host]
else:
    config = config['default']

ag.general_config = config['general']
ag.ml_botting_core_config = config['ml_botting_core']
ag.static_screen_pos = config['static_screen_pos']

ag.up = universal_predictor(config=ag.ml_botting_core_config)
monitor_spec = get_monitor_spec(ag)

ag.monitor_spec = {
    "monitor_dims": (monitor_spec['width'], monitor_spec['height']),
    "monitor_offset": np.array([monitor_spec['left'], monitor_spec['top']])  # x, y
}

while True:
    state_result = get_game_state(ag)
    time.sleep(10)
