""" Name: sma_target.py
    Author: Howl & Edgerton, llc 2020
    About: targets for canbus
"""

import logging
import cantools
import can

class Inverter(object):
    def __init__(self):
        pass

    def update_status(self):
        pass

class SMA(Inverter):
    def __init__(self, config):
        super().__init__()

        self._comm = SMAComm(config)
        self._signals = initialize_signal_map(self.comm.db)
        self._state = initialize_state(self.comm.db) 
        self._messages = initialize_messages(self.comm.db) 

    @property
    def comm(self):
        return self._comm

    @property
    def signals(self):
        return self._signals

    @property
    def state(self):
        return self._state

    @property
    def messages(self):
        return self._messages

    def update_messages(self, data):
        ''' updates the internal message/signal value state, and
            encodes the next state to a message format
            raises AttributeError
        '''
        for sig_name, sig_val in data.items():
            # map the signal back to its message
            msg_name = self.signals.get(sig_name, None)
            if msg_name:
                self._state[msg_name].update({sig_name: sig_val}) 

                # TODO: Update internal state FIRST, flag message names to reencode
                # then reencode them! this will avoid getting a bunch of attirbute
                # errors when data is missing during initial update.

                msg_template = self.comm.db.get_message_by_name(msg_name)
                if msg_template:
                    try:
                        encoded_msg = msg_template.encode(self._state[msg_name])
                        msg = can.Message(arbitration_id=msg_template.frame_id, data=encoded_msg)
                        self._messages.update({msg_name: msg})
                    except:
                        raise AttributeError("unable to encode msg {}".format(msg_name))
                else:
                    raise AttributeError("cannot find message: {} in database".format(msg_name))
            else:
                raise AttributeError("no message in SMA.messages contains the signal: {}".format(sig_name))
            

class SMAComm(object):

    def __init__(self, config):
        self.db = cantools.database.load_file(config['dbc_filepath'])

def initialize_signal_map(db):
    signals = {}
    for message in db.messages:
        for signal in message.signals:
            signals.update({signal.name: message.name})

    return signals

def initialize_state(db):
    state = {}
    for message in db.messages:
        state.update({message.name: {}})
        for signal in message.signals:
            state[message.name].update({signal.name: None}) 

    print(state)
    return state

def initialize_messages(db):
    messages = {}
    for message in db.messages:
        messages.update({message.name: None})

    return messages
