import logging
import unittest
import can
import time

from gateway import config
from canwriter import CANWriter

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

        self.assertEqual(writer._interface, "virtual")
        self.assertEqual(writer._channel, "vcan0")
        self.assertEqual(writer._baudrate, "500000")

    def test_writer(self):
        bus = can.interface.Bus("vcan0", bustype="virtual")

        writer = CANWriter(self.bootstrap['INV_COMM'])
        msg_name = 'IO_CTRL'
        msg = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name, msg)

        resp = bus.recv()
        self.assertEqual(msg.data, resp.data)
        self.assertEqual(msg.arbitration_id, resp.arbitration_id)
        
        writer.stop()
    
    def test_multi_writer_one_msg(self):
        bus = can.interface.Bus("vcan0", bustype="virtual")
        writer = CANWriter(self.bootstrap['INV_COMM'])
        
        msg_name = 'IO_CTRL'
        msg = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name, msg)

        msg = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name, msg)
      
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
       
        msg_name1 = 'IO_CTRL'
        msg1 = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name1, msg1)


        msg_name2 = 'IO_STATE'
        msg2 = can.Message(arbitration_id = 0x305,
                          data = [0xBE, 0xEF, 0xCA, 0xFE],
                          is_extended_id = False,
                          timestamp = time.time())
        
        writer.publish(msg_name2, msg2)
         
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
