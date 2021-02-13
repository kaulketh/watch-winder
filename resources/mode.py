#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 08.02.2021, tkaulke
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

import random
from time import sleep

from logger import LOGGER
from resources.property import winder_props

# fixed angle of rotation
ANGLES = (30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360)

STEP_DELAY_RANGE = (float(winder_props.getProperty("motor.step.delay.min")),
                    float(winder_props.getProperty("motor.step.delay.max")))


def __random_direction():
    d = random.randint(-1, 0)
    return d if d != 0 else 1


def __random_step_delay():
    return round(random.uniform(STEP_DELAY_RANGE[0], STEP_DELAY_RANGE[1]), 4)


def mode_1(motor, turn=1, sleep_time=1.5):
    LOGGER.info(
        f"Run 'mode_1', "
        f"rotate {len(ANGLES)} different angles {turn} times.")

    while turn > 0:
        turn -= 1
        for _ in range(len(ANGLES)):
            i = random.randint(0, len(ANGLES) - 1)
            motor.delay = __random_step_delay()
            motor.rotate(ANGLES[i] * __random_direction())
            sleep(sleep_time)


def mode_2(motor, turn=None, sleep_time=1.5):
    turns = random.randint(1, 3) if not turn else turn
    ccw_steps = random.randint(1_024, 4_096)
    cw_steps = random.randint(-4_096, -1_024)

    LOGGER.info(
        f"Run 'mode_2', "
        f"turn {turns} times {cw_steps} / {ccw_steps} steps.")

    for _ in range(turns):
        motor.delay = __random_step_delay()
        motor.step(cw_steps)
        sleep(sleep_time)
        motor.delay = __random_step_delay()
        motor.step(ccw_steps)
        sleep(sleep_time)


def mode_3(motor, turn=1, sleep_time=1.5):
    LOGGER.info(
        f"Run 'mode_3', "
        f"rotate full rounds for- and backwards, {turn} times.")

    while turn > 0:
        turn -= 1
        motor.delay = __random_step_delay()
        motor.rotate(360)
        sleep(sleep_time)
        motor.delay = __random_step_delay()
        motor.rotate(-360)
        sleep(sleep_time)


if __name__ == '__main__':
    pass
