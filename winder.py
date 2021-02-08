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

import resources.mode
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

WAIT_PERIOD_RANGE = (int(winder_props.getProperty("winder.wait.min")),
                     int(winder_props.getProperty("winder.wait.max")))

NIGHT_REST = (int(winder_props.getProperty("winder.nightrest.begin")),
              int(winder_props.getProperty("winder.nightrest.end")))


def wait_for_next_turn(period_range=WAIT_PERIOD_RANGE):
    wait = random.randint(period_range[0] * 60, period_range[1] * 60)
    LOGGER.info(
        f"Wait {wait} seconds until next run ({round(wait / 60, 1)} minutes)")
    sleep(wait)


def current_hour():
    return datetime.now().hour


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
        wait_for_next_turn((5, 10))
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
                # resources.mode.mode_3(motor, turn=10)
                # resources.mode.mode_2(motor, turn=5)
                resources.mode.mode_1(motor, turn=2, sleep_time=3)
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
