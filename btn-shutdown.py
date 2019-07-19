#!/usr/bin/env python

import time
import os
import buttonshim as btn
import signal

btn.set_pixel(0, 0, 0)

@btn.on_hold(btn.BUTTON_C, hold_time=5)
def handler(button):
	for i in range(0, 9):
		for j in range(0, 255, 32):
			btn.set_pixel(j, 0, 0)
			time.sleep(0.000)
		for j in range(255, 0, -32):
			btn.set_pixel(j, 0, 0)
			time.sleep(0.000)
	for i in range(0, 1):
		for j in range(0, 255, 32):
			btn.set_pixel(j, 0, 0)
			time.sleep(0.000)
		time.sleep(3)
		for j in range(255, 0, -32):
			btn.set_pixel(j, 0, 0)
			time.sleep(0.000)
	time.sleep(5)
	os.system("sudo shutdown -h now")

signal.pause()




