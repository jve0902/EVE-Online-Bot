import cv2
import sys, os, decimal, json

sys.path.append(os.path.realpath('..'))
import json, time
import pandas as pd
import random
import matplotlib.pyplot as plt
import glob
import uuid
import matplotlib.pyplot as plt
import numpy as np
import random
import PIL, json
import tensorflow as tf
from PIL import Image
import socket
import pathlib
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageOps

from sklearn.metrics import confusion_matrix

from TrainingPipelines.ImageClassifier.ModelBuilder import build_and_train

import seaborn as sns
import mplcyberpunk
import json

plt.style.use("cyberpunk")
plt.rcParams['figure.facecolor'] = '#0d1117'
plt.rcParams['axes.facecolor'] = '#0d1117'
plt.rcParams['savefig.facecolor'] = '#0d1117'

cap = cv2.VideoCapture(r"C:\Users\ryans\Videos\2023-04-09 21-29-33.mp4")

output = cv2.VideoWriter(f"C:\\Users\\ryans\\Videos\\out4.avi", cv2.VideoWriter_fourcc(*'DIVX'), 30, (1920, 1080))

model2 = tf.keras.models.load_model(
    r"O:\eve_models\training_data\route_y_large_vert_class_v4\route_y_large_vert_class_v4_model.h5", compile=False)
