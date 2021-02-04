#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 02.02.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------


__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

from time import sleep

import RPi.GPIO as GPIO

from .logger import LOGGER

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class SM28BYJ48:
    """
    The stepper motor 28BYJ-48 is designed in such a way that the motor needs
    8 steps for one revolution. Due to the gear ratio it requires 512 x 8 steps
    so that the axis rotates through 360°.
    """

    def __init__(self, in1: int, in2: int, in3: int, in4: int,
                 delay: float = 0.001):
        """
        Pins of ULN2003A to related Pins of Rapberry Pi

        :param in1: IN 1
        :param in2: IN 2
        :param in3: IN 3
        :param in4: IN 4
        :param delay: Waiting time to control velocity of motor
        """

        self.__delay = delay
        self.__in1 = in1
        self.__in2 = in2
        self.__in3 = in3
        self.__in4 = in4
        self.__sa = 5.625 / 64  # step angle
        self.__spr = 512  # steps per one revolution
        self.__repr_str = f"{self.__class__.__name__}: " \
                          f"IN1={self.__in1}, " \
                          f"IN2={self.__in2}, " \
                          f"IN3={self.__in3}, " \
                          f"IN4={self.__in4}, " \
                          f"Delay={self.__delay}"
        self.__logger = LOGGER
        self.__logger.debug(
            f"Initialize instance of {self.__repr_str}")

        GPIO.setup(self.__in1, GPIO.OUT)
        GPIO.setup(self.__in2, GPIO.OUT)
        GPIO.setup(self.__in3, GPIO.OUT)
        GPIO.setup(self.__in4, GPIO.OUT)

        GPIO.output(self.__in1, False)
        GPIO.output(self.__in2, False)
        GPIO.output(self.__in3, False)
        GPIO.output(self.__in4, False)

    def __repr__(self):
        return self.__repr_str

    def __str__(self):
        return self.__repr_str

    def __step_1(self):
        GPIO.output(self.__in4, True)
        sleep(self.__delay)
        GPIO.output(self.__in4, False)

    def __step_2(self):
        GPIO.output(self.__in4, True)
        GPIO.output(self.__in3, True)
        sleep(self.__delay)
        GPIO.output(self.__in4, False)
        GPIO.output(self.__in3, False)

    def __step_3(self):
        GPIO.output(self.__in3, True)
        sleep(self.__delay)
        GPIO.output(self.__in3, False)

    def __step_4(self):
        GPIO.output(self.__in3, True)
        GPIO.output(self.__in2, True)
        sleep(self.__delay)
        GPIO.output(self.__in3, False)
        GPIO.output(self.__in2, False)

    def __step_5(self):
        GPIO.output(self.__in2, True)
        sleep(self.__delay)
        GPIO.output(self.__in2, False)

    def __step_6(self):
        GPIO.output(self.__in2, True)
        GPIO.output(self.__in1, True)
        sleep(self.__delay)
        GPIO.output(self.__in2, False)
        GPIO.output(self.__in1, False)

    def __step_7(self):
        GPIO.output(self.__in1, True)
        sleep(self.__delay)
        GPIO.output(self.__in1, False)

    def __step_8(self):
        GPIO.output(self.__in4, True)
        GPIO.output(self.__in1, True)
        sleep(self.__delay)
        GPIO.output(self.__in4, False)
        GPIO.output(self.__in1, False)

    def __clockwise(self, steps):
        self.__logger.debug(f"{steps} steps clockwise")
        for _ in range(steps):
            self.__step_1()
            self.__step_2()
            self.__step_3()
            self.__step_4()
            self.__step_5()
            self.__step_6()
            self.__step_7()
            self.__step_8()

    def __counter_clockwise(self, steps):
        self.__logger.debug(f"{steps} steps counter clockwise")
        for _ in range(steps):
            self.__step_8()
            self.__step_7()
            self.__step_6()
            self.__step_5()
            self.__step_4()
            self.__step_3()
            self.__step_2()
            self.__step_1()

    @property
    def logger(self):
        return self.__logger

    def reset(self):
        self.__logger.debug(f"Step motor reset, GPIO cleanup")
        GPIO.cleanup()

    def step(self, steps: int = 1):
        self.__logger.debug(f"Take {steps} steps.")
        self.__counter_clockwise(steps * -1) \
            if steps < 0 else self.__clockwise(steps)

    def rotate(self, degrees):
        self.__logger.debug(f"Rotate {degrees} degrees.")
        self.step(int(degrees / 5.625 / 64 * 512))


if __name__ == '__main__':
    pass
