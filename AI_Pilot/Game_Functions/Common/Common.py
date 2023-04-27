import time
from AI_Pilot.Control_Functions.Mouse_Keyboard import perform_move_click
from AI_Pilot.Control_Functions.Monitors import get_screen
from AI_Pilot.Control_Functions.General import convert_to_baw
from loguru import logger
import numpy as np


def get_game_state(ag):
    # region ----- get game state
    img = get_screen(ag)
    state_result = ag.up.predict(img, 'game_state')
    logger.info(state_result)
    # endregion
    return state_result


def beta_get_game_state_cake(ag):
    img = get_screen(ag)
    result = ag.up.predict(img, 'game_state_cake_layer_1_v1')
    logger.info(result)
    min_threshold = ag.up.classifiers['game_state_cake_layer_1_v1']['meta']['decision_threshold']
    if float(result['value_at_argmax']) < min_threshold:
        result = ag.up.predict(img, 'game_state_cake_layer_2_v1')
        logger.info(result)

    return result


def exit_hanger(ag):
    perform_move_click(ag, ag.static_screen_pos['click_target_exit_hanger'], button='left')
    time.sleep(30)


def extract_values(img, cells, x_range, y_range, columns,
                   monitor_x_offset, monitor_y_offset,
                   click_target_offset_x, click_target_offset_y
                   ):
    frames = []
    for i in range(len(y_range) - 1):
        frame = {}
        for j in range(0, len(x_range) - 1):
            cell = cell_dims_from_list(list(cells[j, i]))
            cell_image = img.crop(cell)

            transcript = pytesseract.image_to_string(cell_image, lang='eng')

            frame[columns[j]] = transcript.replace('\n', '').replace('+', '').replace('>', '').replace('k m',
                                                                                                       ' km').replace(
                ',', '')
        frame['click_target'] = (
            cells[0, i][0] + click_target_offset_x + monitor_x_offset,
            cells[0, i][1] + click_target_offset_y + monitor_y_offset)  # offset by 10x10 pixels
        frames.append(frame)
    return pd.DataFrame(frames, columns=columns)


def extract_bool(img, cells, x_range, y_range, columns,
                 monitor_x_offset, monitor_y_offset,
                 click_target_offset_x, click_target_offset_y
                 ):
    frames = []
    for i in range(len(y_range) - 1):
        frame = {}
        for j in range(0, len(x_range) - 1):
            cell = cell_dims_from_list(list(cells[j, i]))
            cell_image = img.crop(cell)

            cell_image = convert_to_baw(cell_image, thresh=160)
            img_array = np.array(cell_image)

            percent_text = len(img_array[img_array == True]) / (
                    len(img_array[img_array == True]) + len(img_array[img_array == False]))

            populated = False
            if percent_text > 0.005:
                populated = True

            frame[columns[j]] = populated

        frame['click_target'] = (
            cells[0, i][0] + click_target_offset_x + monitor_x_offset,
            cells[0, i][1] + click_target_offset_y + monitor_y_offset)  # offset by 10x10 pixels
        frames.append(frame)
    return pd.DataFrame(frames, columns=columns)