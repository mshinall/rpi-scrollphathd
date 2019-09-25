#!/usr/bin/env python

import random
import time
import scrollphathd as scr
from scrollphathd.fonts import font5x7

delay = 0.001
delay2 = delay * 5
delay3 = delay * 100
bright = 0.3
bright2 = bright * 2
bright3 = 1.0
title = "Bouncing Ball"
[width, height] = scr.get_shape()
quantity = (width * height) / 2

scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)

def bnc_show_title():
	scr.write_string(title, x=0, y=0, brightness=bright)
	scr.show()
	time.sleep(delay*20)

	[bw, bh] = scr.get_buffer_shape()
	for y in [1, -1]:
	        for x in range(0, bw-width-1):
        	        scr.scroll(x=y, y=0)
                	scr.show()
                	time.sleep(delay)
                time.sleep(delay3)
	scr.clear()
	scr.show()

def bnc_main_loop():
	x = 0
	y = 0
	xd = 1
	yd = 1
	scr.clear()
	scr.set_pixel(x=x, y=y, brightness=bright)
	scr.show()
	time.sleep(delay)

	while True:
		x = x + xd
		if(x >= width - 1) or (x <= 0):
			xd = -xd

		y = y + yd
		if(y >= height - 1) or (y <= 0):
			yd = -yd

		scr.clear()
		scr.set_pixel(x=x, y=y, brightness=bright)
		scr.show()
		time.sleep(delay)

try:
	bnc_show_title()
	bnc_main_loop()
except:
	scr.clear()
	scr.show()
finally:
	scr.clear()
	scr.show()
