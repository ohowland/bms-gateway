import logging
import argparse

import gateway

from configparser import ConfigParser
from pathlib import Path

def main(*args, **kwargs):

    print('-----------------------')
    print('Booting Nuvation-SMA Gateway v0.1')
    print('-----------------------')
    
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    if kwargs.get('-d'):
        print('# Logging debug to console')
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)

    if kwargs.get('-c', 0):
        print('# Loading custom bootstrap configuration')
        bootstrap_path = Path.cwd().joinpath(kwargs['-c'])
    else:
        bootstrap_path = Path.cwd()
        while bootstrap_path.parent.stem == 'PGPm':
            bootstrap_path = bootstrap_path.parent
        bootstrap_path = bootstrap_path.joinpath('config', 'bootstrap.ini')
        print('# Loading bootstrap configuration: {}'.format(bootstrap_path.as_posix()))

    bootstrap_parser = ConfigParser()
    bootstrap_parser.read(bootstrap_path.as_posix())

    print('# Launching main()')
    print('-----------------------')
    gateway.main(bootstrap=bootstrap_parser)

    print('-----------------------')
    print('Shutdown Complete')
    print('-----------------------')

if __name__ == '__main__':
    main()
