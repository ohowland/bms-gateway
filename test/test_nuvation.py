import logging
import unittest
from pathlib import Path
from configparser import ConfigParser

import cantools

from gateway import config, translator 

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

