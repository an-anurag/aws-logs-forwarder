# -*- coding: utf-8 -*-
"""
A customised logger for this project for logging to the file and console
Created on 12-02-2020
@author: Anurag
"""

# imports
import os
import logging

try:
    from aws_logs_forwarder.config import conf
except ModuleNotFoundError:
    from bundle.config_reader import conf


class Logger:
    """
    A Threat intelligence hub logger which will take care
    of logging to console and file.
    """

    def __init__(self, filepath):
        """
        Constructor
        :param filepath:
        """
        self.filepath = filepath
        self.logger = logging.getLogger('AWS')
        self.logger.setLevel(logging.DEBUG)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # file handler
        file_handller = logging.FileHandler(os.path.join(self.filepath))
        file_handller.setLevel(logging.DEBUG)
        file_handller.setFormatter(self._formatter)
        self.logger.addHandler(file_handller)


logger = Logger(os.path.abspath(conf.read('log-file', 'name'))).logger

