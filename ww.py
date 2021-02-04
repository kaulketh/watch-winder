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

MOTOR = SM28BYJ48(6, 13, 19, 26)  # init motor
ANGLES = (45, 90, 180, 270, 360)  # define rotation angles
WAIT_PERIOD_RANGE = (900, 3601)  # wait randomly min. 15 minutes, max. 1 hour
NIGHT_REST = (8, 22)  # no run during this period


def angle_mode(turns=1, sleep_time=1.5):
    MOTOR.logger.info(
        f"Run 'angle_mode', "
        f"rotate {len(ANGLES)} different angles {turns} times.")
    while turns > 0:
        turns -= 1
        for _ in range(len(ANGLES)):
            i = random.randint(0, len(ANGLES) - 1)
            MOTOR.rotate(ANGLES[i] * random_direction())
            sleep(sleep_time)


def step_mode(sleep_time=1.5):
    turns = random.randint(1, 3)
    ccw_steps = random.randint(1_024, 4_096)
    cw_steps = random.randint(-4_096, -1_024)
    MOTOR.logger.info(
        f"Run 'step_mode', "
        f"turn {turns} times {cw_steps} / {ccw_steps} steps.")

    for _ in range(turns):
        MOTOR.step(cw_steps)
        sleep(sleep_time)
        MOTOR.step(ccw_steps)
        sleep(sleep_time)


def wait_for_next_turn(wait_period=WAIT_PERIOD_RANGE):
    wait = random.randint(wait_period[0], wait_period[1])
    MOTOR.logger.info(
        f"Waiting {round(wait / 60, 1)} minutes until next movement")
    sleep(wait)


def current_hour():
    return datetime.now().hour


def random_direction():
    d = random.randint(-1, 0)
    return d if d != 0 else 1


def main():
    log_count = 1
    while True:
        try:
            if NIGHT_REST[0] <= current_hour() <= NIGHT_REST[1]:
                if log_count > 0:
                    MOTOR.logger.info("Call turning mode function")
                    log_count -= 1
                angle_mode(turns=3, sleep_time=3)  # turning mode function
                # step_mode(sleep_time=3)
                wait_for_next_turn()
                log_count = 1
            else:
                if log_count > 0:
                    MOTOR.logger.info("Night rest! ;-)")
                    log_count -= 1
                sleep(60)
        except KeyboardInterrupt:
            MOTOR.logger.warning(f"Interrupted by user input")
            exit(1)
        except Exception as e:
            MOTOR.logger.error(f"Any error occurs: {e}")
            MOTOR.reset()
            exit(1)


if __name__ == '__main__':
    main()
