import logging
import unittest
from pathlib import Path
from configparser import ConfigParser

import cantools

from gateway import config, nuvation

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger('debug')

class TestSMADBC(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser
        self.db = cantools.database.load_file(bootstrap_parser['BMS_COMM']['dbc_filepath'])

    def tearDown(self):
        pass
    
    def test_dbc_load(self):
        ''' Test that the manditory control message can be read from 
            the dbc file.
        '''

        io_ctrl = self.db.get_message_by_name('IO_CTRL')
        self.assertEqual(io_ctrl.frame_id, 0x351)

    def test_io_ctrl_signals(self):
        ''' Test the signal integrity of the manditory control message
        '''
        
        io_ctrl = self.db.get_message_by_name('IO_CTRL')
        self.assertEqual(io_ctrl.signals[0].name, 'IO_CTRL_BATT_CHRG_V')
        self.assertEqual(io_ctrl.signals[0].length, 16)
        self.assertFalse(io_ctrl.signals[0].is_signed)
        self.assertEqual(io_ctrl.signals[0].start, 0)
        
        self.assertEqual(io_ctrl.signals[1].name, 'IO_CTRL_BATT_CHRG_I_LIM')
        self.assertEqual(io_ctrl.signals[1].length, 16)
        self.assertTrue(io_ctrl.signals[1].is_signed)
        self.assertEqual(io_ctrl.signals[1].start, 16)
        
        self.assertEqual(io_ctrl.signals[2].name, 'IO_CTRL_BATT_DISCHRG_I_LIM')
        self.assertEqual(io_ctrl.signals[2].length, 16)
        self.assertTrue(io_ctrl.signals[2].is_signed)
        self.assertEqual(io_ctrl.signals[2].start, 32)

        self.assertEqual(io_ctrl.signals[3].name, 'IO_CTRL_BATT_DISCHRG_V')
        self.assertEqual(io_ctrl.signals[3].length, 16)
        self.assertFalse(io_ctrl.signals[3].is_signed)
        self.assertEqual(io_ctrl.signals[3].start, 48)

    def test_io_ctrl_encoding(self):
        ''' Test message encoding and decoding
        '''

        io_ctrl = self.db.get_message_by_name('IO_CTRL')
        
        test_data = {'IO_CTRL_BATT_CHRG_V': 51,
                'IO_CTRL_BATT_CHRG_I_LIM': 400,
                'IO_CTRL_BATT_DISCHRG_I_LIM': 500,
                'IO_CTRL_BATT_DISCHRG_V': 48}

        encoded_test_data = io_ctrl.encode(test_data)
        self.assertEqual(encoded_test_data.hex(), 'fe01a00f8813e001')

        decoded_test_data = io_ctrl.decode(bytes.fromhex('fe01a00f8813e001'))
        self.assertEqual(test_data, decoded_test_data)

    def test_sma(self):
        bms = nuvation.Nuvation(self.bootstrap['BMS_COMM']) 

    def test_update_bad_sig(self):
        bms = nuvation.Nuvation(self.bootstrap['BMS_COMM'])
        self.assertRaises(KeyError, bms.update_status, {'jerry': 1})

    def test_update_half_sig(self):
        bms = nuvation.Nuvation(self.bootstrap['BMS_COMM'])
        
        half_msg_data = {'IO_CTRL_BATT_CHRG_V': 51,
                'IO_CTRL_BATT_CHRG_I_LIM': 400}

        self.assertRaises(TypeError, bms.update_status, half_msg_data)

    def test_update_good_sig(self):
        bms = nuvation.Nuvation(self.bootstrap['BMS_COMM'])
        
        test_data = {'IO_CTRL_BATT_CHRG_V': 51,
                'IO_CTRL_BATT_CHRG_I_LIM': 400,
                'IO_CTRL_BATT_DISCHRG_I_LIM': 500,
                'IO_CTRL_BATT_DISCHRG_V': 48}
       
        bms.update_status(test_data)

        self.assertIsNot(bms.messages, None)
