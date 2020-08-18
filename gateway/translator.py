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
    "IO_DOD": {
        "IO_DOD": {
            None
        },
    },
    "IO_MAX_CELL_V": {
        "IO_MAX_CELL_V": {
            None
        },
    },
    "IO_MIN_CELL_V": {
        "IO_MIN_CELL_V": {
            None
        },
    },
    "IO_AVG_CELL_V": {
        "IO_AVG_CELL_V": {
            None
        },
    },
    "IO_MAX_CELL_TEMP": {
        "IO_MAX_CELL_TEMP": {
            None
        },
    },
    "IO_MIN_CELL_TEMP": {
        "IO_MIN_CELL_TEMP": {
            None
        },
    },
    "IO_AVG_CELL_TEMP": {
        "IO_AVG_CELL_TEMP": {
            "IO_STATUS": "IO_STATUS_TEMP"
        },
    },
    "IO_OVERALL_SAFE": {
        "IO_OVERALL_SAFE": {
            "IO_ALARM": { "IO_ALARM_GENERAL_ARRIVE", "IO_ALARM_GENERAL_LEAVE" } 
        },
    },
    "IO_SAFE_TO_CHRG": {
        "IO_SAFE_TO_CHRG": {
            None
        },
    },
    "IO_SAFE_TO_DISCHRG": {
        "IO_SAFE_TO_DISCHRG": {
            None
        },
    },
    "IO_CHRG_I_LIM": {
        "IO_CHRG_I_LIM": {
            "IO_CTRL": "IO_CTRL_BATT_CHRG_I_LIM" 
        },
    },
    "IO_CHRG_PCT_LIM": {
        "IO_CHRG_PCT_LIM": {
            None
        },
    },
    "IO_DISCHRG_I_LIM": {
        "IO_DISCHRG_I_LIM": {
            "IO_CTRL": "IO_CTRL_BATT_DISCHRG_I_LIM" 
        },
    },
    "IO_DISCHRG_PCT_LIM": {
        "IO_DISCHRG_PCT_LIM": {
            None
        },
    },
    "IO_STACK_STATE": {
        "IO_STACK_STATE": {
            None
        },
    },
    "IO_HEARTBEAT": {
        "IO_HEARTBEAT": {
            None
        },
    },
    "IO_FAULT_STACK_HI_V": {
        "IO_FAULT_STACK_HI_V": {
            "IO_ALARM" : { "IO_ALARM_HI_V_ARRIVE", "IO_ALARM_HI_V_LEAVE" }
        },
    },
    "IO_FAULT_STACK_LO_V": {
        "IO_FAULT_STACK_LO_V": {
            "IO_ALARM" : { "IO_ALARM_LO_V_ARRIVE", "IO_ALARM_LO_V_LEAVE" }
        },
    },
    "IO_FAULT_TEMP_HI": {
        "IO_FAULT_TEMP_HI": {
            None
        },
    },
    "IO_FAULT_TEMP_LO": {
        "IO_FAULT_TEMP_LO": {
            None
        },
    },
    "IO_FAULT_CHRG_TEMP_HI": {
        "IO_FAULT_CHRG_TEMP_HI": {
            None
        },
    },
    "IO_FAULT_CHRG_TEMP_LO": {
        "IO_FAULT_CHRG_TEMP_LO": {
            None
        },
    },
    "IO_FAULT_STACK_HI_I": {
        "IO_FAULT_STACK_HI_I": {
            None
        },
    },
    "IO_FAULT_STACK_LO_I": {
        "IO_FAULT_STACK_LO_I": {
            None
        },
    },
    "IO_FAULT_CONTACTOR": {
        "IO_FAULT_CONTACTOR": {
            None
        },
    },
    "IO_FAULT_LINKBUS": {
        "IO_FAULT_LINKBUS": {
            None
        },
    },
    "IO_CHRG_V": {
        "IO_CHRG_V": {
            "IO_CTRL": "IO_CTRL_BATT_CHRG_V"
        },
    },
    "IO_DISCHRG_V": {
        "IO_DISCHRG_V": {
            "IO_CTRL": "IO_CTRL_BATT_DISCHRG_V"
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
