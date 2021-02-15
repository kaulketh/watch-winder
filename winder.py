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
from resources.config import winder_properties

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

WAIT_PERIOD_RANGE = (int(winder_properties.getProperty("winder.wait.min")),
                     int(winder_properties.getProperty("winder.wait.max")))

NIGHT_REST = (int(winder_properties.getProperty("winder.nightrest.begin")),
              int(winder_properties.getProperty("winder.nightrest.end")))


def wait(period_range=WAIT_PERIOD_RANGE):
    w = random.randint(period_range[0] * 60, period_range[1] * 60)
    LOGGER.info(
        f"Wait {w} seconds until next try ({round(w / 60, 1)} minutes)")
    sleep(w)


def init():
    try:
        LOGGER.info("Initializing...")
        motor = SM28BYJ48(
            int(winder_properties.getProperty("motor.pin.in1")),
            int(winder_properties.getProperty("motor.pin.in2")),
            int(winder_properties.getProperty("motor.pin.in3")),
            int(winder_properties.getProperty("motor.pin.in4")))

        for _ in range(4):
            resources.status_led.red()
            motor.rotate(-90)
            resources.status_led.blue()
            motor.rotate(90)
        LOGGER.info("Winder ready.")
        resources.status_led.blue()
        return motor
    except KeyboardInterrupt:
        LOGGER.warning(f"Interrupted by user input")
        resources.status_led.off()
        exit(1)
    except Exception as e:
        LOGGER.error(f"Any error occurs: {e}")
        resources.status_led.blink_red()
        exit(1)


def main():
    motor = init()
    log_count = 1
    while True:
        try:
            if NIGHT_REST[0] >= datetime.now().hour >= NIGHT_REST[1]:
                resources.status_led.blue()
                LOGGER.info("Start turning mode function")
                # turning mode function
                resources.mode.mode_3(motor, rotations=100)
                # resources.mode.mode_2(motor, turn=5)
                # resources.mode.mode_1(motor, 10, 0.5)
                log_count = 1
            else:
                resources.status_led.red()
                if log_count > 0:
                    LOGGER.info("Night rest, sleeping...")
                    log_count -= 1
            wait()
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
