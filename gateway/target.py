""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
import logging
import can

import translator
import canreader
import canwriter

log = logging.getLogger('sys')

class Target(object):
    def __init__(self, config, loop):
        self._bus = can.interface.Bus(
            config['channel'],
            bustype=config['interface'], 
            bitrate=config['baudrate'],
        )
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

    def update_status(self, msg):
        self._status.update(msg)

    def update_control(self, msg):
        self._control.update(msg)

    async def read_canbus(self):
        ''' await a message in the asynchronous read buffer
        '''
        msg = await self._reader.get_message() 
        return self._trans.decode_from_frame(msg)

    def write_canbus(self, msg):
        ''' decode msg and write/update canbus periodic send task
        '''
        for name, data in msg.items():
            encoded = self._trans.encode_to_frame(name, data)
            self._writer.publish(name, encoded)

    def stop(self):
        log.debug("Target shutting down")
        '''
        try:
            self._reader.stop()
        except Exception as e:
            log.warning(e)

        try:
            self._writer.stop()
        except Exception as e:
            log.warning(e)

        '''
        try:
            self._bus.shutdown()
        except Exception as e:
            log.warning(e)
