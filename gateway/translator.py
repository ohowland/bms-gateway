""" Name: translator.py
    Author: Howl & Edgerton, llc 2020 
"""

import logging

BMS = { 
    "IO_STACK_V": {
        "IO_STACK_V": { 
            "IO_STATUS": "IO_STATUS_V"
        },
    },
    "IO_STACK_I": {
        "IO_STACK_I": {
            "IO_STATUS": "IO_STATUS_I"
        },
    },
    "IO_SOC": {
        "IO_SOC": {
            "IO_STATE": { "IO_STATE_SOC", "IO_STATE_SOC_HIRES" }
        },
    },
}

class Translator(object):
    def __init__(self):
        self.bms_to_inv = BMS

    def translate(self, msg):
        translated_msgs = {}
        for msg_name, signals in msg.items():
            for signal_name, signal_value in signals.items():
                 msg_map = self.bms_to_inv[msg_name][signal_name]
                 translated_msgs = self._map_signal(msg_map, signal_value, translated_msgs)

        return translated_msgs

    def _map_signal(self, msg_map, signal_value, translated_msgs):
        for t_msg_name, t_signal_names in msg_map.items():
            # If t_signal_name is not a set, then we need to prevent
            # python from iterating over the string as chars.
            if isinstance(t_signal_names, str):
                translated_msgs = self._update_translated_msgs(
                    t_msg_name,
                    t_signal_names,
                    signal_value,
                    translated_msgs,
                )
            else:
                for t_signal_name in t_signal_names:
                    translated_msgs = self._update_translated_msgs(
                        t_msg_name,
                        t_signal_name,
                        signal_value,
                        translated_msgs,
                    )

        return translated_msgs

    def _update_translated_msgs(self, t_msg_name, t_signal_name, signal_value, translated_msgs):
        existing_signal = translated_msgs.get(t_msg_name, None)
        if existing_signal:
            translated_msgs[t_msg_name][t_signal_name] = signal_value
        else:
            translated_msgs[t_msg_name] = {t_signal_name: signal_value}
        return translated_msgs



    
