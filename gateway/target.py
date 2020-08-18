""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
import logging
import can

import framer
import canreader
import canwriter

log = logging.getLogger('sys')

class Target(object):
    def __init__(self, config, loop):

        self._framer = framer.Framer(config)
        can_filter_mask = int(config['can_mask'])

        can_filters = [{"can_id": id, "can_mask": can_filter_mask, "extended": False} \
                for id in self._framer.defined_messages()]

        self._bus = can.interface.Bus(
            config['channel'],
            bustype=config['interface'], 
            bitrate=config['baudrate'],
            can_filters=can_filters
        )

        self._status = dict()
        self._control = dict()
        self._reader = canreader.CANReader(config, self._bus, loop)
        self._writer = canwriter.CANWriter(config, self._bus)
        self._write_buffer = list() 

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
        ''' update control mutates the internal control state of the target
            object. this includes appending changed control messages to the
            write buffer.
        '''
        self._control.update(msg)
        for name in msg.keys():
            complete_data = self._control[name]
            self._write_buffer.append({name, complete_data})

    async def read_canbus(self):
        ''' Returns a dictionary of structure {msg_name: {signal_name: value}}
            or None. This call is asynchrous and will await a message in 
            the asynchronous canbus read buffer
        '''
        msg = await self._reader.get_message() 
        return self._framer.decode_from_frame(msg)

    def write_canbus(self, msg):
        ''' Encodes msg and if successful, writes the encoded message to the
            canbus as a periodic write. The periodic rate is defined by the
            update_rate object field.
        '''
        for name, data in msg.items():
            encoded = self._framer.encode_to_frame(name, data)
            if encoded:
                self._writer.publish(name, encoded)

    def get_write_buffer(self):
        write_buffer = self._write_buffer
        self._write_buffer = list()
        return write_buffer

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
