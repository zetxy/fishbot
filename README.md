# Fishbot

### Requirements

```
python 3.x - recommended python 3.7
```

On Ubuntu/Linux
```
sudo apt-get install python3.7
```

On Windows, a bit of hand job is required.
https://www.python.org/downloads/release/python-379/

Navigate to the bottom of the page and download an installer. You probably want to download the
`Windows x86-64 executable installer`.
You might also need to add python executable to your Windows PATH.

### Installation
In the root folder of this project, run this in your command line:
```
pip3 install -r requirements.txt
```

If for some reason pip is not working, please check this manual.
https://www.liquidweb.com/kb/install-pip-windows/


### Description
This simple bot simulates the player in order to catch fish in
World of Warcraft. The bot works only by performing image analysis using
the computer vision library OpenCV.

The bot reacts not on the bobber, but on the splash, by filtering mostly white
pixels. This also means that there should not be much white objects in the scene.

Higher ambient light is also beneficial.

Some requirements must be met in order to use this bot.
1. Have Fishing bound to F10 keybind. The bot will attempt to press this key in order to start
fishing.
2. Be in first person mode to minimize occlusion and get the best performance from your bot.
3. Pick a static scene. In order to maximize the accuracy, there should be nothing moving around 
that could tamper with the detection.
4. Have WoW in ultra resolution mode.
5. Have auto loot enabled.

### Usage
First of all, place your character in a place, suitable for fishing. After that you can
run the program. After initial countdown, the bot will start catching fish.

After each attempt, UI is temporarily restored - e.g. in order to check chat messages.
To turn off the bot, simply hit F9 and wait for a while.

You can run it like this 
```bash
python fishbot.py [tolerance] [tresh]
```

Tolerance is the pixel saturation amount which will be taken into account. It should be and
integer between 1 and 254. Recommended is 15. Increasing the tolerance may result in more fish caught, but also 
increases the amount of false positives produced.

Again, tresh means, how many white new white pixels should be considered enough.
This value is dependent on the scene, time of day. Set it accordingly to your preferences. 25 is considered to be
the default value right now. You can lower it if you think that too much fish are being missed.

So example usage could be
```
python fishbot.py 15 25
```