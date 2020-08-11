import logging
import unittest
import can
import time

from gateway import config
from gateway.can_writer import CANWriter

from pathlib import Path
from configparser import ConfigParser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestCANWriter(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_config(self):
        writer = CANWriter(self.bootstrap['INV_COMM'])

        self.assertEqual(writer.interface, "virtual")
        self.assertEqual(writer.channel, "vcan0")
        self.assertEqual(writer.baudrate, "500000")

    def test_writer(self):
        bus = can.interface.Bus("vcan0", bustype="virtual")

        writer = CANWriter(self.bootstrap['INV_COMM'])
        test_msg = {
                'IO_CTRL': can.Message(
                    arbitration_id = 0x321,
                    data = [0xDE, 0xAD, 0xBE, 0xEF],
                    is_extended_id = False,
                    timestamp = time.time())
        }
        writer.update(test_msg)

        resp = bus.recv()
        self.assertEqual(test_msg['IO_CTRL'].data, resp.data)
        self.assertEqual(test_msg['IO_CTRL'].arbitration_id, resp.arbitration_id)

        self.assertNotEqual([0xBE, 0xEF, 0xCA, 0xFE], resp.data)
        
        writer.stop()
    
    def test_multi_writer_one_msg(self):
        bus = can.interface.Bus("vcan0", bustype="virtual")
        writer = CANWriter(self.bootstrap['INV_COMM'])
        
        test_msg1 = {
                'IO_CTRL': can.Message(
                    arbitration_id = 0x321,
                    data = [0xDE, 0xAD, 0xBE, 0xEF],
                    is_extended_id = False)
        }
        writer.update(test_msg1)
         
        test_msg2 = {
                'IO_CTRL': can.Message(
                    arbitration_id = 0x321,
                    data = [0xBE, 0xEF, 0xCA, 0xFE],
                    is_extended_id = False)
        }
        writer.update(test_msg2)
        
        c = 0 
        for msg in bus:
            if c == 3:
                break
            self.assertEqual(msg.arbitration_id, 0x321)
            c+=1
        
        writer.stop()
    
    def test_multi_writer_multi_msg(self):
        bus = can.interface.Bus("vcan0", bustype="virtual")
        writer = CANWriter(self.bootstrap['INV_COMM'])

        test_msg1 = {
                'IO_CTRL': can.Message(
                    arbitration_id = 0x321,
                    data = [0xDE, 0xAD, 0xBE, 0xEF],
                    is_extended_id = False)
        }
        writer.update(test_msg1)
         
        test_msg2 = {
                'IO_STATE': can.Message(
                    arbitration_id = 0x305,
                    data = [0xBE, 0xEF, 0xCA, 0xFE],
                    is_extended_id = False)
        }
        writer.update(test_msg2)

        c = 0
        for msg in bus:
            c += 1
            if c > 4:
                break
            if msg.arbitration_id == 0x321:
                continue
            elif msg.arbitration_id == 0x305:
                continue
            else:
                self.assertTrue(False, "invalid arbitration id on bus")
        
        writer.stop()
