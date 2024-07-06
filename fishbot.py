import os
import sys
from datetime import datetime
import random
import time
import cv2
import mss as mss
import numpy as np
import pyautogui as gui
import pyttsx3
from matplotlib import pyplot as plt
from pynput import keyboard

engine = pyttsx3.init()
engine.runAndWait()

diff = None
tresh = None


def prints(s):
    engine.say(s)
    engine.runAndWait()
    print(s)


def on_press(key):
    try:
        if key.char == "p":
            pass
            # os._exit(0)
    except:
        pass


listener = keyboard.Listener(on_press=on_press)
listener.start()


def catch_fish(x, y):
    gui.moveTo(x, y, random.uniform(0.3, 0.4), gui.easeOutQuad)
    gui.rightClick()


def attempt_catch(mon, x0, y0, x1, y1):
    last = None
    start = datetime.now()

    while True:
        im = np.array(screen.grab(mon))
        im = im[y0:y1, x0:x1, :]
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        _, splash = cv2.threshold(im_gray, 255 - diff, 255, cv2.THRESH_BINARY)
        spc = splash.copy()
        if last is not None:
            splash = splash - last
            white = np.sum(splash / 255)

            if white > 0:
                print(f'White: {white}')

            if white > tresh:
                kernel = np.ones((3, 3), np.uint8)
                splash = cv2.dilate(splash, kernel, iterations=1)
                contours, hierarchy = cv2.findContours(splash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                if len(contours) != 0:
                    c = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(c)
                    x = x + w / 2
                    y = y + h / 2
                    catch_fish(x0 + x, y0 + y)
                    return True

        last = spc
        now = datetime.now()
        if (now - start).total_seconds() > 30:
            return False


def experimental(mon):
    template = cv2.imread('78155.png', cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    kernel = np.ones((5, 5), np.float32) / 25

    gui.hotkey('ctrl', 'alt', 'z')
    time.sleep(0.5)
    img1 = cv2.cvtColor(np.array(screen.grab(mon)), cv2.COLOR_RGBA2RGB)

    gui.press('o')
    time.sleep(0.5)

    img2 = cv2.cvtColor(np.array(screen.grab(mon)), cv2.COLOR_RGBA2RGB)

    img1 = cv2.filter2D(img1, -1, kernel).astype(float)
    img2 = cv2.filter2D(img2, -1, kernel).astype(float)

    dif = img2 - img1
    dif[dif < 0] = 0

    hsv = cv2.cvtColor(dif.astype(np.uint8), cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 5])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    dif[np.where(mask0 == 0)] = 0

    blue = dif[:, :, 0]
    green = dif[:, :, 1]
    red = dif[:, :, 2]

    prints('Thresholding')

    for t in (50, 0, -5):
        _, mask = cv2.threshold(red, t, 255, cv2.THRESH_BINARY)
        mask = mask.astype(np.uint8)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(dif, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 2)
            prints(f'Found threshold at: {t}')
            cv2.imwrite('test.png', dif)
            return attempt_catch(mon, x - 20, y - 30, x + w + 20, y + h + 10)

    return False


def bober(mon):
    template = cv2.imread('fishing_target.png', cv2.IMREAD_COLOR)
    w, h, _ = template.shape

    gui.hotkey('ctrl', 'alt', 'z')
    gui.press('o')

    time.sleep(0.5)

    for i in range(10):
        im = np.array(screen.grab(mon))
        im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        im = im.astype(np.uint8)

        res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # threshold = 0.8
        # loc = np.where(res >= threshold)
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        if max_val >= threshold:
            cx, cy = max_loc

            x0 = cx - 30
            y0 = cy - 30

            x1 = cx + 40
            y1 = cy + 30

            cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)
            cv2.imwrite('res.png', im)
            return attempt_catch(mon, x0, y0, x1, y1)

    return False


def main_loop(mon):
    while True:
        # gui.hotkey('ctrl', 'alt', 'z')
        # gui.press('o')

        if bober(mon):
            prints("Attempt successful")
        else:
            prints("Attempt failed")

        gui.hotkey('ctrl', 'alt', 'z')
        t = random.uniform(3.0, 4.0)
        prints(f"Waiting for {t:.1f} seconds")
        time.sleep(t)


if __name__ == '__main__':
    diff = int(sys.argv[1])
    tresh = int(sys.argv[2])

    prints(f"Starting in {5}...")
    for i in range(4, 0, -1):
        prints(f"{i}...")

    prints("Initializing")
    with mss.mss() as screen:
        mon = screen.monitors[0]
        main_loop(mon)
        # bober(mon)
