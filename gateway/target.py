""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
import logging
import can

import framer
import canreader
import canwriter

LOGGER = logging.getLogger('target')

class Target:
    def __init__(self, config, loop):

        self._name = config['name']
        self._framer = framer.Framer(config)
        can_filter_mask = int(config['can_mask'])

        can_filters = [{"can_id": msg.frame_id, "can_mask": can_filter_mask, "extended": False} \
                for msg in self._framer.defined_messages()]

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

        self._whitelist = 
        self._ready = False

    def __repr__(self):
        return "Name: {}\nStatus: {}\nControl: {}\n"\
                .format(self.name, self.status, self.control)

    def __del__(self):
        self.stop()

    @property
    def name(self):
        return self._name

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
        for msg_name, signals in msg.items():
            exists = self.control.get(msg_name, None)
            if exists:
                self._control[msg_name].update(signals)
            else:
                self._control.update({msg_name: signals})
            
            self._update_write_buffer(msg)

    def _update_write_buffer(self, msg):
        for name in msg.keys():
            complete_data = self._control[name]
            self._write_buffer.append({name: complete_data})

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
        ''' Returns the write buffer, and clears the
            internal buffer storage
        '''

        write_buffer = self._write_buffer
        self._write_buffer = list() # Clear the buffer after read
        return write_buffer

    def ready(self):
        if self._ready:
            return True
        else:
            signals_list = {y.name for x in self._framer.defined_messages() for y in x.signals}
            signals_ready = {y for x in self._control.values() for y in x.keys()}
            
            signals_waiting = signals_list.difference(signals_ready)
            if signals_waiting:
                LOGGER.debug("waiting for signals to initialize: {}".format(signals_waiting))
                return False
            else:
                self._ready = True
                LOGGER.debug("{} write control initialization complete".format(self.name))
                return True

    def stop(self):
        LOGGER.debug("Target shutting down")
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
            LOGGER.warning(e)
