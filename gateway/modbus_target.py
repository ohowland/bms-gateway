""" Name: modbus_target.py
    Author: Howl & Edgerton, llc 2019
    About: targets for alarming program
"""

import logging

from modbus_poller import Modbus

class BMS(object):
    def __init__(self):
        self._alarm = False

    def update_status(self):
        pass


class Nuvation(BMS):
    def __init__(self):
        super().__init__()
        self._comm = NuvationComm()
        self._soc = 0
        self._vpack = 0

    @property
    def comm(self):
        return self._comm

    @property
    def SOC(self):
        return self._active_alarm_level

    @SOC.setter
    def SOC(self, value):
        self._active_alarm_level = value

    @property
    def Vpack(self):
        return self._active_brake_level

    @Vpack.setter
    def Vpack(self, value):
        self._active_brake_level = value

    def update_from(self, polled_data):
        for key, val in polled_data.items():
            setattr(self, "_" + key, val)


class NuvationComm(object):

    def __init__(self):
        #register = namedtuple('modbus_register', 'name, address, type, function_code')
        self.registers = [
            Modbus.register('soc', 0, 'U16', 0x03),
            Modbus.register('vpack', 1, 'U16', 0x03),
        ]