#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# __init__.py
# created 08.03.2021
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
        self.__prop_path = os.path.join(self.THIS_FOLDER, file)
        self.__logger.debug(f"Load properties from {self.__prop_path}")
        self.load(open(self.__prop_path))

    def getProperty(self, key):
        value = self._props.get(key, '')
        self.__logger.debug(f"Get property '{key}={value}'")
        return value


winder_properties = Properties("../resources/winder.properties")
