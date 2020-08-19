""" Name: config.py
    Author: Howl & Edgerton, llc 2019
    About: Helper functions for configuration
"""
#import logging

from pathlib import Path

def get(filename, **kwargs):
    """ Return path to the filename, file must exist at top level of config folder
    """

    base_path = Path.cwd()
    #logging.debug('base_path: {}'.format(base_path))
    while base_path.parent.stem == 'gateway':
        base_path = base_path.parent

    if kwargs.get('TESTING'):
        path_to_file = base_path.joinpath('test', 'config', filename)
    else:
        path_to_file = base_path.joinpath('config', filename)

    #logging.debug('path_to_file: {}'.format(path_to_file))
    return path_to_file
