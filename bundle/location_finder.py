# -*- coding: utf-8 -*-
"""
Ip address location updater using local db on given parameters
Created on 10/9/2019
@author: Anurag
"""

# imports
import os
import geoip2.database

try:
    from bundle.config_reader import conf
except ModuleNotFoundError:
    from config_reader import conf


class LocationFinder:
    """
    A class to implement custom location updater for easy fetching of location parameters
    """

    def __init__(self, ip_address):
        """
        Instance initialisation
        :param ip_address:
        """
        self.ip_address = ip_address
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), conf.read('geoip2-db', 'db'))
        if not os.path.isfile(db_path):
            raise FileNotFoundError("GeoLite database is not present")
        else:
            self._reader = geoip2.database.Reader(os.path.join(db_path))
            self._result = self._reader.city(self.ip_address)
            self._reader.close()

    def get_city(self):
        """
        Method to retrieve ip address city name
        :return: city in string
        """
        return self._result.city.name

    def get_country(self):
        """
        Method to retrieve ip address country
        :return: country in string
        """
        return self._result.country.name

    def get_latitude(self):
        """
        Method to retrieve ip address latitude
        :return: latitude in string
        """
        return self._result.location.latitude

    def get_longitude(self):
        """
        Method to retrieve ip address longitude
        :return: longitude in string
        """
        return self._result.location.longitude
