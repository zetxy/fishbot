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
from pynput import keyboard
from pynput.keyboard import Key

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
            os._exit(0)
    except:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()


def catch_fish(x, y):
    gui.moveTo(x, y)
    t = random.random() * 0.8
    time.sleep(t)
    gui.rightClick()


def attempt_catch(mon):
    last = None
    start = datetime.now()
    while True:
        im = np.array(screen.grab(mon))
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        _, splash = cv2.threshold(im_gray, 255 - diff, 255, cv2.THRESH_BINARY)
        spc = splash.copy()
        if last is not None:
            splash = splash - last
            white = np.sum(splash / 255)
            if white > tresh:
                kernel = np.ones((3, 3), np.uint8)
                splash = cv2.dilate(splash, kernel, iterations=1)
                contours, hierarchy = cv2.findContours(splash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                if len(contours) != 0:
                    c = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(c)
                    x = x + w / 2
                    y = y + h / 2
                    catch_fish(x, y)
                    return True

        last = spc
        now = datetime.now()
        if (now - start).total_seconds() > 30:
            return False


def main_loop(mon):
    while True:
        gui.hotkey('ctrl', 'alt', 'z')
        gui.press('o')

        if attempt_catch(mon):
            prints("Attempt successful")
        else:
            prints("Attempt failed")

        gui.hotkey('ctrl', 'alt', 'z')
        t = random.random() * 8
        prints(f"Waiting for {t:.1f} seconds")


if __name__ == '__main__':
    diff = int(sys.argv[1])
    tresh = int(sys.argv[2])

    prints(f"Starting in {10}...")
    for i in range(9, 0, -1):
        prints(f"{i}...")

    prints("Initializing main routine")
    with mss.mss() as screen:
        mon = screen.monitors[0]
        main_loop(mon)
