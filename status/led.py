#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# led.py
# created 08.03.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------


import os

import RPi.GPIO as GPIO


class StatusLed():

    def __init__(self, pin_red: int, pin_blue: int):
        self.__pins = (pin_red, pin_blue)  # RED, BLUE

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__pins[0], GPIO.OUT)
        GPIO.setup(self.__pins[1], GPIO.OUT)

    def red(self):
        self.off()
        GPIO.output(self.__pins[0], GPIO.HIGH)

    def blue(self):
        self.off()
        GPIO.output(self.__pins[1], GPIO.HIGH)

    def blink_red(self):
        self.off()
        os.system('gpio -g mode 20 out')
        os.system('gpio -g blink 20')

    def blink_blue(self):
        self.off()
        os.system('gpio -g mode 21 out')
        os.system('gpio -g blink 21')

    def off(self):
        for pin in self.__pins:
            GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
    pass
