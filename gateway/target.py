""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
import logging

import translator
import canreader
import canwriter

log = logging.get_logger('sys')

class Target(object):
    def __init__(self, config, loop):
        self._bus = can.interface.Bus(config['channel'],
                                     bustype=config['interface'], 
                                     bitrate=config['baudrate'])
        self._trans = translator.Translator(config)
        self._status = dict()
        self._control = dict()
        self._reader = canreader.CANReader(config, self._bus, loop)
        self._writer = canwriter.CANWriter(config, self._bus)

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

    async def update_status(self):
        async for msg in self._reader: 
            yield self._trans.decode_from_frame(msg)
        else:
            return None
            
    def write_control(self):
        for name, data in self._control.items():
            encoded = self._trans.encode_to_frame(name, data)
            self._writer.publish(name, encoded)

    def stop(self):
        try:
            self._reader.stop()
        except as e:
            log.warning(e)

        try:
            self._writer.stop()
        except as e:
            log.warning(e)

        try:
            self._bus.shutdown()
        except as e:
            log.warning(e)
