""" Name: can_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""

import logging
import cantools
import can

class BMS(object):
    def __init__(self):
        pass

    def update_status(self):
        pass

class Nuvation(BMS):
    def __init__(self, config):
        super().__init__()

        self._comm = NuvationComm(config)
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
        for signal_name in data.keys():
            msg_name = self.signals.get(signal_name, None)
            if msg_name:
                msg_template = self.comm.db.get_message_by_name(msg_name)
                if msg_template:
                    data = msg_template.encode(data)
                    msg = can.Message(arbitration_id=msg_template.frame_id, data=data)
                    self._messages.update({msg_name: msg})
                else:
                    raise AttributeError("cannot find message: {} in database".format(msg_name))
            else:
                raise AttributeError("no message in Nuvation.messages contains the signal: {}".format(key))
            

class NuvationComm(object):

    def __init__(self, config):
        self.db = cantools.database.load_file(config['dbc_filepath'])

def map_signals(db):
    signals = {}
    for message in db.messages:
        for signal in message.signals:
            print(signal)
            signals.update({signal.name: message.name})

    return signals