import threading, time, json, socket, pyautogui, uuid, random

def load_config(ag):
    host = socket.gethostname()
    ag.config = json.load(open(ag.config_dir))
    if host in ag.config:
        config = ag.config[host]
    else:
        config = ag.config['default']
    ag.this_config = config

    ag.general_config = config['general']
    ag.ml_botting_core_config = config['ml_botting_core']
    ag.static_screen_pos = config['static_screen_pos']
    ag.mongo_logging = config['mongo_logging']

def save_config(ag):
    host = socket.gethostname()
    raw_config = json.load(open(ag.config_dir))
    target = None
    if host in ag.config:
        target = host
    else:
        target = 'default'

    raw_config[target]['general'] = ag.general_config
    raw_config[target]['ml_botting_core'] = ag.ml_botting_core_config
    raw_config[target]['static_screen_pos'] = ag.static_screen_pos
    raw_config[target]['mongo_logging'] = ag.mongo_logging

    with open(ag.config_dir, "w+") as outfile:
        outfile.write(json.dumps(raw_config, indent=1))

    load_config(ag)
    return ag