class_names = [
  "100_200",
  "100_210",
  "100_220",
  "100_250",
  "100_260",
  "100_270",
  "100_290",
  "100_310",
  "100_320",
  "100_330",
  "100_340",
  "100_350",
  "100_360",
  "100_370",
  "100_380",
  "100_390",
  "100_400",
  "100_410",
  "100_420",
  "100_430",
  "100_440",
  "100_460",
  "100_470",
  "100_480",
  "100_490",
  "110_200",
  "110_210",
  "110_220",
  "110_250",
  "110_260",
  "110_270",
  "110_290",
  "110_310",
  "110_320",
  "110_330",
  "110_340",
  "110_350",
  "110_360",
  "110_370",
  "110_380",
  "110_390",
  "110_400",
  "110_410",
  "110_420",
  "110_430",
  "110_440",
  "110_460",
  "110_470",
  "110_480",
  "110_490",
  "120_200",
  "120_210",
  "120_220",
  "120_250",
  "120_260",
  "120_270",
  "120_290",
  "120_310",
  "120_320",
  "120_330",
  "120_340",
  "120_350",
  "120_360",
  "120_370",
  "120_380",
  "120_390",
  "120_400",
  "120_410",
  "120_420",
  "120_430",
  "120_440",
  "120_460",
  "120_470",
  "120_480",
  "120_490",
  "130_100",
  "130_110",
  "130_120",
  "130_130",
  "130_140",
  "130_150",
  "130_160",
  "130_170",
  "130_180",
  "130_190",
  "130_200",
  "130_210",
  "130_220",
  "130_230",
  "130_240",
  "130_250",
  "130_260",
  "130_270",
  "130_280",
  "130_290",
  "130_300",
  "130_310",
  "130_320",
  "130_330",
  "130_340",
  "130_350",
  "130_360",
  "130_370",
  "130_380",
  "130_390",
  "130_400",
  "130_410",
  "130_420",
  "130_430",
  "130_440",
  "130_450",
  "130_460",
  "130_470",
  "130_480",
  "130_490",
  "130_500",
  "130_510",
  "130_520",
  "130_530",
  "130_540",
  "130_550",
  "130_560",
  "130_570",
  "130_580",
  "140_200",
  "140_210",
  "140_220",
  "140_250",
  "140_270",
  "140_290",
  "140_310",
  "140_320",
  "140_330",
  "140_340",
  "140_350",
  "140_360",
  "140_370",
  "140_380",
  "140_390",
  "140_400",
  "140_410",
  "140_420",
  "140_430",
  "140_440",
  "140_460",
  "140_480",
  "140_490",
  "150_200",
  "150_210",
  "150_220",
  "150_250",
  "150_260",
  "150_270",
  "150_290",
  "150_310",
  "150_320",
  "150_330",
  "150_340",
  "150_350",
  "150_360",
  "150_370",
  "150_380",
  "150_390",
  "150_400",
  "150_410",
  "150_420",
  "150_430",
  "150_440",
  "150_460",
  "150_480",
  "150_490",
  "160_200",
  "160_210",
  "160_220",
  "160_250",
  "160_260",
  "160_270",
  "160_290",
  "160_310",
  "160_320",
  "160_330",
  "160_340",
  "160_350",
  "160_360",
  "160_370",
  "160_380",
  "160_390",
  "160_400",
  "160_410",
  "160_420",
  "160_430",
  "160_440",
  "160_460",
  "160_480",
  "160_490",
  "170_200",
  "170_210",
  "170_220",
  "170_250",
  "170_260",
  "170_270",
  "170_290",
  "170_310",
  "170_320",
  "170_330",
  "170_340",
  "170_350",
  "170_360",
  "170_370",
  "170_380",
  "170_390",
  "170_400",
  "170_410",
  "170_420",
  "170_430",
  "170_440",
  "170_460",
  "170_470",
  "170_480",
  "170_490",
  "180_200",
  "180_210",
  "180_220",
  "180_250",
  "180_270",
  "180_290",
  "180_310",
  "180_320",
  "180_330",
  "180_340",
  "180_350",
  "180_360",
  "180_370",
  "180_380",
  "180_390",
  "180_400",
  "180_410",
  "180_420",
  "180_430",
  "180_440",
  "180_460",
  "180_480",
  "180_490",
  "190_200",
  "190_210",
  "190_220",
  "190_250",
  "190_260",
  "190_270",
  "190_290",
  "190_310",
  "190_320",
  "190_330",
  "190_340",
  "190_350",
  "190_360",
  "190_370",
  "190_380",
  "190_390",
  "190_400",
  "190_410",
  "190_420",
  "190_430",
  "190_440",
  "190_460",
  "190_480",
  "190_490",
  "200_200",
  "200_210",
  "200_220",
  "200_250",
  "200_260",
  "200_270",
  "200_290",
  "200_310",
  "200_320",
  "200_330",
  "200_340",
  "200_350",
  "200_360",
  "200_370",
  "200_380",
  "200_390",
  "200_400",
  "200_410",
  "200_420",
  "200_430",
  "200_440",
  "200_460",
  "200_480",
  "200_490",
  "210_200",
  "210_210",
  "210_220",
  "210_250",
  "210_270",
  "210_290",
  "210_310",
  "210_320",
  "210_330",
  "210_340",
  "210_350",
  "210_360",
  "210_370",
  "210_380",
  "210_390",
  "210_400",
  "210_410",
  "210_420",
  "210_430",
  "210_440",
  "210_460",
  "210_470",
  "210_480",
  "210_490",
  "220_200",
  "220_210",
  "220_220",
  "220_250",
  "220_270",
  "220_290",
  "220_310",
  "220_320",
  "220_330",
  "220_340",
  "220_350",
  "220_360",
  "220_370",
  "220_380",
  "220_390",
  "220_400",
  "220_410",
  "220_420",
  "220_430",
  "220_440",
  "220_460",
  "220_470",
  "220_480",
  "220_490",
  "230_200",
  "230_210",
  "230_220",
  "230_250",
  "230_270",
  "230_290",
  "230_310",
  "230_320",
  "230_330",
  "230_340",
  "230_350",
  "230_360",
  "230_370",
  "230_380",
  "230_390",
  "230_400",
  "230_410",
  "230_420",
  "230_430",
  "230_440",
  "230_460",
  "230_480",
  "230_490",
  "30_200",
  "30_210",
  "30_220",
  "30_250",
  "30_270",
  "30_290",
  "30_310",
  "30_320",
  "30_330",
  "30_340",
  "30_350",
  "30_360",
  "30_370",
  "30_380",
  "30_390",
  "30_400",
  "30_410",
  "30_420",
  "30_430",
  "30_440",
  "30_460",
  "30_480",
  "30_490",
  "40_200",
  "40_210",
  "40_220",
  "40_250",
  "40_260",
  "40_270",
  "40_290",
  "40_310",
  "40_320",
  "40_330",
  "40_340",
  "40_350",
  "40_360",
  "40_370",
  "40_380",
  "40_390",
  "40_400",
  "40_410",
  "40_420",
  "40_430",
  "40_440",
  "40_460",
  "40_470",
  "40_480",
  "40_490",
  "50_200",
  "50_210",
  "50_220",
  "50_250",
  "50_260",
  "50_270",
  "50_290",
  "50_310",
  "50_320",
  "50_330",
  "50_340",
  "50_350",
  "50_360",
  "50_370",
  "50_380",
  "50_390",
  "50_400",
  "50_410",
  "50_420",
  "50_430",
  "50_440",
  "50_460",
  "50_480",
  "50_490",
  "60_200",
  "60_210",
  "60_220",
  "60_250",
  "60_260",
  "60_270",
  "60_290",
  "60_310",
  "60_320",
  "60_330",
  "60_340",
  "60_350",
  "60_360",
  "60_370",
  "60_380",
  "60_390",
  "60_400",
  "60_410",
  "60_420",
  "60_430",
  "60_440",
  "60_460",
  "60_480",
  "60_490",
  "70_200",
  "70_210",
  "70_220",
  "70_250",
  "70_270",
  "70_290",
  "70_310",
  "70_320",
  "70_330",
  "70_340",
  "70_350",
  "70_360",
  "70_370",
  "70_380",
  "70_390",
  "70_400",
  "70_410",
  "70_420",
  "70_430",
  "70_440",
  "70_460",
  "70_480",
  "70_490",
  "80_200",
  "80_210",
  "80_220",
  "80_250",
  "80_270",
  "80_290",
  "80_310",
  "80_320",
  "80_330",
  "80_340",
  "80_350",
  "80_360",
  "80_370",
  "80_380",
  "80_390",
  "80_400",
  "80_410",
  "80_420",
  "80_430",
  "80_440",
  "80_460",
  "80_480",
  "80_490",
  "90_200",
  "90_210",
  "90_220",
  "90_250",
  "90_260",
  "90_270",
  "90_290",
  "90_310",
  "90_320",
  "90_330",
  "90_340",
  "90_350",
  "90_360",
  "90_370",
  "90_380",
  "90_390",
  "90_400",
  "90_410",
  "90_420",
  "90_430",
  "90_440",
  "90_460",
  "90_480",
  "90_490"
 ]
