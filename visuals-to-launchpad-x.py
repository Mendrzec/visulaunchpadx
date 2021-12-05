import time

import cv2
import mss
import numpy
import mido


LAUNCHPADX_PORTS={'in':'LPX MIDI 1', 'out':'MIDIOUT2 (LPX MIDI) 2'}
SYSEX_START = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0C, 0x03]
SYSEX_END = 0xf7
LAUNCHPADX_NOTE = [
    [81, 82, 83, 84, 85, 86, 87, 88],
    [71, 72, 73, 74, 75, 76, 77, 78],
    [61, 62, 63, 64, 65, 66, 67, 68],
    [51, 52, 53, 54, 55, 56, 57, 58],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [31, 32, 33, 34, 35, 36, 37, 38],
    [21, 22, 23, 24, 25, 26, 27, 28],
    [11, 12, 13, 14, 15, 16, 17, 18]
]

def gen_colorspec(x, y, bgr):
    return [0x03, LAUNCHPADX_NOTE[y][x], bgr[2], bgr[1], bgr[0]]

def colorspecs_to_msg(colorspecs: list):
    result = []
    result.extend(SYSEX_START)
    for colorspec in colorspecs:
        result.extend(colorspec)
    result.append(SYSEX_END)
    return mido.Message.from_bytes(result)


with mido.open_output(LAUNCHPADX_PORTS['out']) as outport:
    with mss.mss() as sct:
        # Customize those values to ajust captured area roughly
        # Correct in runtime using w,s,a,d controls
        monitor = {"top": 170, "left": 550, "width": 700, "height": 700}

        while "Screen capturing":
            img = numpy.array(sct.grab(monitor))

            cv2.namedWindow('CV2normal', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('CV2normal', 200, 200)
            cv2.imshow('CV2normal', img)

            downsized = (cv2.resize(img, (8,8), interpolation = cv2.INTER_AREA)/2).astype(numpy.uint8)
            cv2.namedWindow('CVdownsized', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('CVdownsized', 200, 200)
            cv2.imshow('CVdownsized', downsized)

            colorspecs = []
            for y, column in enumerate(downsized):
                for x, rgba in enumerate(column):
                    colorspecs.append(gen_colorspec(x, y, rgba[0:3]))
            msg = colorspecs_to_msg(colorspecs)
            outport.send(msg)

            time.sleep(0.025)

            wait_key = cv2.waitKey(25) & 0xFF
            if wait_key == ord("q"):
                cv2.destroyAllWindows()
                break
            elif wait_key == ord('a'):
                monitor["left"] -= 2
            elif wait_key == ord('d'):
                monitor["left"] += 2
            elif wait_key == ord('w'):
                monitor["top"] -= 2
            elif wait_key == ord('s'):
                monitor["top"] += 2
