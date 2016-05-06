#!/usr/bin/env python
# coding: utf-8

"""
Released under MIT License. See LICENSE file.

Controling a motor jingling a bell using a relay (connected to NC).

By Kamel TIGHIDET <tighidet.kamel@gmail.com>

"""


import time
try:
	import RPi.GPIO as IO
except:
	print("Failed importing GPIO. You have to be root")

PIN_BELL = 3

IO.setmode(IO.BCM)

IO.setup(PIN_BELL, IO.OUT)
IO.output(PIN_BELL, IO.HIGH)

def jingle_bell():
	try:
		IO.output(PIN_BELL, IO.LOW)
		time.sleep(10)
		IO.output(PIN_BELL, IO.HIGH)
	except:
		IO.output(PIN_BELL, IO.HIGH)

jingle_bell()
