#!/usr/bin/env python

import random
import time
import scrollphathd as scr
from scrollphathd.fonts import font5x7
import buttonshim as btn
import signal
import os

delay = 0.005
delay3 = delay * 100
bright0 = 0.0
bright = 0.3
bright1 = bright
bright2 = bright * 2
bright3 = bright * 3
[width, height] = scr.get_shape()

c = 0

shp_y = 3
shp_y2 = 3
blt_x = 0
blt_x2=0
blt_y = 0
blt_y2 = 0
trg_x = 0
trg_x2 = 0
trg_y = 0
trg_y2 = 0

scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)

btn.set_pixel(0,0,0)

def show_msg(msg):
	scr.clear()
	scr.write_string(msg, x=0, y=0, brightness=bright)
	scr.show()
	time.sleep(delay*20)

	[bw, bh] = scr.get_buffer_shape()
	for y in [1, -1, 1]:
	        for x in range(0, bw-width-1):
        	        scr.scroll(x=y, y=0)
                	scr.show()
                	time.sleep(delay)
                time.sleep(delay3)
	scr.clear()
	scr.show()

def draw_pixel(x, y, b):
	if(x >= 0 and y >= 0 and x <= width-1 and y <= height-1):
		scr.set_pixel(x=x, y=y, brightness=b)

def draw_ship():
	global shp_y, shp_y2
	draw_pixel(0, shp_y2-1, bright0)
	draw_pixel(0, shp_y2, bright0)
	draw_pixel(0, shp_y2+1, bright0)
	draw_pixel(1, shp_y2, bright0)

	shp_y2 = shp_y

	draw_pixel(0, shp_y-1, bright)
	draw_pixel(0, shp_y, bright)
	draw_pixel(0, shp_y+1, bright)
	draw_pixel(1, shp_y, bright)

def draw_blt():
	global blt_x, blt_y, blt_x2, blt_y2, trg_x, trg_y
	draw_pixel(blt_x2, blt_y2, bright0)
	if(blt_x + blt_y > 0):
		if(blt_x > width - 1):
			hide_blt()
		elif(blt_x >= trg_x) and (blt_y == trg_y):
			exp_trg()
		else:
			draw_pixel(blt_x, blt_y, bright3)
			blt_x2 = blt_x
			blt_y2 = blt_y
			blt_x = blt_x + 1


def hide_blt():
	global blt_x, blt_y
	blt_x = 0
	blt_y = 0
	if(trg_x <= width-1):
		draw_pixel(blt_x, blt_y, bright0)

def draw_trg():
	global trg_x, trg_x2, trg_y, trg_y2, blt_x, blt_y
	#print("trg: " + str(trg_x) + "," + str(trg_y))
	draw_pixel(trg_x2, trg_y2, bright0)
	if(trg_x + trg_y > 0):
		if(trg_x < 0):
			hide_trg()
		if(blt_x >= trg_x) and (blt_y == trg_y):
			exp_trg()
		else:
			draw_pixel(trg_x, trg_y, bright)
			trg_x2 = trg_x
			trg_y2 = trg_y
			trg_x = trg_x - 1


def hide_trg():
	global trg_x, trg_y
	trg_x = 0
	trg_y = 0
	draw_pixel(trg_x, trg_y, bright0)
	
def exp_trg():
	global trg_x, trg_y, blt_x, blt_y
	x = blt_x + 1
	y = blt_y
	hide_trg()
	hide_blt()

	draw_pixel(x, y, bright0)

	blt_x = blt_x + 1
	draw_pixel(x,   y-1, bright3)
	draw_pixel(x,   y+1, bright3)
	draw_pixel(x-1, y, bright3)
	draw_pixel(x+1, y, bright3)
	draw_pixel(x-1, y-1, bright1)
	draw_pixel(x+1, y-1, bright1)
	draw_pixel(x-1, y+1, bright1)
	draw_pixel(x+1, y+1, bright1)
	scr.show();
	time.sleep(delay)

	draw_pixel(x,   y-1, bright0)
	draw_pixel(x,   y+1, bright0)
	draw_pixel(x-1, y, bright0)
	draw_pixel(x+1, y, bright0)
	draw_pixel(x-1, y-1, bright0)
	draw_pixel(x+1, y-1, bright0)
	draw_pixel(x-1, y+1, bright0)
	draw_pixel(x+1, y+1, bright0)
	
	hide_blt()

def rand_trg():
	global trg_x, trg_y
	if(trg_x + trg_y == 0):
		trg_x = width - 1
		trg_y = random.choice(range(0, 8))
		#print("random:" + str(trg_x) + "," + str(trg_y))

@btn.on_press(btn.BUTTON_A)
def handler(button, pressed):
	global blt_x, blt_y, shp_y
	if(blt_x + blt_y == 0):
		blt_x = 1
		blt_y = shp_y

@btn.on_hold(btn.BUTTON_C, hold_time=5)
def handler(button):
	show_msg("Shutting Down...")
	os.system("sudo shutdown -h now")

@btn.on_press(btn.BUTTON_D, repeat=True, repeat_time=0.15)
def handler(button, pressed):
	global shp_y 
	if(shp_y >= height - 1):
		shp_y = height - 1
	else:
		shp_y = shp_y + 1
	#draw_ship()

@btn.on_press(btn.BUTTON_E, repeat=True, repeat_time=0.15)
def handler(button, pressed):
	global shp_y
	if(shp_y <= 0):
		shp_y = 0
	else:
		shp_y = shp_y - 1
	#draw_ship()

def tick():
	global c
	c = c + 1
	if(c >= 59):
		c = 0

def main_loop():
	global c
	while True:
		tick()
		draw_ship()
		if(c % 5 == 0):
			rand_trg()
			draw_trg()
		draw_blt()
		#print(str(shp_y) + " " + str(blt_x) + " " + str(blt_y))
		scr.show()
		time.sleep(delay)

try:
	main_loop()
except KeyboardInterrupt:
	exit()








