#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# __init__.py
# created 08.03.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import RPi.GPIO as GPIO
import os

from logger import LOGGER


class StatusLed:
    def __init__(self, pin):
        self.__logger = LOGGER
        self.__pin = pin
        self.__logger.debug(f"Init status led {self}")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__pin, GPIO.OUT)

    def on(self):
        self.off()
        self.__logger.debug("Enable light")
        GPIO.output(self.__pin, GPIO.HIGH)

    def blink(self):
        self.off()
        self.__logger.debug("Enable blinking red light")
        os.system('gpio -g mode %s out' % str(self.__pin))
        os.system('gpio -g blink %s' % str(self.__pin))

    def off(self):
        self.__logger.debug("Disable led")
        GPIO.output(self.__pin, GPIO.LOW)


class TwoColorStatusLed:
    def __init__(self, pin_red: int, pin_blue: int):
        self.__logger = LOGGER
        self.__pins = (pin_red, pin_blue)  # RED, BLUE
        self.__logger.debug(f"Init red/blue status led {self}")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__pins[0], GPIO.OUT)
        GPIO.setup(self.__pins[1], GPIO.OUT)

    def red(self):
        self.off()
        self.__logger.debug("Enable red light")
        GPIO.output(self.__pins[0], GPIO.HIGH)

    def blue(self):
        self.off()
        self.__logger.debug("Enable blue light")
        GPIO.output(self.__pins[1], GPIO.HIGH)

    def blink_red(self):
        self.off()
        self.__logger.debug("Enable blinking red light")
        os.system('gpio -g mode %s out' % str(self.__pins[0]))
        os.system('gpio -g blink %s' % str(self.__pins[0]))

    def blink_blue(self):
        self.off()
        self.__logger.debug("Enable blinking blue light")
        os.system('gpio -g mode %s out' % str(self.__pins[1]))
        os.system('gpio -g blink %s' % str(self.__pins[1]))

    def off(self):
        self.__logger.debug("Disable led")
        for pin in self.__pins:
            GPIO.output(pin, GPIO.LOW)