reduction = 5

img_width = int(500 / reduction)
img_height = int(600 / reduction)

font = cv2.FONT_HERSHEY_SIMPLEX
# org
org = (100, 100)

# fontScale
fontScale = 0.75

# Blue color in BGR
color = (0, 0, 255)

# Line thickness of 2 px
thickness = 1


def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


while (True):
    ret, frame = cap.read()
    if (ret):

        # adding filled rectangle on each frame
        # if random.randint(0, 9) < 1:
        #    id = uuid.uuid1()
        #    cv2.imwrite(f"temp\\{id}.png", frame)
        # frame = cv2.transpose(frame)
        color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        pil_image = Image.fromarray(color_converted)
        pil_image = pil_image.crop((0, 0, 500, 600))
        img = pil_image.resize((img_width, img_height), resample=Image.Resampling.NEAREST)
        #img = pil_image

        img = np.array([np.array(img)])

        #model = tf.keras.Model(inputs=model2.inputs, outputs=model2.layers[1].output)

        prediction = model2.predict(img)
        #c1img = Image.fromarray((prediction[0][:, :, 9:12] * 255).astype(np.uint8))
        #c2img = Image.fromarray((prediction[0][:, :, 3:6] * 255).astype(np.uint8))
        #c3img = Image.fromarray((prediction[0][:, :, 6:9] * 255).astype(np.uint8))
        #prediction = model2.predict(img)
        argm = np.argmax(prediction)
        y_prediction = class_names[argm]
        pres = y_prediction.split('Audit_History')
        frame = cv2.transpose(frame)
        '''
        y0, dy = 200, 20
        paylaod = "Model Output: \n" + json.dumps(list(prediction[0].astype(str)), indent=1)
        for i, line in enumerate(paylaod.split('\n')):
            y = y0 + i * dy
            if i-2 == argm:
                color = (0, 255, 0)
            else:
                color = (0,0,255)

            frame = cv2.putText(frame, line, (1200, y), font, fontScale, color, thickness, cv2.LINE_AA)
        '''
        frame = cv2.putText(frame, 'AI trying to locate the y axis of the waypoint bar', (100, 100), font, 2,
                            (0, 255, 0), 2, cv2.LINE_AA)

        #frame[0:600, 0:500] = c1img
        #frame[0:600, 500:1000] = c1img
        #frame[0:600, 1000:1500] = c3img

        cv2.line(frame, (0, int(pres[1]) + 4), (1000, int(pres[1]) + 4),
                 (0, 255, 0), thickness=2)
        cv2.line(frame, (int(pres[0]) + 4, 0), (int(pres[0])+4, 1000),
                 (0, 255, 0), thickness=2)


        # writing the new frame in output
        output.write(frame)
        cv2.imshow("output", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    else:
        break

cv2.destroyAllWindows()
output.release()
cap.release()