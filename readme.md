# visulaunchpadx

1. capture screen fragment and stream it to launchpad x
2. enjoy colorful ambience

## prepare
* python 3.7
* cv2
* mido
* mss
* numpy
* rtmidi

## run
```sh
python visuals-to-launchpad-x.py
```
* press `q` to stop
* move capturing window in runtime using `a s d w`


default capture window args are `monitor = {"top": 170, "left": 550, "width": 700, "height": 700}` which is approximately where a yt player is in your browser
