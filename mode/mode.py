#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# mode.py
# created 08.03.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import random
from time import sleep

from logger import LOGGER
from resources.config import winder_properties


def random_direction():
    d = random.randint(-1, 0)
    return d if d != 0 else 1


class Mode:
    """Class represents turning modes of a given stepper motor"""
    FIX_ANGLES = (
        30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360)

    def __init__(self, motor):
        self.__logger = LOGGER
        self.__motor = motor
        self.__step_delay_range = (
            float(winder_properties.getProperty("motor.step.delay.min")),
            float(winder_properties.getProperty("motor.step.delay.max")))
        self.__fix_angles = self.FIX_ANGLES
        self.__logger.debug("Init rotation modes")

    def __random_step_delay(self):
        return round(
            random.uniform(self.__step_delay_range[0],
                           self.__step_delay_range[1]),
            4)

    def mode_1(self, turn=1, sleep_time=1.5):
        self.__logger.info(
            f"Run 'mode_1', "
            f"rotate {len(self.__fix_angles)} different angles {turn} times.")

        while turn > 0:
            turn -= 1
            for _ in range(len(self.__fix_angles)):
                i = random.randint(0, len(self.__fix_angles) - 1)
                self.__motor.delay = self.__random_step_delay()
                self.__motor.rotate(
                    self.__fix_angles[i] * random_direction())
                sleep(sleep_time)

    def mode_2(self, turn=None, sleep_time=1.5):
        turns = random.randint(1, 3) if not turn else turn
        ccw_steps = random.randint(1_024, 4_096)
        cw_steps = random.randint(-4_096, -1_024)

        self.__logger.info(
            f"Run 'mode_2', "
            f"turn {turns} times {cw_steps} / {ccw_steps} steps.")

        for _ in range(turns):
            self.__motor.delay = self.__random_step_delay()
            self.__motor.step(cw_steps)
            sleep(sleep_time)
            self.__motor.delay = self.__random_step_delay()
            self.__motor.step(ccw_steps)
            sleep(sleep_time)

    def mode_3(self, rotations=1, sleep_time=1.5):
        self.__logger.info(
            f"Run 'mode_3', "
            f"rotate full rounds for- and backwards, {rotations} times.")

        while rotations > 0:
            rotations -= 1
            self.__motor.delay = self.__random_step_delay()
            self.__motor.rotate(360)
            sleep(sleep_time)
            self.__motor.delay = self.__random_step_delay()
            self.__motor.rotate(-360)
            sleep(sleep_time)


if __name__ == '__main__':
    pass
