import logging
from logging.handlers import RotatingFileHandler

import gateway

from configparser import ConfigParser
from pathlib import Path

def main(*args, **kwargs):
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.handlers.RotatingFileHandler('error.log', maxBytes=100000, backupCount=1)
    fh.setLevel(logging.WARNING)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(name)s_%(levelname)s: %(message)s') 
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('-----------------------')
    logger.info('Booting Nuvation-SMA Gateway v0.1')
    logger.info('-----------------------')

    bootstrap_path = Path.cwd()
    logger.info(bootstrap_path)
    while bootstrap_path.parent.stem == 'bms-gateway':
        bootstrap_path = bootstrap_path.parent
    bootstrap_path = bootstrap_path.joinpath('config', 'bootstrap.ini')
    logger.info('Loading bootstrap configuration: {}'.format(bootstrap_path.as_posix()))
    bootstrap_parser = ConfigParser()
    bootstrap_parser.read(bootstrap_path.as_posix())

    gateway.main(bootstrap=bootstrap_parser)

    print('-----------------------')
    print('Shutdown Complete')
    print('-----------------------')

if __name__ == '__main__':
    main()
