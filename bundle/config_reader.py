# -*- coding: utf-8 -*-
"""A setup file reader for the aws_console module"""

import os
import sys

if sys.version_info.major == 2:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


class ConfigReader:
    """
    A class to implement custom cfg file reader
    """
    def __init__(self):
        self.aws_conf = ConfigParser()
        self.cfg_file = os.path.join(os.path.dirname(__file__), '../setup.cfg')
        self._config = ConfigParser()
        self._config.read(self.cfg_file)

    def read(self, section, option):
        """
        A read method to read key and values
        :return:
        """
        return self._config.get(section, option)

    def get_profile_names(self):
        """
        Retrieve AWS credential from machine
        :return:
        """
        path = self.read('default', 'path')
        self.aws_conf.read(os.path.expanduser(path))
        return self.aws_conf.sections()


conf = ConfigReader()
