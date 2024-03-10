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
row_pins = [board.GP20, board.GP21, board.GP22, board.GP19, board.GP18, board.GP17, board.GP16]
for row in row_pins:
    row_key = digitalio.DigitalInOut(row)
    row_key.direction = digitalio.Direction.OUTPUT
    rows.append(row_key)

cols = []   # Alternatively, use GP23 in place of 15 if it acts "funky"
col_pins = [board.GP15, board.GP14, board.GP13, board.GP12, board.GP11, board.GP10, board.GP9, board.GP8, board.GP7, board.GP6, board.GP4, board.GP3, board.GP2, board.GP0, board.GP1 ]
for col in col_pins:
    col_key = digitalio.DigitalInOut(col)
    col_key.direction = digitalio.Direction.INPUT
    col_key.pull = digitalio.Pull.DOWN
    cols.append(col_key)

keymap = [
          [None, None, None, None, None, None, None, None, None, ConsumerControlCode.VOLUME_DECREMENT, ConsumerControlCode.MUTE, ConsumerControlCode.VOLUME_INCREMENT, None, None, None],
          [Keycode.ESCAPE, Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5, Keycode.F6, Keycode.F7, Keycode.F8, Keycode.F9, Keycode.F10, Keycode.F11, Keycode.F12, Keycode.PRINT_SCREEN, None],
          [Keycode.GRAVE_ACCENT, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO, Keycode.MINUS, Keycode.EQUALS, Keycode.BACKSPACE, Keycode.DELETE],
          [Keycode.TAB, Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T, Keycode.Y, Keycode.U, Keycode.I, Keycode.O, Keycode.P, Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.BACKSLASH, Keycode.PAGE_UP],
          [Keycode.CAPS_LOCK, Keycode.A, Keycode.S, Keycode.D, Keycode.F, Keycode.G, Keycode.H, Keycode.J, Keycode.K, Keycode.L, Keycode.SEMICOLON, Keycode.QUOTE, Keycode.ENTER, None, Keycode.PAGE_DOWN],
          [Keycode.LEFT_SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V, Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD, Keycode.FORWARD_SLASH, Keycode.RIGHT_SHIFT, Keycode.UP_ARROW, None, Keycode.END],
          [Keycode.LEFT_CONTROL, Keycode.GUI, Keycode.LEFT_ALT, None, None, Keycode.SPACE, None, None, Keycode.RIGHT_ALT, Keycode.RIGHT_GUI, Keycode.RIGHT_CONTROL, Keycode.LEFT_ARROW, Keycode.DOWN_ARROW, None, Keycode.RIGHT_ARROW]
          ]

while True:
    for r in rows:
        r.value=1 # set row r to high
        for c in cols:
            if c.value: # if a keypress is detected
                key = keymap[rows.index(r)][cols.index(c)]
                while c.value: # wait until key is released
                    time.sleep(0.01)
                # print(type(key)) # more debug
                if(r == 0): # We're just gonna hard code that the top row is for media controls
                    cc.send(key)
                else:
                    kbd.press(key)
                # print(f"Key press as ({rows.index(r)}, {cols.index(c)})") # for debug
                kbd.release_all()
        r.value=0
