""" Name: framer.py
    Author: Howl & Edgerton, llc 2020
"""

import logging
import cantools
import can

LOGGER = logging.getLogger('framer')

class Framer:
    """ Framer encodes and decodes CAN Frames to and from dictonaries
    """
    def __init__(self, config):
        self._db = cantools.database.load_file(config['dbc_filepath'])

    @property
    def db(self):
        return self._db

    def defined_messages(self):
        return self._db.messages


    def decode_from_frame(self, msg):
        try:
            decoded_data = self.db.decode_message(msg.arbitration_id, msg.data, scaling=True)
            LOGGER.debug("decoded frame: %s", decoded_data)
            msg_name = self.db.get_message_by_frame_id(msg.arbitration_id).name
            return {msg_name: decoded_data}
        except KeyError as error:
            LOGGER.warning("key %s not found in CAN database", msg.name)
        except cantools.database.DecodeError as error:
            LOGGER.warning("unable to decode message 0x{:02x}".format(int(str(error))))
            return None


    def encode_to_frame(self, name: str, data: dict) -> can.Message:
        try:
            template = self.db.get_message_by_name(name)
        except KeyError as error:
            LOGGER.warning("no message found in database with name: %s", error)
            return None

        try:
            encoded_data = self.db.encode_message(template.frame_id, data, scaling=True)
            #LOGGER.debug(encoded_data)
            msg = can.Message(arbitration_id=template.frame_id,
                              data=encoded_data,
                              is_extended_id=template.is_extended_frame,
                              dlc=template.length)
            return msg

        except cantools.database.EncodeError as error:
            LOGGER.warning("unable to encode message 0x{:02x}".format(int(str(error))))
            return None
