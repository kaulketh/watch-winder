#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 03.02.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import random
from datetime import datetime
from time import sleep

from SM_28BYJ48 import SM28BYJ48

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

MOTOR = SM28BYJ48(6, 13, 19, 26)
ANGLES = (45, 90, 180, 270, 360)


def angle_mode(turns=1, sleep_time=1.5):
    while turns > 0:
        turns -= 1
        for _ in range(len(ANGLES)):
            i = random.randint(0, len(ANGLES) - 1)
            MOTOR.rotate(ANGLES[i] * random_direction())
            sleep(sleep_time)
    wait_for_next_turn(600, 1_800)


def full_random_mode(sleep_time=1.5):
    turns = random.randint(1, 3)
    MOTOR.logger.debug(
        f"Turn {turns} times clockwise/counter clockwise.")
    ccw_steps = random.randint(1_024, 4_096)
    cw_steps = random.randint(-4_096, -1_024)
    for _ in range(turns):
        MOTOR.step(cw_steps)
        sleep(sleep_time)
        MOTOR.step(ccw_steps)
        sleep(sleep_time)
    wait_for_next_turn()


def wait_for_next_turn(range_begin=1_800, range_end=3600):
    wait = random.randint(range_begin, range_end)
    MOTOR.logger.info(
        f"Waiting {round(wait / 60, 1)} minutes until next movement")
    sleep(wait)


def current_hour():
    return datetime.now().hour


def random_direction():
    d = random.randint(-1, 0)
    return d if d != 0 else 1


if __name__ == '__main__':
    MOTOR.logger.debug(MOTOR)
    count = 1
    while True:
        try:
            if 8 <= current_hour() <= 22:
                # insert function here
                angle_mode(sleep_time=3)

                count = 1
            else:
                # Wait for the end of the night
                if count > 0:
                    MOTOR.logger.info("Night rest! ;-)")
                    count -= 1
                sleep(60)
        except KeyboardInterrupt:
            MOTOR.logger.warning(f"Interrupted by user input")
            exit(1)
        except Exception as e:
            MOTOR.logger.error(f"Any error occurs: {e}")
            MOTOR.reset()
            exit(1)
