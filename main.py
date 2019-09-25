#!/usr/bin/env python
# -*- coding: utf-8 -*-

import buttonshim as btn
import signal
import os

import tvsnow
import wifimeter
import strobelight
import bounce

is_busy = False
last_func = None

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

def busy():
	global is_busy
	if(is_busy):
		return True
	else:
		is_busy = True
		return False

def free():
	global is_busy
	if(is_busy):
		is_busy = False
		return False
	else:
		return True
def do(func):
	global last_func
	if(busy()):
		#print("busy: " + func.__name__)
		return
	#print("free: " + func.__name__)
	blink()
	btn.set_pixel(0, 0, 127)
	last_func = func
	func()
	btn.set_pixel(0, 0, 0)
	free()

def setSigHandlers(module):
	signal.signal(signal.SIGINT, module.stop())
	signal.signal(signal.SIGTERM, module.stop())
	signal.signal(signal.SIGABRT, module.stop());
	signal.signal(signal.SIGQUIT, module.stop());

def wifi():
	setSigHandlers(wifimeter)
	wifimeter.show_title()
	wifimeter.show_ssid()
	wifimeter.init_meter()
	wifimeter.main_loop()

def snow():
	setSigHandlers(tvsnow)
	tvsnow.show_title()
	tvsnow.main_loop()

def strobe():
	setSigHandlers(strobelight)
	strobelight.show_title()
	strobelight.main_loop()

def ball():
	setSigHandlers(bounce)
	bounce.show_title()
	bounce.main_loop()

@btn.on_hold(btn.BUTTON_E, hold_time=1)
def handler(button):
	do(ball)

@btn.on_hold(btn.BUTTON_D, hold_time=1)
def handler(button):
	do(strobe)

@btn.on_hold(btn.BUTTON_B, hold_time=1)
def handler(button):
	do(snow)

@btn.on_hold(btn.BUTTON_A, hold_time=1)
def handler(button):
	do(wifi)

try:
	do(bounce)
	time.sleep(300)
	while True:
		do(last_func)
		time.sleep(300)
	#signal.pause()
except:
	exit()
