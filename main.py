### Author: Ben Caller
### Description: Your badge is now a USB mouse. Tilt to move. A & B to click. Joystick scrolls.
### Category: Other
### License: GPLv3
### Appname: USB Mouse
### reboot-before-run: True
### USB-mode: VCP+HID

import pyb
import buttons
import ugfx
from os import sep, remove
from imu import IMU


TILT_SENSITIVITY = 25


def click():
    # Button data is a bitmask
    return buttons.is_pressed('BTN_A') + 2 * buttons.is_pressed('BTN_B') + 4 * buttons.is_pressed('JOY_CENTER')


def joystick_scroll(factor=1):
    if buttons.is_pressed('JOY_UP'):
        return factor
    elif buttons.is_pressed('JOY_DOWN'):
        return -factor
    return 0


ugfx.init()
buttons.init()
if 'HID' in pyb.usb_mode():
    # HID mode rather than mass storage
    ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)
    ugfx.text(30, 30, "USB Mouse mode by bcaller", ugfx.html_color(0xFF7C11))
    accelerometer = IMU()
    hid = pyb.USB_HID()
    transform = lambda a: int(a * TILT_SENSITIVITY)
    
    def mouse_update():
        accel = accelerometer.get_acceleration()
        # Buttons, x, y, scroll
        hid.send((click(), transform(accel['x']), transform(accel['y']), joystick_scroll()))
    
    while True:
        mouse_update()
        pyb.delay(20)
else:
    # Not a HID, press B and reset
    ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)
    ugfx.text(30, 30, "Error, not in HID mode. Press B to reset.", ugfx.html_color(0xFF7C11))
    while True:
        if buttons.is_pressed('BTN_B'):
            pyb.hard_reset()
        pyb.delay(10)
