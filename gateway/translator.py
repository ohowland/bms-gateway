""" Name: translator.py
    Author: Howl & Edgerton, llc 2020 
"""

import logging
import cantools
import can

class Translator(object):
    
    def __init__(self, config):
        self._db = cantools.database.load_file(config['dbc_filepath'])
        self._state = init_state(self.db)

    @property
    def db(self):
        return self._db


    def decode_from_frame(self, msg: can.Message) -> dict:
        try:
            decoded_data = self.db.decode_message(msg.arbitration_id, msg.data, scaling=True) 
            msg_name = self.db.get_message_by_frame_id(msg.arbitration_id).name
            return {msg_name: decoded_data}
        except:
            raise TypeError("unable to decode frame id: {}".format(msg.arbitration_id))

    def encode_to_frame(self, name: str, data: dict) -> can.Message:
        try:
            template = self.db.get_message_by_name(name)
        except:
            raise KeyError("message name {} does not exist in .DBC database".format(name))

        try:
            encoded_data = self.db.encode_message(template.frame_id, data, scaling=True)
            msg = can.Message(arbitration_id = template.frame_id,
                              data = encoded_data,
                              is_extended_id = template.is_extended_frame,
                              dlc = template.length)
        except:
            raise TypeError("unable to encode frame id: {}".format(template.frame_id))

