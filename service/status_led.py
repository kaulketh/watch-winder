#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 05.02.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

import os

import RPi.GPIO as GPIO

LEDS = (20, 21)  # RED, BLUE

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LEDS[0], GPIO.OUT)
GPIO.setup(LEDS[1], GPIO.OUT)


def red():
    off()
    GPIO.output(LEDS[0], GPIO.HIGH)


def blue():
    off()
    GPIO.output(LEDS[1], GPIO.HIGH)


def blink_red():
    off()
    os.system('gpio -g mode 20 out')
    os.system('gpio -g blink 20')


def blink_blue():
    off()
    os.system('gpio -g mode 21 out')
    os.system('gpio -g blink 21')


def off():
    for led in LEDS:
        GPIO.output(led, GPIO.LOW)


if __name__ == '__main__':
    pass
