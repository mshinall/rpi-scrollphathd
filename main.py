#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import re
import signal
import time
from threading import Thread
from numpy import interp
import buttonshim as btn
import scrollphathd as scr
from scrollphathd.fonts import font5x7

delay = 0.005
delay2 = delay * 5
delay3 = delay * 100
bright0 = 0
bright = 0.3
bright1 = bright
bright2 = bright * 2
bright3 = bright * 3
[width, height] = scr.get_shape()
signal_high = 0
signal_low = width-1
count = 0

is_busy = False
last_func = None
break_loop = False

threads = []

scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)

btn.set_pixel(0,0,0)

wth_summary_map = {
	"snow":                "Snow",
	"sleet":               "Sleet",
	"rain":                "Rain",
	"fog":                 "Fog",
	"cloudy":              "Cloudy",
	"partly-cloudy-day":   "Partly Cloudy",
	"partly-cloudy-night": "Partly Cloudy",
	"clear-day":           "Clear",
	"clear-night":         "Clear",
	"wind":                "Wind"
}

def blink():
	btn.set_pixel(0,127,0)
        time.sleep(0.1)
        btn.set_pixel(0,0,0)

def show_title(title):
	scr.write_string(title, x=0, y=0, brightness=bright2)
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

def tv_main_loop():
	while True:
		if break_loop:
			break
		#scr.clear()
		g = random.uniform(0.0, 0.2)
		for x in range(width):
			for y in range(height):
				b = random.uniform(0.2, 0.5)
				scr.set_pixel(x=x, y=y, brightness=b+g)

		scr.show()
		time.sleep(delay)

def wifi_info():
	global signal_high, signal_low
	out = os.popen('echo `iwconfig wlan0 | egrep "ESSID|Link Quality"`').read()
	m = re.search('^.*ESSID:"([\w.-]*)".*Link Quality=(\d*)/(\d*).*$', out)
	id = m.group(1)
	n = int(m.group(2))
	d = int(m.group(3))
	s = int(interp(n, [0, d], [0, width]))
	if(s > signal_high):
		signal_high = s
	if(s < signal_low):
		signal_low = s
	#print(id + " " + str(n) + "/" + str(d) + " " + str(s) + "/" + str(width))
	return [id, s]

def wifi_show_ssid():
	[id, s] = wifi_info()
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

def wifi_init_meter():
	for i in range(0, 18):
        	scr.fill(brightness=bright, x=0, y=0, width=i, height=height)
        	scr.show()
        	time.sleep(delay2)

	for j in range(0, 18):
		scr.fill(brightness=bright0, x=width-j, y=0, width=j, height=height)
        	scr.show()
        	time.sleep(delay2)

def wifi_main_loop():
	while True:
		if break_loop:
			break
		global count, signal_high, signal_low
		scr.clear()
		[id, s] = wifi_info()
		scr.fill(brightness=bright1, x=0, y=1, width=s-1, height=height-2)
		scr.fill(brightness=bright3, x=s-1, y=1, width=1, height=height-2)
		scr.fill(brightness=bright2, x=signal_high-1, y=0, width=1, height=height-1)
		scr.fill(brightness=bright2, x=signal_low-1, y=1, width=1, height=height-1)

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

def bnc_main_loop():
	x = 0
	y = 0
	xd = 1
	yd = 1
	scr.clear()
	scr.set_pixel(x=x, y=y, brightness=bright2)
	scr.show()
	time.sleep(delay)
	while True:
		if break_loop:
			break
		x = x + xd
		if(x >= width - 1) or (x <= 0):
			xd = -xd

		y = y + yd
		if(y >= height - 1) or (y <= 0):
			yd = -yd

		scr.clear()
		scr.set_pixel(x=x, y=y, brightness=bright2)
		scr.show()
		time.sleep(delay)

def str_main_loop():
	while True:
		if break_loop:
			break
		scr.clear()
		scr.show()
		d = random.uniform(0.005, 0.02)
		time.sleep(d)
		scr.fill(brightness=bright3, x=0, y=0, width=width, height=height)
		scr.show()
		d = random.uniform(0.005, 0.02)
		time.sleep(d)

def busy():
	global is_busy
	if is_busy:
		return True
	else:
		is_busy = True
		return False

def free():
	global is_busy
	if is_busy:
		is_busy = False
		return False
	else:
		return True

def startProc(func):
	process = Thread(target=func)
	process.start()
	threads.append(process)

def stopProcs():
	global threads
	global break_loop
	break_loop = True
	for process in threads:
		threads.remove(process)
		process.join()
	break_loop = False

def do(func):
	global last_func
	global break_loop
	if busy():
		return
		#print("busy: " + func.__name__)
	#print("free: " + func.__name__)
	blink()
	btn.set_pixel(0, 0, 127)
	last_func = func
	stopProcs()
	scr.clear()
	scr.show()
	startProc(func)
	btn.set_pixel(0, 0, 0)
	free()

def wifi():
	show_title("WIFI Signal")
	wifi_show_ssid()
	wifi_init_meter()
	wifi_main_loop()

def tv():
	show_title("TV Snow")
	tv_main_loop()

def strobe():
	show_title("Strobe Light")
	str_main_loop()

def bounce():
	show_title("Bouncing Ball")
	bnc_main_loop()

@btn.on_hold(btn.BUTTON_E, hold_time=1)
def handler(button):
	do(bounce)

@btn.on_hold(btn.BUTTON_D, hold_time=1)
def handler(button):
	do(strobe)

@btn.on_hold(btn.BUTTON_B, hold_time=1)
def handler(button):
	do(tv)

@btn.on_hold(btn.BUTTON_A, hold_time=1)
def handler(button):
	do(wifi)

try:
	do(bounce)
	signal.pause()
except:
	scr.clear()
	scr.show()
	exit()
