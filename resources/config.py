#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# created 08.02.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import os

import pyjavaproperties3

from logger import LOGGER

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"


class Properties(pyjavaproperties3.Properties):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, file):
        super().__init__()
        self.__logger = LOGGER
        self.path = f"{self.THIS_FOLDER}{file}"
        self.__logger.debug(f"Load properties from {self.path}")
        self.load(open(self.path))

    def getProperty(self, key):
        value = self._props.get(key, '')
        self.__logger.debug(f"Get property '{key}={value}'")
        return value


winder_properties = Properties("/winder.properties")

if __name__ == '__main__':
    pass
