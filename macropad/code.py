import usb_hid
import board
import digitalio
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

rows = []
row_pins = [board.GP16, board.GP17, board.GP18]
for row in row_pins:
    row_key = digitalio.DigitalInOut(row)
    row_key.direction = digitalio.Direction.OUTPUT
    rows.append(row_key)

cols = []
col_pins = [board.GP15, board.GP14, board.GP13]
for col in col_pins:
    col_key = digitalio.DigitalInOut(col)
    col_key.direction = digitalio.Direction.INPUT
    col_key.pull = digitalio.Pull.DOWN
    cols.append(row_key)

keymap = [[Keycode.ESCAPE, Keycode.ONE, Keycode.TWO],
          [Keycode.A, Keycode.B, Keycode.C],
          [Keycode.CONTROL, Keycode.SPACE, Keycode.SHIFT]]

while True:
    for r in rows:
        r.value=1 # set row r to high
        for c in cols:
            if c.value: # if a keypress is detected
                while c.value: # wait until key is released
                    time.sleep(0.01)
                kbd.press(keymap[rows.index(r)][cols.index(c)])
                print(f"Key press as ({rows.index(r)}, {cols.index(c)})")
                kbd.release_all()
        r.value=0


