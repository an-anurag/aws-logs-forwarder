# -*- coding: utf-8 -*-
"""A main aws_console log generator"""

# imports
import re
import socket
import time
from typing import Generator

# third party imports
import boto3
from geoip2.errors import AddressNotFoundError
from bundle.yaml_reader import get_confs

try:
    from bundle.config_reader import conf
    from bundle.location_finder import LocationFinder
    from bundle.logger import logger
except ModuleNotFoundError:
    from config_reader import conf
    from location_finder import LocationFinder
    from logger import logger


class CloudWatchForwarder:
    """
    A custom implemented AWS API
    """
    def __init__(self, acc_id=None, log_group=None, user_profile=None):
        """
        Constructor
        """
        self.acc_id = acc_id
        self.log_group = log_group
        self.user_profile = user_profile
        self.session = boto3.Session(profile_name=self.user_profile)
        self.cloudwatch = self.session.client('logs')
        self.sts = self.session.client('sts')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tokens = {}
        self.kwargs = {
            'logGroupName': self.log_group,
            'logStreamName': None,
        }
        self.validated_data = []

    def get_account_id(self):
        """
        Returns AWS account id
        """
        return self.sts.get_caller_identity()['Account']

    def validate_account(self):
        """
        Currently unused
        """
        try:
            account_id = self.get_account_id()
            api_call = self.cloudwatch.describe_log_groups(logGroupNamePrefix=self.log_group)['logGroups'][0]
            log_grp = api_call['logGroupName']
            if log_grp:
                if (log_grp == self.log_group) and (account_id == self.acc_id):
                    self.validated_data.append([self.acc_id, self.log_group, self.user_profile])
                    return True
            return False
        except IndexError:
            logger.exception("Invalid account id or log group", exc_info=False)

    def get_log_streams(self) -> list:
        """
        Logic to fetch all log stream in a given log group
        :return:
        """
        stream_batch = list()
        streams = self.cloudwatch.describe_log_streams(logGroupName=self.log_group)['logStreams']
        for stream in streams:
            stream_batch.append(stream['logStreamName'])
        return stream_batch

    def get_logs(self, streams) -> Generator[dict, None, None]:
        """
        A logic to continuously poll each log stream to fetch logs in  batch
        :return:
        """

        while True:
            for stream in streams:
                self.kwargs['logStreamName'] = stream
                if self.tokens.get(stream):
                    self.kwargs['nextToken'] = self.tokens[stream]
                resp = self.cloudwatch.get_log_events(**self.kwargs)
                yield from resp['events']
                self.tokens[stream] = str(resp['nextForwardToken'])
                time.sleep(15)

    def forward(self, host: str, port: int, log: str) -> None:
        """
        A method to forward logs to graylog input
        :param host:
        :param port:
        :param log:
        :return:
        """
        self._socket.sendto(bytes(log, encoding='utf-8'), (host, int(port)))

    @staticmethod
    def add_location(log: str) -> str:
        """
        A method to return ip geolocation if ip present in log
        :param log:
        :return:
        """
        ip_pat = re.compile(r'sourceIPAddress":\s?"(?P<src_ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')
        match = ip_pat.search(log)
        try:
            if match:
                ip = match.group('src_ip')
                city = LocationFinder(ip).get_city()
                lat = LocationFinder(ip).get_latitude()
                long = LocationFinder(ip).get_longitude()
                location = r''', 'location': {"ip_city":"%s","latitude":"%s","longitude":"%s"}''' % (city, lat, long)
                return log + location
            return log
        except AddressNotFoundError:
            return log

    def run(self, host, port):
        streams = self.get_log_streams()
        for log in self.get_logs(streams=streams):
            log = self.add_location(str(log))
            # self.forward(host, port, log)
            print(log)



# c = CloudWatchForwarder(acc_id='202925831767', log_group='/aws/cloudtrail/console-events', user_profile='default')
