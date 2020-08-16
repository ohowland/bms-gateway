""" Name: framer.py
    Author: Howl & Edgerton, llc 2020 
"""

import logging
import cantools
import can

log = logging.getLogger('sys')

class Framer(object):

    def __init__(self, config):
        self._db = cantools.database.load_file(config['dbc_filepath'])

    @property
    def db(self):
        return self._db


    def decode_from_frame(self, msg):
        try:
            print(msg)
            decoded_data = self.db.decode_message(msg.arbitration_id, msg.data, scaling=True) 
            print(decoded_data)
            msg_name = self.db.get_message_by_frame_id(msg.arbitration_id).name
            return {msg_name: decoded_data}
        except KeyError as e:
            log.warning("unable to decode message 0x{:02x}".format(int(str(e))))
            return None


    def encode_to_frame(self, name: str, data: dict) -> can.Message:
        try:
            template = self.db.get_message_by_name(name)
        except Exception as e:
            log.warning(e)

        try:
            encoded_data = self.db.encode_message(template.frame_id, data, scaling=True)
            msg = can.Message(arbitration_id = template.frame_id,
                              data = encoded_data,
                              is_extended_id = template.is_extended_frame,
                              dlc = template.length)
            return msg

        except Exception as e:
            log.warning(e)

            return None
