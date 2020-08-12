""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""
import translator
import canreader
import canwriter

class Target(object):
    def __init__(self, config, loop=None):
        self._trans = translator.Translator(config)
        self._status = dict()
        self._control = dict()
        self._reader = canreader.CANReader(config, loop=loop)
        self._writer = canwriter.CANWriter(config, loop=loop)

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
            yield self._trans.decode_from_frame(msg)
            
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
