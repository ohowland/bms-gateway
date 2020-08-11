""" Name: nuvation.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""

import logging
import cantools
import can

class Translator(object):
    
    def __init__(self, config):
        self._comm = DBCComm(config)
        self._state = init_state(self.comm.db)
        self._signals = init_signals(self.comm.db)
        self._messages = init_messages(self.comm.db) 

    @property
    def comm(self):
        return self._comm

    @property
    def signals(self):
        return self._signals

    @property
    def messages(self):
        return self._messages

    def update_status(self, msg):
        try:
            decoded_msg = self.comm.db.decode_message(msg.arbitration_id, msg, scaling=True) 
            for name, val in decoded_msg:
                self._state[name] = val
        except:
            raise TypeError("uanble to decode frame id: {}".format(msg.arbitration_id)

            

class NuvationComm(object):

    def __init__(self, config):
        self._db = cantools.database.load_file(config['dbc_filepath'])

    @property
    def db(self):
        return self._db

def init_signals(db):
    signals = {}
    for message in db.messages:
        for signal in message.signals:
            signals.update({signal.name: message.name})

    return signals

def init_state(db):
    state = {}
    for message in db.messages:
        state.update({message.name: {}})
        for signal in message.signals:
            state[message.name].update({signal.name: None})

    return state

def init_messages(db):
    messages = {}
    for message in db.messages:
        messages.update({message.name: None})
