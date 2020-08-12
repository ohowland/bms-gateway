""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
from can_reader import CANReader
from can_writer import CANWriter
from translator import Translator

class Target(object):
    def __init__(self, config):
        self._trans = Translator(config)
        self._status = dict()
        self._control = dict()
        self._reader = CANReader(config)
        self._writer = CANWriter(config)

    def __repr__(self):
        return "Status: {}\nControl: {}\n"\
                .format(self.status, self.control)
                

    def __del__(self):
        self.stop()

    @property
    def status(self):
        return self._status

    @property
    def control(self):
        return self._control


    @property
    def trans(self):
        return self._trans

    def update_status(self):
        for msg in self._reader: 
            decoded = self._trans.decode_from_frame(msg)
            self._status.update(decoded)

    def write_control(self):
        for name, data in self._control.items():
            encoded = self._trans.encode_to_frame(name, data)
            self._writer.publish(name, encoded)

    def stop(self):
        try:
            self._reader.stop()
        except:
            pass

        try:
            self._writer.stop()
        except:
            pass
