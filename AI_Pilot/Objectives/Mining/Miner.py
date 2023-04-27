from AI_Pilot.Game_Functions.Common.Common import beta_get_game_state_cake
from AI_Pilot.Game_Functions.Cargo.Cargo import get_ship_root_cargo, unload_cargo
from AI_Pilot.Game_Functions.Common.Common import exit_hanger
from AI_Pilot.Game_Functions.Mining.Mining import get_miners_running
from loguru import logger
import time

cargo_unload_threshold = 0.9

def mining_cycle(ag):
    while True:
        state_result = beta_get_game_state_cake(ag)
        cargo_full = True if get_ship_root_cargo(ag) > cargo_unload_threshold else False

        if state_result['class'] == 'in_flight' and cargo_full:
            # nav home (set waypoint)
            # TODO
            raise Exception("Not Imp")
        elif state_result['class'] == 'in_hanger' and cargo_full:
            # unload
            unload_cargo(ag)
        elif state_result['class'] == 'in_hanger' and not cargo_full:
            # exit hanger
            exit_hanger(ag)
        elif state_result['class'] == 'in_flight' and not cargo_full:
            mining_tool_state_result = get_miners_running(ag)

            pass


        time.sleep(10)
    # get states
    # truth table
    # repeat







def mining_cycle_old(ag):
    logger.info('starting mining cycle')
    while True:
        state_result = beta_get_game_state_cake(ag)
        cargo_result = get_ship_root_cargo(ag)

        if state_result['class'] == 'in_flight':
            logger.info('currently in_flight')
            if cargo_result > cargo_unload_threshold:
                # Navigate to Home
                # TODO
                raise Exception("Not Imp")
                logger.info('need to unload cargo')
                unload_cargo(ag)
                logger.info('unloaded')
                pass
            else:
                logger.info('no need to unload cargo')
                # do nothing
                pass
            pass
        elif state_result['class'] == 'in_hanger':
            logger.info('currently in_hanger')
            if cargo_result > cargo_unload_threshold:
                logger.info('need to unload cargo')
                unload_cargo(ag)
                logger.info('unloaded')
                pass
            else:
                logger.info('no need to unload cargo')
                # do nothing
                pass
            # undock
            exit_hanger(ag)
            pass
        else:
            #TODO
            raise Exception('NOT IMP')
            pass

        # Pick Mining Site
        # Navigate to Mining Site
        # Start Mining


    time.sleep(10000)











    # get state
    # get to space