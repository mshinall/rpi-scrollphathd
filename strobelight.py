#!/usr/bin/env python

import random
import time
import scrollphathd as scr
from scrollphathd.fonts import font5x7

delay = 0.000
delay2 = delay * 5
delay3 = delay * 100
bright = 0.3
bright2 = bright * 2
bright3 = 1.0
title = "Strobe Light"
[width, height] = scr.get_shape()
quantity = (width * height) / 2

scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)

def show_title():
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

def main_loop():
	while True:
		scr.clear()
		scr.show()
		d = random.uniform(0.005, 0.02)
		time.sleep(d)
		scr.fill(brightness=bright3, x=0, y=0, width=width, height=height)
		scr.show()
		d = random.uniform(0.005, 0.02)
		time.sleep(d)

try:
	show_title()
	main_loop()
except:
	scr.clear()
	scr.show()
finally:
	scr.clear()
	scr.show()
