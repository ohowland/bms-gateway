""" Name: translator.py
    Author: Howl & Edgerton, llc 2020 
"""

import logging
import re
from functools import partial

log = logging.getLogger('translator')

alarm_re = re.compile("^\w+_(ARRIVE|LEAVE)$")

class Translator(object):
    def __init__(self):
        self._map = BMS_TO_SMA


    def translate(self, from_msg):
        ''' returns a translated message mapped from bms to sma
        '''

        to_msgs = {}
        for msg_name, sigs in from_msg.items():
            for sig_name, sig_val in sigs.items():
                 to_msg = self._get_mapping(msg_name, sig_name)
                 if to_msg:
                     to_msgs = to_msg.transfer_function(sig_val, to_msgs)
                 else:
                     log.debug("CAN message {}::{} is not mapped, consider removing from production dbc".format(msg_name, sig_name))

        return to_msgs
    
    def _get_mapping(self, msg_name, sig_name):
        ''' returns a dict{set{}} {message_name: {signal name(s)}} for the inverter 
            that correspond to the message name and signal name provided
        '''

        return self._map[msg_name][sig_name]


def _write_sig_val(msg_name, sig_name, sig_value, to_msgs):
    ''' returns a mutated translated_msgs which contains an updated msg
        with the signal value
    '''

    existing_msg = to_msgs.get(msg_name, None)
    if existing_msg:
        to_msgs[msg_name][sig_name] = sig_value
    else:
        to_msgs[msg_name] = {sig_name: sig_value}

    return to_msgs 

class Map:
    def __init__(self, msg, tfunc):
        self._msg = msg
        self._tfunc = tfunc  # function that knows how to decode the mapping

    def msg(self):
        return self._msg

    def transfer_function(self, sig_val, to_msgs):
        return self._tfunc(self._msg, sig_val, to_msgs)

    def map_alarm_sig(to_msg, sig_val, to_msgs):
        ''' returns a mutate to_msgs which contains a mapped boolean alarm value
        '''

        for msg_name, sig_names in to_msg.items():
            for sig_name in sig_names:
                m = alarm_re.match(sig_name)
                if m:
                    if m.group(1) == "ARRIVE":
                        to_msgs = _write_sig_val(
                                msg_name,
                                sig_name,
                                sig_val,
                                to_msgs,
                        )
                elif m.group(1) == "LEAVE":
                    to_msgs = _write_sig_val(
                                msg_name,
                                sig_name,
                                not sig_val, # flip the bit, leave == !arrive
                                to_msgs,
                    )
                else:
                    log.warning("unable to match alarm signal: {}".format(sig_name))

       return to_msgs

    def map_invert_alarm_sig(to_msg, sig_val, to_msgs):
        ''' returns a mutate to_msgs which contains a mapped boolean alarm value
            that is inverted. boolean hi = no alarm, boolean lo = alarm.
        '''
        for msg_name, sig_names in to_msg.items():
            for sig_name in sig_names:
                m = alarm_re.match(sig_name)
                if m:
                    if m.group(1) == "ARRIVE":
                        to_msgs= _write_sig_val(
                                msg_name,
                                sig_name,
                                not sig_val, # flip the bit, leave == !arrive

                                to_msgs,
                        )
                    elif m.group(1) == "LEAVE":
                        to_msgs = _write_sig_val(
                                msg_name,
                                sig_name,
                                sig_val,
                                to_msgs,
                        )
                    else:
                        log.warning("unable to match alarm signal: {}".format(sig_name))
        return to_msgs
        

    def map_default_sig(to_msg, sig_value, to_msgs):
        ''' returns a mutated translated_msgs which contains the message and signal value
        ''' 

        for msg_name, sig_names in to_msg.items():
            for sig_name in sig_names:
                to_msgs = _write_sig_val(
                        msg_name,
                        sig_name,
                        sig_value,
                        to_msgs,
                )

        return to_msgs

