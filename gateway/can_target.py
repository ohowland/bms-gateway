""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""

import logging
import cantools

class Inverter(object):
    def __init__(self):
        pass

    def update_status(self):
        pass

class SMA(Inverter):
    def __init__(self, config):
        super().__init__()

        self._comm = SMAComm(config)
        self._signals = map_signals(self.comm.db)
        self._messages = {}

    @property
    def comm(self):
        return self._comm

    @property
    def signals(self):
        return self._signals

    @property
    def messages(self):
        return self._messages

    def update_messages(self, data):
        for key in data.keys():
            msg_name = self.signals.get(key, None)
            if msg_name:
                msg = self.messages.get(msg_name, None)
                if not msg: 
                    msg = self.comm.db.get_message_by_name(msg_name)
                if msg:
                    msg.data = msg.encode(data)
                    self._messages.update({msg_name: msg})
            else:
                logging.debug("unrecognized signal name {}".format(key))
            

class SMAComm(object):

    def __init__(self, config):
        self.db = cantools.database.load_file(config['dbc_filepath'])

def map_signals(db):
    signals = {}
    for message in db.messages:
        for signal in message.signals:
            print(signal)
            signals.update({signal.name: message.name})

    return signals
