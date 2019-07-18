#!/usr/bin/env python

#import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
gp0 = InputDevice('/dev/input/event0')

#prints out device info at start
print(gp0)

#evdev takes care of polling the controller in a loop
for event in gp0.read_loop():
    print(categorize(event))
