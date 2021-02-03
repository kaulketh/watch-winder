#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 02.02.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import random
from time import sleep, strftime, localtime

from SM_28BYJ48 import SM28BYJ48

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

MOTOR = SM28BYJ48(6, 13, 19, 26)
ANGLES = (45, 90, 180, 270, 360)


def angle_mode_1(turns=1, sleep_time=1.5):
    while turns > 0:
        turns -= 1
        for _ in range(len(ANGLES)):
            i = random.randint(0, len(ANGLES) - 1)
            MOTOR.rotate(ANGLES[i] * -1)
            sleep(sleep_time)
    __wait_for_next_turn(900, 1800)


def random_mode_1(sleep_time=1.5):
    turns = random.randint(1, 3)
    MOTOR.logger.info(
        f"Turn {turns} times clockwise/counter clockwise.")
    ccw_steps = random.randint(1_024, 4_096)
    cw_steps = random.randint(-4_096, -1_024)
    for _ in range(turns):
        MOTOR.step(cw_steps)
        sleep(sleep_time)
        MOTOR.step(ccw_steps)
        sleep(sleep_time)
    __wait_for_next_turn()


def __wait_for_next_turn(range_begin=1_800, range_end=3600):
    wait = random.randint(range_begin, range_end)
    timestamp = strftime('%H:%M:%S', localtime())
    MOTOR.logger.info(
        f"{timestamp} Waiting {round(wait / 60, 2)} minutes until next movement")
    sleep(wait)


if __name__ == '__main__':
    MOTOR.logger.info(MOTOR)
    while True:
        try:
            # insert function here
            random_mode_1()
            # angle_mode_1()
            # angle_mode_1(turns=5, sleep_time=3)
        except KeyboardInterrupt:
            MOTOR.logger.warning(f"\nInterrupted by user input")
            exit(1)
        except Exception as e:
            MOTOR.logger.error(f"Any error occurs: {e}")
            exit(1)
        finally:
            MOTOR.reset()
