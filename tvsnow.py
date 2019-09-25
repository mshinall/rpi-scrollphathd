#!/usr/bin/env python

import random
import time
import scrollphathd as scr
from scrollphathd.fonts import font5x7
import buttonshim as btn
import signal

delay = 0.000
delay2 = delay * 5
delay3 = delay * 100
bright = 0.3
bright2 = bright * 2
title = "TV Snow"
[width, height] = scr.get_shape()
quantity = (width * height) / 2

scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)

btn.set_pixel(0,0,0)

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
		#scr.clear()
		g = random.uniform(0.0, 0.2)
		for x in range(width):
			for y in range(height):
				b = random.uniform(0.2, 0.5)
				scr.set_pixel(x=x, y=y, brightness=b+g)

		scr.show()
		time.sleep(delay)

def stop():
	scr.clear()
	scr.show()

try:
	show_title()
	main_loop()
except:
	stop()
finally:
	stop()
