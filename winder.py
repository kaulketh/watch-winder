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

from config import winder_properties
from logger import LOGGER
from mode import Mode
from motor import SM28BYJ48
from status_led import TwoColorStatusLed

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

WAIT_PERIOD_RANGE = (int(winder_properties.getProperty("winder.wait.min")),
                     int(winder_properties.getProperty("winder.wait.max")))

NIGHT_REST = (int(winder_properties.getProperty("winder.nightrest.begin")),
              int(winder_properties.getProperty("winder.nightrest.end")))

LED = TwoColorStatusLed(pin_red=20, pin_blue=21)


def init():
    try:
        LOGGER.info("Initializing...")
        motor = SM28BYJ48(
            int(winder_properties.getProperty("motor.pin.in1")),
            int(winder_properties.getProperty("motor.pin.in2")),
            int(winder_properties.getProperty("motor.pin.in3")),
            int(winder_properties.getProperty("motor.pin.in4")))
        for _ in range(4):
            LED.red()
            motor.rotate(-90)
            LED.blue()
            motor.rotate(90)
        LOGGER.info("Winder ready.")
        LED.blue()
        return motor
    except KeyboardInterrupt:
        LOGGER.warning(f"Interrupted by user input")
        LED.off()
        exit(1)
    except Exception as e:
        LOGGER.error(f"Any error occurs: {e}")
        LED.blink_red()
        exit(1)


def main():
    m = Mode(init())
    log_count = 1
    while True:
        try:
            if NIGHT_REST[0] >= datetime.now().hour >= NIGHT_REST[1]:
                LED.blue()
                LOGGER.info("Start turning mode function")
                # turning mode function
                m.mode_3(rotations=100)
                # m.mode_2(turn=5)
                # m.mode_1(turn=10, sleep_time=0.5)
                log_count = 1
            else:
                LED.red()
                if log_count > 0:
                    LOGGER.info("Night rest, sleeping...")
                    log_count -= 1
            w = random.randint(WAIT_PERIOD_RANGE[0] * 60,
                               WAIT_PERIOD_RANGE[1] * 60)
            LOGGER.info(
                f"Wait {w} seconds until next try ({round(w / 60, 1)} minutes)")
            sleep(w)
        except KeyboardInterrupt:
            LOGGER.warning(f"Interrupted by user input")
            LED.off()
            exit(1)
        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            LED.blink_red()
            exit(1)


if __name__ == '__main__':
    main()
