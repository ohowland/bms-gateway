""" Name: sma.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
from gateway import translator, can_reader, can_writer

import logging
import cantools
import can
import time

class Target(object):
    def __init__(self, config):
        self._trans = translator.Translator(config)
        self._status = dict()
        self._control = dict()
        self._reader = can_reader(config)
        self._writer = can_writer(config)

    @property
    def state(self):
        return self._state

    @property
    def trans(self):
        return self._trans

    def update_status(self)
