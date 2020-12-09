# -*- coding: utf-8 -*-
"""A main logic to continuously running this script"""

import time
import socket
from threading import Thread

try:
    from aws_logs_forwarder.cloudwatch_forwarder import CloudWatchForwarder
    from aws_logs_forwarder.logger import logger
    from aws_logs_forwarder.config import conf
except ModuleNotFoundError:
    from bundle.cloudwatch_forwarder import CloudWatchForwarder
    from bundle.logger import logger
    from bundle.config_reader import conf
    from bundle.yaml_reader import get_confs

HOST = conf.read('prod-logger-input', 'host')
PORT = conf.read('prod-logger-input', 'port')


def main():
    """
    A main logic
    """

    try:
        accounts = get_confs()['accounts']
        print(accounts)
        profiles = conf.get_profile_names()
        print(profiles)

        for profile in profiles:
            for acc in accounts:
                acc_id = acc['id']
                log_group = acc['log_groups'][0]
                print(acc_id, log_group, profile)
                # cloudwatch = CloudWatchForwarder(acc_id=acc['id'], log_group=acc['log_groups'][0], user_profile=profile)
                # if cloudwatch.validate_account():
                #     thread = Thread(target=cloudwatch.run, args=(HOST, PORT))
                #     thread.start()
                # else:
                #     print("invalid account")

    except socket.timeout as err:
        logger.exception("timeout occurred, trying again", err)
        time.sleep(60)
        return main()
    except socket.gaierror as err:
        logger.exception("Connection error, trying again", err)
        time.sleep(60)
        return main()
    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