BMS_TO_SMA = { 
    "IO_STACK_V": {
        "IO_STACK_V":  
            Map({"IO_STATUS": {"IO_STATUS_V"}}, Map.map_default_sig) 
    },
    "IO_STACK_I": {
        "IO_STACK_I": 
            Map({"IO_STATUS": {"IO_STATUS_I"}}, Map.map_default_sig)
    },
    "IO_SOC": {
        "IO_SOC": 
            Map({"IO_STATE": {"IO_STATE_SOC", "IO_STATE_SOC_HIRES"}}, Map.map_default_sig)
    },
    "IO_DOD": {
        "IO_DOD":
            None
    },
    "IO_MAX_CELL_V": {
        "IO_MAX_CELL_V":
            None
    },
    "IO_MIN_CELL_V": {
        "IO_MIN_CELL_V":
            None
    },
    "IO_AVG_CELL_V": {
        "IO_AVG_CELL_V":
            None
    },
    "IO_MAX_CELL_TEMP": {
        "IO_MAX_CELL_TEMP":
            None
    },
    "IO_MIN_CELL_TEMP": {
        "IO_MIN_CELL_TEMP":
            None
    },
    "IO_AVG_CELL_TEMP": {
        "IO_AVG_CELL_TEMP":
            Map({"IO_STATUS": {"IO_STATUS_TEMP"}}, Map.map_default_sig)
    },
    "IO_OVERALL_SAFE": {
        "IO_OVERALL_SAFE":
            Map({"IO_ALARM": {"IO_ALARM_GENERAL_ARRIVE", "IO_ALARM_GENERAL_LEAVE"}"IO_WARN": { "IO_WARN_GENERAL_ARRIVE", "IO_WARN_GENERAL_LEAVE"}}, Map.map_invert_alarm_sig)
    },
    "IO_SAFE_TO_CHRG": {
        "IO_SAFE_TO_CHRG":
            None
    },
    "IO_SAFE_TO_DISCHRG": {
        "IO_SAFE_TO_DISCHRG":
            None
    },
    "IO_CHRG_I_LIM": {
        "IO_CHRG_I_LIM":
            Map({"IO_CTRL": {"IO_CTRL_BATT_CHRG_I_LIM"}}, Map.map_default_sig)
    },
    "IO_CHRG_PCT_LIM": {
        "IO_CHRG_PCT_LIM":
            None
    },
    "IO_DISCHRG_I_LIM": {
        "IO_DISCHRG_I_LIM":
            Map({"IO_CTRL": {"IO_CTRL_BATT_DISCHRG_I_LIM"}}, Map.map_default_sig)
    },
    "IO_DISCHRG_PCT_LIM": {
        "IO_DISCHRG_PCT_LIM":
            None
    },
    "IO_STACK_STATE": {
        "IO_STACK_STATE":
            None
    },
    "IO_HEARTBEAT": {
        "IO_HEARTBEAT":
            None
    },
    "IO_FAULT_STACK_HI_V": {
        "IO_FAULT_STACK_HI_V":
        Map({"IO_ALARM" : {"IO_ALARM_HI_V_ARRIVE", "IO_ALARM_HI_V_LEAVE"}, "IO_WARN": {"IO_ALARM_HI_V_ARRIVE", "IO_ALARM_HI_V_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_STACK_LO_V": {
        "IO_FAULT_STACK_LO_V":
            Map({"IO_ALARM" : {"IO_ALARM_LO_V_ARRIVE", "IO_ALARM_LO_V_LEAVE"} "IO_WARN" : {"IO_WARN_LO_V_ARRIVE", "IO_WARN_LO_V_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_TEMP_HI": {
        "IO_FAULT_TEMP_HI":
            Map({"IO_ALARM" : {"IO_ALARM_HI_TEMP_ARRIVE", "IO_ALARM_HI_TEMP_LEAVE"} "IO_WARN" : {"IO_WARN_HI_TEMP_ARRIVE", "IO_WARN_HI_TEMP_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_TEMP_LO": {
        "IO_FAULT_TEMP_LO":
            Map({"IO_ALARM" : {"IO_ALARM_LO_TEMP_ARRIVE", "IO_ALARM_LO_TEMP_LEAVE"} "IO_WARN" : {"IO_WARN_LO_TEMP_ARRIVE", "IO_WARN_LO_TEMP_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_CHRG_TEMP_HI": {
        "IO_FAULT_CHRG_TEMP_HI":
            Map({"IO_ALARM" : {"IO_ALARM_HI_TEMP_CHRG_ARRIVE", "IO_ALARM_HI_TEMP_CHRG_LEAVE"} "IO_WARN" : {"IO_WARN_HI_TEMP_CHRG_ARRIVE", "IO_WARN_HI_TEMP_CHRG_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_CHRG_TEMP_LO": {
        "IO_FAULT_CHRG_TEMP_LO":
            Map({"IO_ALARM" : {"IO_ALARM_LO_TEMP_CHRG_ARRIVE", "IO_ALARM_LO_TEMP_CHRG_LEAVE"} "IO_WARN" : {"IO_WARN_LO_TEMP_CHRG_ARRIVE", "IO_WARN_LO_TEMP_CHRG_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_STACK_HI_I": {
        "IO_FAULT_STACK_HI_I":
            Map({"IO_ALARM" : {"IO_ALARM_HI_I_ARRIVE", "IO_ALARM_HI_I_LEAVE"} "IO_WARN" : {"IO_WARN_HI_I_ARRIVE", "IO_WARN_HI_I_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_STACK_LO_I": {
        "IO_FAULT_STACK_LO_I":
            Map({"IO_ALARM" : {"IO_ALARM_HI_I_CHRG_ARRIVE", "IO_ALARM_HI_I_CHRG_LEAVE"} "IO_WARN" : {"IO_WARN_HI_I_CHRG_ARRIVE", "IO_WARN_HI_I_CHRG_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_CONTACTOR": {
        "IO_FAULT_CONTACTOR":
            Map({"IO_ALARM" : {"IO_ALARM_CONTACTOR_ARRIVE", "IO_ALARM_CONTACTOR_LEAVE"} "IO_WARN" : {"IO_WARN_CONTACTOR_ARRIVE", "IO_WARN_CONTACTOR_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_FAULT_LINKBUS": {
        "IO_FAULT_LINKBUS":
            Map({"IO_ALARM" : {"IO_ALARM_BMS_ARRIVE", "IO_ALARM_BMS_LEAVE"} "IO_WARN" : {"IO_WARN_BMS_ARRIVE", "IO_WARN_BMS_LEAVE"}}, Map.map_alarm_sig)
    },
    "IO_CHRG_V": {
        "IO_CHRG_V":
            Map({"IO_CTRL": { "IO_CTRL_BATT_CHRG_V" }}, Map.map_default_sig)
    },
    "IO_DISCHRG_V": {
        "IO_DISCHRG_V":
            Map({"IO_CTRL": { "IO_CTRL_BATT_DISCHRG_V" }}, Map.map_default_sig)
    },
    
}

