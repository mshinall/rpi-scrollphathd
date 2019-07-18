#!/usr/bin/env python

import os
import time
import re
from numpy import interp
import scrollphathd as scr
from scrollphathd.fonts import font5x7

delay = 0.005
delay2 = delay * 5
delay3 = delay * 100
bright = 0.3
bright2 = bright * 2
signal = 0
count = 0
title = "WIFI Signal Meter"
[width, height] = scr.get_shape()

scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)

def winfo():
	out = os.popen('echo `iwconfig wlan0 | egrep "ESSID|Link Quality"`').read()
	m = re.search('^.*ESSID:"([\w.]*)".*Link Quality=(\d*)/(\d*).*$', out)
	id = m.group(1)
	n = int(m.group(2))
	d = int(m.group(3))
	s = int(interp(n, [0, d], [0, width]))
	global signal
	if(s > signal):
		signal = s
	#print(id + " " + str(n) + "/" + str(d) + " " + str(s) + "/" + str(width))
	return [id, s]

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

def show_ssid():
	[id, s] = winfo()
	scr.write_string(id, x=0, y=0, brightness=bright)
	scr.show()
	time.sleep(delay3)

	[bw, bh] = scr.get_buffer_shape()
	for i in range(0,2):
		for y in [1, -1]:
			for x in range(0, bw-width-1):
				scr.scroll(x=y, y=0)
				scr.show()
				time.sleep(delay)
			time.sleep(delay3)

	scr.clear()
	scr.show()

def init_meter():
	for i in range(0, 17):
        	scr.fill(brightness=bright, x=0, y=0, width=i, height=height)
        	scr.fill(brightness=bright2, x=i, y=0, width=1, height=height)
        	scr.show()
        	time.sleep(delay2)


def main_loop():
	while True:
		global count
		global signal
		scr.clear()
		[id, s] = winfo()
		scr.fill(brightness=bright, x=0, y=0, width=s-1, height=height)
		scr.fill(brightness=bright2, x=s-1, y=0, width=1, height=height)
		if(s < signal):
			scr.fill(brightness=bright, x=signal-1, y=0, width=1, height=height)

		if(count > 0 and count <=9 ):
			scr.set_pixel(x=0, y=3, brightness=bright)
		elif(count > 9 and count <= 19):
			#scr.clear_rect(0, 0, 1, 1)
			scr.set_pixel(x=0, y=3, brightness=bright2)
		elif(count >= 19):
			count = 0
		count = count + 1	

		scr.show()
		time.sleep(delay)

try:
	show_title()
	show_ssid()
	init_meter()
	main_loop()
except:
	scr.clear()
	scr.show()
finally:
	scr.clear()
	scr.show()







