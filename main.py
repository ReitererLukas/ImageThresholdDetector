import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys


HSV_LOWER=[0,0,0]
HSV_UPPER=[255,255,255]
FRAME=None
CROP=False

def show_frame(window_name):
    lower: list = np.array(HSV_LOWER, dtype="uint8")
    upper: list = np.array(HSV_UPPER, dtype="uint8")

    frame = FRAME
    if CROP:
        original_width = FRAME.shape[1]
        original_height = FRAME.shape[0]

        new_width = 800
        new_height = int(new_width / original_width * original_height)
        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow(window_name, result)

    pass

def edit_hsv_value(value, scheme, index):
    if scheme == 'upper':
        HSV_UPPER[index] = value
        pass
    elif scheme == 'lower':
        HSV_LOWER[index] = value
        pass


    pass

def change_frame(value, videos):
    global FRAME
    FRAME = videos[value]
    pass

def button_pressed(value):
    global CROP
    CROP = True if value == 1 else False

def createTrackBars(window_name: str):
    cv2.createTrackbar("Crop?", window_name, 0, 1, lambda v: button_pressed(v))
    cv2.createTrackbar('H UPPER', window_name, HSV_UPPER[0], 255, lambda v: edit_hsv_value(v, 'upper', 0))
    cv2.createTrackbar('S UPPER', window_name, HSV_UPPER[1], 255, lambda v: edit_hsv_value(v, 'upper', 1))
    cv2.createTrackbar('V UPPER', window_name, HSV_UPPER[2], 255, lambda v: edit_hsv_value(v, 'upper', 2))
    cv2.createTrackbar('H LOWER', window_name, HSV_LOWER[0], 255, lambda v: edit_hsv_value(v, 'lower', 0))
    cv2.createTrackbar('S LOWER', window_name, HSV_LOWER[1], 255, lambda v: edit_hsv_value(v, 'lower', 1))
    cv2.createTrackbar('V LOWER', window_name, HSV_LOWER[2], 255, lambda v: edit_hsv_value(v, 'lower', 2))
    pass

def get_file() -> str:
    Tk().withdraw()
    file = askopenfilename()
    if file == '':
        sys.exit()
        pass
    return file

def loop(window_name):
    while(True):
        show_frame(window_name)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        pass

    cv2.destroyAllWindows()
    sys.exit()
    pass

def threshold_image():
    window_name = "Image Threshold"
    cv2.namedWindow(window_name)
    createTrackBars(window_name)
    loop(window_name)
    pass


def threshold_video(video):
    global FRAME

    videos = []
    success, frame = video.read()
    FRAME = frame
    while success:
        videos.append(frame)
        success, frame = video.read()


    window_name = "Video Threshold"
    cv2.namedWindow(window_name)
    createTrackBars(window_name)
    cv2.createTrackbar("Frame",window_name,0,len(videos),lambda value: change_frame(value, videos))
    loop(window_name)
    pass


if __name__ == "__main__":
    file = get_file()

    image = cv2.imread(file)

    if image is not None:
        FRAME = image
        threshold_image()
    else:
        video = cv2.VideoCapture(file)
        if video is not None:
            threshold_video(video)

    print("File not valid")
    pass