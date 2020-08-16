import logging
import unittest
from pathlib import Path
from configparser import ConfigParser

import cantools

from gateway import config

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger('testing')

class TestNuvation(unittest.TestCase):

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

        io_ctrl = self.db.get_message_by_name('IO_STACK_V')
        self.assertEqual(io_ctrl.frame_id, 0x101)

    def test_io_ctrl_signals(self):
        ''' Test the signal integrity of the manditory control message
        '''
        
        io_ctrl = self.db.get_message_by_name('IO_STACK_V')
        self.assertEqual(io_ctrl.signals[0].name, 'IO_STACK_V')
        self.assertEqual(io_ctrl.signals[0].length, 32)
        self.assertTrue(io_ctrl.signals[0].is_signed)
        #self.assertEqual(io_ctrl.signals[0].start, 0)
        

    def test_io_ctrl_encoding(self):
        ''' Test message encoding and decoding
        '''

        io_ctrl = self.db.get_message_by_name('IO_STACK_V')
        
        test_data = {'IO_STACK_V': 51}
        encoded_test_data = io_ctrl.encode(test_data)
        self.assertEqual(encoded_test_data.hex(), '00')

        decoded_test_data = io_ctrl.decode(encoded_test_data)
        self.assertEqual(test_data, decoded_test_data)

'''
    def test_update_bad_sig(self):
        inv = Translator(self.bootstrap['INV_COMM'])
        self.assertRaises(KeyError, inv.encode_to_frame, name='JERRY_CTRL', data={'jerry': 1})

    def test_update_half_sig(self):
        inv = Translator(self.bootstrap['INV_COMM'])
        
        half_msg_data = {'IO_CTRL_BATT_CHRG_V': 51,
                'IO_CTRL_BATT_CHRG_I_LIM': 400}

        self.assertRaises(TypeError, inv.encode_to_frame, name='IO_CTRL', data=half_msg_data)

    def test_update_good_sig(self):
        inv = Translator(self.bootstrap['INV_COMM'])
        
        name = 'IO_CTRL'
        data = {'IO_CTRL_BATT_CHRG_V': 51,
                'IO_CTRL_BATT_CHRG_I_LIM': 400,
                'IO_CTRL_BATT_DISCHRG_I_LIM': 500,
                'IO_CTRL_BATT_DISCHRG_V': 48}
       
        encoded = inv.encode_to_frame(name, data)
        decoded = inv.decode_from_frame(encoded)
        self.assertEqual(decoded[name], data)
'''
