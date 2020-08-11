""" Name: sma.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""

import logging
import cantools
import can
import time

class Target(object):
    def __init__(self, config):
        self._trans = 
        self._state =  
        self._reader
        self._writer =

    @property
    def state(self):
        return self._state

    @property
    def trans(self):
        return self._trans

    
    def update_status(self, data):
        ''' updates the internal message/signal value state, and
            encodes the next state to a message format
            raises AttributeError
        '''
        encode = set()
        for sig_name, sig_val in data.items():
            # map the signal back to its message
            msg_name = self.signals.get(sig_name, None)
            if msg_name:
                self._state[msg_name].update({sig_name: sig_val}) 
                encode.update({msg_name})
            else:
                raise KeyError("no message in SMA.messages contains the signal: {}".format(sig_name))

        for msg_name in encode:
            msg_template = self.comm.db.get_message_by_name(msg_name)
            if msg_template:
                try:
                    encoded_msg = msg_template.encode(self._state[msg_name])
                    msg = can.Message(
                            arbitration_id = msg_template.frame_id, 
                            data = encoded_msg, 
                            is_extended_id = msg_template.is_extended_frame,
                            dlc = msg_template.length,
                            timestamp = time.time())
                    self._messages.update({msg_name: msg})
                except:
                    raise TypeError("unable to encode msg {}".format(msg_name))
            else:
                raise KeyError("cannot find message: {} in database".format(msg_name))
            

class SMAComm(object):

    def __init__(self, config):
        self._db = cantools.database.load_file(config['dbc_filepath'])

    @property
    def db(self):
        return self._db

def init_signal(db):
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

    return messages
