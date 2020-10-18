import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import cv2
import time
import requests
import pyautogui
import matplotlib.pyplot as plt
import numpy as np
from fer import FER


emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
room_id = 69

while True:
    image = np.array(pyautogui.screenshot())
    detector = FER(mtcnn=True)
    results = detector.detect_emotions(image)
    # print(results)

    emotion_vec = []
    for e in emotions:
        total_emotion = 0
        for r in results:
            total_emotion += r["emotions"][e]
        if results:
            total_emotion /= len(results)
            emotion_vec.append(total_emotion)

    data = {k:v for k, v in zip(emotions, emotion_vec)}
    data["room_id"] = room_id
    res = requests.post("http://18.223.166.141:8080/emotions", data=data)
    if res.ok:
        print("sent to server")
    else:
        print(res.status_code)
    print(data)
