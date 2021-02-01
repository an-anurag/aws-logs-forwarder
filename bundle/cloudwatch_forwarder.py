# -*- coding: utf-8 -*-
"""A main aws_console log generator"""

# imports
import re
import os
import socket
import time
import datetime
import sys

import pytz

# third party imports
import boto3
from geoip2.errors import AddressNotFoundError

try:
    from config_reader import conf
    from location_finder import LocationFinder
    from logger import logger
except ImportError:
    from bundle.config_reader import conf
    from bundle.location_finder import LocationFinder
    from bundle.logger import logger


class CloudWatchForwarder:
    """
    A custom implemented AWS API
    """
    def __init__(self, acc_id=None, log_group=None, user_profile=None, host=None, port=None):
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
        self.host = host
        self.port = port
        self.log_dir = os.path.join('/var/log/')
        self.log_path = None
        self.timezone = pytz.timezone(conf.read('time', 'timezone'))

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

    def get_log_streams(self):
        """
        Logic to fetch all log stream in a given log group
        :return:
        """
        stream_batch = list()
        streams = self.cloudwatch.describe_log_streams(logGroupName=self.log_group)['logStreams']
        for stream in streams:
            stream_batch.append(stream['logStreamName'])
        return stream_batch

    def get_logs(self, streams):
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
                # yield from resp['events']
                for log in resp['events']:
                    yield log
                self.tokens[stream] = str(resp['nextForwardToken'])
                time.sleep(15)

    def forward(self, log):
        """
        A method to forward logs to graylog input
        :param host:
        :param port:
        :param log:
        :return:
        """
        if sys.version_info.major == '2':
            self._socket.sendto(log, (self.host, int(self.port)))
        else:
            self._socket.sendto(bytes(log), (self.host, int(self.port)))

    @staticmethod
    def add_location(log):
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
                location = r''',"location":{"ip_city":"%s","latitude":"%s","longitude":"%s"}''' % (city, lat, long)
                return log + location
            return log
        except AddressNotFoundError:
            return log

    @staticmethod
    def add_keyword(log, log_group_name):
        """
        Method to add keyword in every log according to platform
        """

        if 'windows-ami' in log_group_name.lower():
            return 'windows-ami - ' + log

        if 'ubuntu-ami' in log_group_name.lower():
            return 'ubuntu-ami - ' + log

        if 'centos-ami' in log_group_name.lower():
            return 'centos-ami - ' + log

        if 'aws-console' in log_group_name.lower():
            return 'aws-console - ' + log
        
    def get_log_filename(self, log_group_name):

        log_dir = self.log_dir

        if 'windows-ami' in log_group_name.lower():
            self.log_path = log_dir + 'windows-ami.log'
            return self.log_path

        if 'ubuntu-ami' in log_group_name.lower():
            self.log_path = log_dir + 'ubuntu-ami.log'
            return self.log_path

        if 'centos-ami' in log_group_name.lower():
            self.log_path = log_dir + 'centos-ami.log'
            return self.log_path

        if 'aws-console' in log_group_name.lower():
            self.log_path = log_dir + 'aws-console.log'
            return self.log_path

    def add_timestamp(self, log):
        now = datetime.datetime.now(tz=self.timezone)
        clean = now.strftime('%a %d %H:%M:%S')
        return clean + " " + log

    def run(self):
        self.get_log_filename(self.log_group)
        streams = self.get_log_streams()
        with open(self.log_path, 'a+') as log_file:
            for log in self.get_logs(streams=streams):
                log = self.add_location(str(log))
                log = self.add_keyword(log, self.log_group)
                log = self.add_timestamp(log)
                self.forward(log)
                log_file.write('%s\n' % str(log))
                print(log)
