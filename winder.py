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

import service.status_led
from SM_28BYJ48 import SM28BYJ48

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

# init motor
MOTOR = SM28BYJ48(6, 13, 19, 26)
SPEED_RANGE = (0.0008, 0.0010)
# define rotation angles
ANGLES = (30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360)
# wait random time (minutes)
WAIT_PERIOD_RANGE = (15, 60)
# no run during night period
NIGHT_REST = (22, 9)


def mode_1(turn=1, sleep_time=1.5):
    MOTOR.logger.info(
        f"Run 'mode_1', "
        f"rotate {len(ANGLES)} different angles {turn} times.")

    while turn > 0:
        turn -= 1
        for _ in range(len(ANGLES)):
            i = random.randint(0, len(ANGLES) - 1)
            MOTOR.delay = random_speed()
            MOTOR.rotate(ANGLES[i] * random_direction())
            sleep(sleep_time)


def mode_2(turn=None, sleep_time=1.5):
    turns = random.randint(1, 3) if not turn else turn
    ccw_steps = random.randint(1_024, 4_096)
    cw_steps = random.randint(-4_096, -1_024)

    MOTOR.logger.info(
        f"Run 'mode_2', "
        f"turn {turns} times {cw_steps} / {ccw_steps} steps.")

    for _ in range(turns):
        MOTOR.delay = random_speed()
        MOTOR.step(cw_steps)
        sleep(sleep_time)
        MOTOR.delay = random_speed()
        MOTOR.step(ccw_steps)
        sleep(sleep_time)


def mode_3(turn=1, sleep_time=1.5):
    MOTOR.logger.info(
        f"Run 'mode_3', "
        f"rotate full rounds for- and backwards, {turn} times.")

    while turn > 0:
        turn -= 1
        MOTOR.delay = random_speed()
        MOTOR.rotate(360)
        sleep(sleep_time)
        MOTOR.delay = random_speed()
        MOTOR.rotate(-360)
        sleep(sleep_time)


def wait_for_next_turn(period_range=WAIT_PERIOD_RANGE):
    wait = random.randint(period_range[0] * 60, period_range[1] * 60 + 1)
    MOTOR.logger.debug(f"sleep({wait})")
    MOTOR.logger.info(f"Wait about {wait // 60} minutes until next run")
    sleep(wait)


def current_hour():
    return datetime.now().hour


def random_speed():
    return round(random.uniform(SPEED_RANGE[0], SPEED_RANGE[1]), 4)


def random_direction():
    d = random.randint(-1, 0)
    return d if d != 0 else 1


def welcome():
    MOTOR.logger.info("Start...")
    for _ in range(4):
        service.status_led.red()
        MOTOR.rotate(-90)
        service.status_led.blue()
        MOTOR.rotate(90)
    MOTOR.logger.info("Winder ready")
    service.status_led.blue()
    wait_for_next_turn()


def main():
    welcome()
    log_count = 1
    while True:
        try:
            if NIGHT_REST[0] >= current_hour() >= NIGHT_REST[1]:
                service.status_led.blue()
                MOTOR.logger.info("Start turning mode function")
                # turning mode function
                # mode_3(10)
                # mode_2(turn=5)
                mode_1(turn=2, sleep_time=3)
                wait_for_next_turn()
                log_count = 1
            else:
                if log_count > 0:
                    MOTOR.logger.info("Night rest! ;-)")
                    log_count -= 1
                service.status_led.red()
                sleep(60)
        except KeyboardInterrupt:
            MOTOR.logger.warning(f"Interrupted by user input")
            service.status_led.off()
            exit(1)
        except Exception as e:
            MOTOR.logger.error(f"Any error occurs: {e}")
            service.status_led.blink_red()
            exit(1)


if __name__ == '__main__':
    main()
