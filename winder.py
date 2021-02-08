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

import resources.status_led
from logger import LOGGER
from motor import SM28BYJ48
from resources.property import winder_props

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

motor = SM28BYJ48(
    int(winder_props.getProperty("motor.pin.in1")),
    int(winder_props.getProperty("motor.pin.in2")),
    int(winder_props.getProperty("motor.pin.in3")),
    int(winder_props.getProperty("motor.pin.in4")))

SPEED_RANGE = (float(winder_props.getProperty("motor.speed.min")),
               float(winder_props.getProperty("motor.speed.max")))

ANGLES = tuple(winder_props.getProperty("winder.turn.angles"))

WAIT_PERIOD_RANGE = (int(winder_props.getProperty("winder.wait.min")),
                     int(winder_props.getProperty("winder.wait.max")))

NIGHT_REST = (winder_props.getProperty("winder.nightrest.begin"),
              winder_props.getProperty("winder.nightrest.end"))


def mode_1(turn=1, sleep_time=1.5):
    LOGGER.info(
        f"Run 'mode_1', "
        f"rotate {len(ANGLES)} different angles {turn} times.")

    while turn > 0:
        turn -= 1
        for _ in range(len(ANGLES)):
            i = random.randint(0, len(ANGLES) - 1)
            motor.delay = random_speed()
            motor.rotate(ANGLES[i] * random_direction())
            sleep(sleep_time)


def mode_2(turn=None, sleep_time=1.5):
    turns = random.randint(1, 3) if not turn else turn
    ccw_steps = random.randint(1_024, 4_096)
    cw_steps = random.randint(-4_096, -1_024)

    LOGGER.info(
        f"Run 'mode_2', "
        f"turn {turns} times {cw_steps} / {ccw_steps} steps.")

    for _ in range(turns):
        motor.delay = random_speed()
        motor.step(cw_steps)
        sleep(sleep_time)
        motor.delay = random_speed()
        motor.step(ccw_steps)
        sleep(sleep_time)


def mode_3(turn=1, sleep_time=1.5):
    LOGGER.info(
        f"Run 'mode_3', "
        f"rotate full rounds for- and backwards, {turn} times.")

    while turn > 0:
        turn -= 1
        motor.delay = random_speed()
        motor.rotate(360)
        sleep(sleep_time)
        motor.delay = random_speed()
        motor.rotate(-360)
        sleep(sleep_time)


def wait_for_next_turn(period_range=WAIT_PERIOD_RANGE):
    wait = random.randint(period_range[0] * 60, period_range[1] * 60 + 1)
    LOGGER.debug(f"sleep({wait})")
    LOGGER.info(f"Wait about {wait // 60} minutes until next run")
    sleep(wait)


def current_hour():
    return datetime.now().hour


def random_speed():
    return round(random.uniform(SPEED_RANGE[0], SPEED_RANGE[1]), 4)


def random_direction():
    d = random.randint(-1, 0)
    return d if d != 0 else 1


def start():
    try:
        LOGGER.info("Start...")
        for _ in range(4):
            resources.status_led.red()
            motor.rotate(-90)
            resources.status_led.blue()
            motor.rotate(90)
        LOGGER.info("Winder ready")
        resources.status_led.blue()
        wait_for_next_turn()
    except KeyboardInterrupt:
        LOGGER.warning(f"Interrupted by user input")
        resources.status_led.off()
        exit(1)
    except Exception as e:
        LOGGER.error(f"Any error occurs: {e}")
        resources.status_led.blink_red()
        exit(1)


def main():
    start()
    log_count = 1
    while True:
        try:
            if NIGHT_REST[0] >= current_hour() >= NIGHT_REST[1]:
                resources.status_led.blue()
                LOGGER.info("Start turning mode function")
                # turning mode function
                # mode_3(10)
                # mode_2(turn=5)
                mode_1(turn=2, sleep_time=3)
                wait_for_next_turn()
                log_count = 1
            else:
                if log_count > 0:
                    LOGGER.info("Night rest! ;-)")
                    log_count -= 1
                resources.status_led.red()
                sleep(60)
        except KeyboardInterrupt:
            LOGGER.warning(f"Interrupted by user input")
            resources.status_led.off()
            exit(1)
        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            resources.status_led.blink_red()
            exit(1)


if __name__ == '__main__':
    main()
