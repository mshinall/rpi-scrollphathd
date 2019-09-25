#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import scrollphathd as scr
from scrollphathd.fonts import font5x7
from time import localtime, strftime
import buttonshim as btn
import signal
import os
import re
from numpy import interp
import geocoder
import requests
from bs4 import BeautifulSoup
import random

import tvsnow
import wifimeter
import strobelight
import bounce


[width, height] = scr.get_shape()
scr.set_brightness(bright)
scr.set_font(font=font5x7)
scr.set_clear_on_exit(value=True)
btn.set_pixel(0, 0, 0)
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

def wifi():
	wifimeter.show_title()
	wifimeter.show_ssid()
	wifimeter.init_meter()
	wifimeter.main_loop()

def snow():
	tvsnow.show_title()
	tvsnow.main_loop()

def strobe():
	strobelight.show_title()
	strobelight.main_loop()

def ball():
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
	#do(clock)
	do(image)
	time.sleep(300)
	while True:
		do(last_func)
		time.sleep(300)
	#signal.pause()
except:
	exit()
